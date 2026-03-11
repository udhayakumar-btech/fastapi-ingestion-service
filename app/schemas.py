from pydantic import BaseModel
from typing import Dict

class EntitySchema(BaseModel):
    provider: str
    external_id: str
    normalized: Dict
    derived_field: str
