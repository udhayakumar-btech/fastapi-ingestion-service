from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import Job
from ..tasks import ingest_job

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

VALID_PROVIDERS = {"api1", "api2", "api3"}

@router.post("/ingest")
def start_job(providers: list[str], db: Session = Depends(get_db)):
    for p in providers:
        if p not in VALID_PROVIDERS:
            raise HTTPException(status_code=400, detail=f"Invalid provider: {p}")
    job = Job(state="pending")
    db.add(job)
    db.commit()
    ingest_job.delay(job.id, providers)
    return {"job_id": job.id}

@router.get("/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"state": job.state}
