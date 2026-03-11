# app/routers/health.py
from fastapi import APIRouter
from sqlalchemy import text
from ..db import SessionLocal

router = APIRouter(prefix="/health")

@router.get("/")
def health_check():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "details": str(e)}
