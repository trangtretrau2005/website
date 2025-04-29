from pydantic import BaseModel
from typing import List

class PersonnelItem(BaseModel):
    name: str
    student_code: str
    role: str

class AddPersonnelRequest(BaseModel):
    event_id: int
    personnel_list: List[PersonnelItem]

class RemovePersonnelRequest(BaseModel):
    event_id: int
    personnel_id: int