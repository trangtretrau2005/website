from pydantic import BaseModel
from datetime import datetime

class EventCreateSchema(BaseModel):
    name: str
    event_date: datetime
    location: str
    description: str
