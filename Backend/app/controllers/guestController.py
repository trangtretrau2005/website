# backend/app/controllers/guestController.py

from fastapi import HTTPException
from Backend.app.models.guest import Guest
from Backend.app.config.database import SessionLocal
from sqlalchemy.orm import Session

# Thêm khách mời vào sự kiện
def add_guest_to_event(guest_data: dict, db: Session):
    guest = Guest(
        name=guest_data['name'],
        email=guest_data['email'],
        check_status=guest_data['check_status'],
        event_id=guest_data['event_id']
    )
    db.add(guest)
    db.commit()
    db.refresh(guest)
    return guest

# Lấy danh sách khách mời của một sự kiện
def get_guests_for_event(event_id: int, db: Session):
    guests = db.query(Guest).filter(Guest.event_id == event_id).all()
    return guests

# backend/app/controllers/guestController.py

# import csv
# from io import StringIO
# from fastapi import HTTPException
# from models.guest import Guest
# from config.database import SessionLocal
# from sqlalchemy.orm import Session

# def add_guests_from_csv(file: StringIO, db: Session):
#     """
#     Hàm này nhận vào file CSV dạng StringIO và thêm khách mời vào cơ sở dữ liệu.
#     """
#     csv_reader = csv.DictReader(file)
    
#     for row in csv_reader:
#         name = row['name']
#         email = row['email']
#         check_status = row['check_status']
#         event_id = int(row['event_id'])  # Cột event_id phải có trong file CSV

#         guest = Guest(
#             name=name,
#             email=email,
#             check_status=check_status,
#             event_id=event_id
#         )
        
#         db.add(guest)
    
#     db.commit()
#     return {"message": "Guests added successfully!"}
