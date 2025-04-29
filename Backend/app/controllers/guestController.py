# backend/app/controllers/guestController.py

from fastapi import HTTPException
from Backend.app.models.guest import Guest
from Backend.app.config.database import SessionLocal
from sqlalchemy.orm import Session
from Backend.app.models.event_guest import EventGuest
from Backend.app.models.guest import Guest
from Backend.app.schemas.guestSchema import AddGuestsRequest,xoa
from Backend.app.models.event import Event


def add_guests_to_event(data: AddGuestsRequest, db: Session):
    event_id = data.event_id
    guest_infos = data.guests

    # Kiểm tra event có tồn tại không
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail=f"Event with ID {event_id} not found.")

    added_guests = []

    for guest_data in guest_infos:
        # Kiểm tra email đã tồn tại chưa
        existing_guest = db.query(Guest).filter(Guest.email == guest_data.email).first()

        if existing_guest:
            # Nếu email đã tồn tại thì BỎ QUA, KHÔNG làm gì cả
            continue

        # Nếu email chưa tồn tại, tạo mới Guest
        new_guest = Guest(
            name=guest_data.name,
            email=guest_data.email,
            check_status="0"  # Luôn set bằng "0"
        )
        db.add(new_guest)
        db.commit()
        db.refresh(new_guest)

        # Sau đó thêm liên kết vào bảng event_guest
        event_guest = EventGuest(
            event_id=event_id,
            guest_id=new_guest.id
        )
        db.add(event_guest)
        db.commit()

        # Đưa vào danh sách trả về
        added_guests.append({
            "id": new_guest.id,
            "name": new_guest.name,
            "email": new_guest.email
        })

    if not added_guests:
        raise HTTPException(status_code=400, detail="No new guests were added. All emails already exist.")

    return {
        "message": "Guests added successfully",
        "guests": added_guests
    }
def delete_guest_from_event(data: xoa, db: Session):
    # 1. Xóa record trong bảng event_guest
    event_guest = db.query(EventGuest).filter(
        EventGuest.event_id == data.event_id,
        EventGuest.guest_id == data.guest_id
    ).first()

    if not event_guest:
        raise HTTPException(status_code=404, detail="Guest not linked to this event.")

    db.delete(event_guest)
    db.commit()

    # 2. Xóa record trong bảng guests
    guest = db.query(Guest).filter(Guest.id == data.guest_id).first()

    if guest:
        db.delete(guest)
        db.commit()

    return {"message": "Guest deleted successfully from event and system."}
