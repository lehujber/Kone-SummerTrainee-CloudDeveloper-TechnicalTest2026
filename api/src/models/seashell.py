from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class SeashellBase(BaseModel):
    name: str = Field(..., min_length=1)
    species: str = Field(..., min_length=1)
    description: Optional[str] = None
    personal_notes: Optional[str] = None
    date_found: Optional[date] = None

class SeashellCreate(SeashellBase):
    pass

class SeashellUpdate(SeashellBase):
    pass