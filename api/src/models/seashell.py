from pydantic import BaseModel
from datetime import date
from typing import Optional

class SeashellBase(BaseModel):
    name: str
    species: str
    description: Optional[str] = None
    personal_notes: Optional[str] = None
    date_found: Optional[date] = None

class SeashellCreate(SeashellBase):
    pass

class SeashellUpdate(SeashellBase):
    pass