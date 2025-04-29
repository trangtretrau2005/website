# backend/app/routes/personnelRoutes.py

from fastapi import APIRouter, Depends
from Backend.app.controllers.personnelController import add_multiple_personnel_to_event,remove_personnel_from_event
from Backend.app.config.database import SessionLocal
from sqlalchemy.orm import Session
from Backend.app.schemas.personnelSchema import AddPersonnelRequest,RemovePersonnelRequest


router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("create new personel")
def add_multiple_personnel(data: AddPersonnelRequest, db: Session = Depends(get_db)):
    return add_multiple_personnel_to_event(data, db)

@router.delete("/remove")
def remove_personnel(data: RemovePersonnelRequest, db: Session = Depends(get_db)):
    return remove_personnel_from_event(data, db)