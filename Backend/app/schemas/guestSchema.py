from pydantic import BaseModel
from typing import List

class GuestInfo(BaseModel):
    name: str
    email: str

class AddGuestsRequest(BaseModel):
    event_id: int
    guests: List[GuestInfo]

class xoa(BaseModel):
    event_id: int
    guest_id: int