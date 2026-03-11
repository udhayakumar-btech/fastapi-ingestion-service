# app/models.py
from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    state = Column(String, default="pending")
    retries = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class RawEvent(Base):
    __tablename__ = "raw_events"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    provider = Column(String)
    payload = Column(JSON)
    job = relationship("Job")

class Entity(Base):
    __tablename__ = "entities"
    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String)
    external_id = Column(String, index=True)
    normalized = Column(JSON)
    derived_field = Column(String)
