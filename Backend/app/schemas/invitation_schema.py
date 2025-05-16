# app/schemas/invitation_schema.py
from pydantic import BaseModel
from typing import List

class GuestItem(BaseModel):
    ten: str
    email: str
    status: str

class GuestList(BaseModel):
    guests: List[GuestItem]

