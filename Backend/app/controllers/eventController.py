# backend/app/controllers/eventController.py

from fastapi import HTTPException
from Backend.app.models.event import Event
from Backend.app.config.database import SessionLocal
from sqlalchemy.orm import Session

# Tạo sự kiện mới
def create_event(event_data: dict, db: Session):
    event = Event(
        name=event_data['name'],
        event_date=event_data['event_date'],
        location=event_data['location'],
        description=event_data['description'],
        user_id=event_data['user_id']  # giả sử user_id được cung cấp từ frontend
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

# Lấy danh sách sự kiện
def get_events(db: Session):
    events = db.query(Event).all()
    return events

# Tìm sự kiện theo ID
def get_event_by_id(event_id: int, db: Session):
    event = db.query(Event).filter(Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
