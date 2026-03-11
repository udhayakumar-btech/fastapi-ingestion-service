import os
import logging
from celery import Celery
from concurrent.futures import ThreadPoolExecutor

from .workers import fetch_with_limit
from .db import SessionLocal
from .models import Job, RawEvent, Entity
from .utils import idempotency_key


from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Create Celery app FIRST

# Get Redis URL from environment
REDIS_URL = os.getenv("REDIS_URL")

celery_app = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)

# 2. THEN define tasks
@celery_app.task(bind=True, max_retries=3)
def ingest_job(self, job_id, providers):
    logger.info(f"Starting job {job_id} with providers: {providers}")
    db = SessionLocal()
    try:
        job = db.query(Job).get(job_id)
        job.state = "running"
        db.commit()


        #Test API's
        urls = {
            "api1": "https://jsonplaceholder.typicode.com/posts",
            "api2": "https://jsonplaceholder.typicode.com/comments",
        }

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(fetch_with_limit, p, urls[p]): p for p in providers}
            for f, p in futures.items():
                try:
                    data = f.result()
                    logger.info(f"Provider {p} returned: {data}")
                except Exception as e:
                    logger.error(f"Error fetching from {p}: {e}")
                    raise

                raw = RawEvent(job_id=job_id, provider=p, payload=data)
                db.add(raw)

                if isinstance(data, list):
                    for item in data:
                        if "id" in item:
                            key = idempotency_key(p, item["id"])
                            entity = Entity(
                                provider=p,
                                external_id=item["id"],
                                normalized=item,
                                derived_field="extra_info"
                            )
                            db.add(entity)
                elif isinstance(data, dict) and "id" in data:
                    key = idempotency_key(p, data["id"])
                    entity = Entity(
                        provider=p,
                        external_id=data["id"],
                        normalized=data,
                        derived_field="extra_info"
                    )
                    db.add(entity)


        job.state = "completed"
        db.commit()
        logger.info(f"Job {job_id} completed successfully")

    except Exception as e:
        job.state = "failed"
        job.retries += 1
        db.commit()
        logger.error(f"Job {job_id} failed: {e}")
        raise self.retry(exc=e, countdown=30)

    finally:
        db.close()
