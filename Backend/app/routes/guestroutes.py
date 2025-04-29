# backend/app/routes/guestRoutes.py

from fastapi import APIRouter, Depends,Query
from Backend.app.controllers.guestController import  add_guests_to_event,delete_guest_from_event
from Backend.app.config.database import SessionLocal
from sqlalchemy.orm import Session
from Backend.app.schemas.guestSchema import AddGuestsRequest,xoa


router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/add")
def add_guests(data: AddGuestsRequest, db: Session = Depends(get_db)):
    return add_guests_to_event(data, db)


@router.delete("/remove")
def remove_personnel(data: xoa, db: Session = Depends(get_db)):
    return delete_guest_from_event(data, db)