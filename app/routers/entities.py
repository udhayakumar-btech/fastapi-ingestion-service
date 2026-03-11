from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import Entity

router = APIRouter(
    prefix="/entities",
    tags=["entities"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_entities(provider: str, db: Session = Depends(get_db)):
    return db.query(Entity).filter(Entity.provider == provider).all()
