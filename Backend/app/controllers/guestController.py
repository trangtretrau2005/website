from fastapi import HTTPException
from Backend.app.models.guest import Guest
from Backend.app.models.event_guest import EventGuest
from Backend.app.config.database import SessionLocal
from sqlalchemy.orm import Session

# Thêm khách mời vào sự kiện
def add_guest_to_event(guest_data: dict, db: Session):
    # Check if a guest with the same email and event_id already exists
    existing_guest = db.query(Guest).join(EventGuest).filter(
        Guest.email == guest_data['email'],
        EventGuest.event_id == guest_data['event_id']
    ).first()

    if existing_guest:
        raise HTTPException(
            status_code=400,
            detail="Guest with the same email already exists for this event."
        )

    # Add the guest to the `guests` table
    guest = Guest(
        name=guest_data['name'],
        email=guest_data['email'],
    )
    db.add(guest)
    db.commit()
    db.refresh(guest)

    # Add the guest-event relationship to the `event_guest` table
    event_guest = EventGuest(
        guest_id=guest.id,
        event_id=guest_data['event_id'],
        response_status="Chưa phản hồi"  # Default value
    )
    db.add(event_guest)
    db.commit()

    return {"message": "Guest added successfully!"}

# Lấy danh sách khách mời của một sự kiện
def get_guests_for_event(event_id: int, db: Session):
    # Query the EventGuest table to get guests and their response_status for the given event_id
    guests = (
        db.query(EventGuest.guest_id, Guest.name, Guest.email, EventGuest.response_status)
        .join(EventGuest, Guest.id == EventGuest.guest_id)
        .filter(EventGuest.event_id == event_id)
        .all()
    )

    # Map the results to a list of dictionaries
    result = [
        {
            "id": guest.guest_id,
            "name": guest.name,
            "email": guest.email,
            "response_status": guest.response_status,
        }
        for guest in guests
    ]

    return result

# Cập nhật thông tin khách mời
def update_guest(guest_id: int, guest_data: dict, db: Session):
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    
    # Update guest fields
    for key, value in guest_data.items():
        setattr(guest, key, value)
    
    db.commit()
    db.refresh(guest)
    return guest

# Xóa khách mời khỏi sự kiện
def delete_guest(guest_id: int, db: Session):
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    
    db.delete(guest)
    db.commit()
    return {"message": "Guest deleted successfully"}

# Cập nhật thông tin khách mời
# def update_guest(guest_id: int, guest_data: dict, db: Session):
#     guest = db.query(Guest).filter(Guest.id == guest_id).first()
#     if guest is None:
#         raise HTTPException(status_code=404, detail="Guest not found")
    
#     # Cập nhật thông tin khách mời
#     for key, value in guest_data.items():
#         setattr(guest, key, value)
    
#     db.commit()
#     db.refresh(guest)
#     return guest
# backend/app/controllers/guestController.py

# import csv
# from io import StringIO
# from fastapi import HTTPException
# from models.guest import Guest
# from config.database import SessionLocal
# from sqlalchemy.orm import Session

# def add_guests_from_csv(file: StringIO, db: Session):
#     """
# #     Hàm này nhận vào file CSV dạng StringIO và thêm khách mời vào cơ sở dữ liệu.
# #     """
#     csv_reader = csv.DictReader(file)

#     for row in csv_reader:
#         name = row['name']
#         email = row['email']
#         check_status = row['check_status']
#         event_id = int(row['event_id'])  # Cột event_id phải có trong file CSV

#     guest = Guest(
#             name=name,
#             email=email,
#             check_status=check_status,
#             event_id=event_id
#         )
    
#         db.add(guest)

#     db.commit()
#     return {"message": "Guests added successfully!"}
