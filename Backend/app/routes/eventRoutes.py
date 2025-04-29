# backend/app/routes/eventRoutes.py

from fastapi import APIRouter, Depends
from Backend.app.controllers.eventController import update_event_info,create_new_event,delete_event_with_all_relations
from Backend.app.config.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from pydantic import BaseModel
from Backend.app.schemas.event_schema import EventCreateSchema

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API tạo sự kiện mới
@router.post("/create")
async def create_event_route(
    user_id: int,
    event_data: EventCreateSchema,
    db: Session = Depends(get_db)
):
    return create_new_event(event_data, user_id, db)

@router.delete("/event/delete}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    return delete_event_with_all_relations(event_id, db)

@router.put("/update}")
def update_event(event_id: int, event_data: EventCreateSchema, db: Session = Depends(get_db)):
    return update_event_info(event_id, event_data, db)