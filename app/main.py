from fastapi import FastAPI
from .routers import jobs, entities, health

app = FastAPI()

app.include_router(jobs.router)
app.include_router(entities.router)
app.include_router(health.router)

#celery -A app.tasks worker --loglevel=info --pool=solo
#python -m uvicorn app.main:app --reload

#*** This will create Ingestion DB ***# #One time to run
#from app.db import Base, engine
#from app import models

#Base.metadata.create_all(bind=engine)
