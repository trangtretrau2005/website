# backend/app/controllers/eventController.py

from fastapi import HTTPException
from Backend.app.models.event import Event
from Backend.app.config.database import SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime
from Backend.app.schemas.event_schema import EventCreateSchema
from Backend.app.models.user_event import UserEvent
from Backend.app.models.event_guest import EventGuest
from Backend.app.models.personnel import Personnel
from Backend.app.models.event_personnel import EventPersonnel



def create_new_event(event_data: EventCreateSchema, user_id: int, db: Session):
    # Kiểm tra trùng tên sự kiện
    existing_event = db.query(Event).filter(Event.name == event_data.name).first()
    if existing_event:
        raise HTTPException(status_code=400, detail="Event with this name already exists")
    
    # Tạo mới sự kiện
    new_event = Event(
        name=event_data.name,
        event_date=event_data.event_date,
        location=event_data.location,
        description=event_data.description,
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    # Luôn thêm vào bảng trung gian user_event
    user_event = UserEvent(user_id=user_id, event_id=new_event.id)
    db.add(user_event)
    db.commit()

    # Trả về dữ liệu chi tiết
    return {
        "message": "Event created and user registered successfully",
        "event": {
            "id": new_event.id,
            "name": new_event.name,
            "event_date": new_event.event_date,
            "description": new_event.description
        }
    }


def delete_event_with_all_relations(event_id: int, db: Session):
    # 1. Kiểm tra sự kiện có tồn tại
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")

    # 2. Xoá liên kết trong user_event
    db.query(UserEvent).filter(UserEvent.event_id == event_id).delete()

    # 3. Xoá event_guest và xoá guests nếu không còn liên kết nào khác
    event_guests = db.query(EventGuest).filter(EventGuest.event_id == event_id).all()
    for eg in event_guests:
        guest_id = eg.guest_id
        db.delete(eg)
        # Kiểm tra guest còn trong sự kiện khác không
        remaining_guest_links = db.query(EventGuest).filter(EventGuest.guest_id == guest_id).count()
        if remaining_guest_links == 0:
            guest = db.query(Guest).filter(Guest.id == guest_id).first()
            if guest:
                db.delete(guest)

    # 4. Xoá event_personnel và xoá personnel nếu không còn liên kết nào khác
    event_personnels = db.query(EventPersonnel).filter(EventPersonnel.event_id == event_id).all()
    for ep in event_personnels:
        personnel_id = ep.personnel_id
        db.delete(ep)
        # Kiểm tra personnel còn trong sự kiện khác không
        remaining_personnel_links = db.query(EventPersonnel).filter(EventPersonnel.personnel_id == personnel_id).count()
        if remaining_personnel_links == 0:
            personnel = db.query(Personnel).filter(Personnel.id == personnel_id).first()
            if personnel:
                db.delete(personnel)

    # 5. Xoá sự kiện
    db.delete(event)
    db.commit()

    return {"message": f"Event ID {event_id} and all related data deleted successfully."}


def update_event_info(event_id: int, event_data: EventCreateSchema, db: Session):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")

    # Cập nhật từng field nếu được truyền
    if event_data.name is not None:
        event.name = event_data.name
    if event_data.event_date is not None:
        event.date = event_data.event_date
    if event_data.description is not None:
        event.description = event_data.description
    if event_data.location is not None:
        event.location = event_data.location

    db.commit()
    db.refresh(event)

    return {"message": "Event updated successfully.", "event": {
        "id": event.id,
        "name": event.name,
        "date": event.date,
        "description": event.description,
        "location": event.location
    }}
