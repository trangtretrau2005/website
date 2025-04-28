# backend/app/controllers/personnelController.py

from fastapi import HTTPException
from Backend.app.models.personnel import Personnel
from Backend.app.config.database import SessionLocal
from sqlalchemy.orm import Session

# Thêm nhân sự vào sự kiện
def add_personnel_to_event(personnel_data: dict, db: Session):
    personnel = Personnel(
        name=personnel_data['name'],
        student_code=personnel_data['student_code'],
        role=personnel_data['role'],
        event_id=personnel_data['event_id']
    )
    db.add(personnel)
    db.commit()
    db.refresh(personnel)
    return personnel

# Lấy danh sách nhân sự cho sự kiện
def get_personnel_for_event(event_id: int, db: Session):
    personnel = db.query(Personnel).filter(Personnel.event_id == event_id).all()
    return personnel

# # backend/app/controllers/personnelController.py

# import csv
# from io import StringIO
# from fastapi import HTTPException
# from models.personnel import Personnel
# from config.database import SessionLocal
# from sqlalchemy.orm import Session

# def add_personnel_from_csv(file: StringIO, db: Session):
#     """
#     Hàm này nhận vào file CSV dạng StringIO và thêm nhân sự vào cơ sở dữ liệu.
#     """
#     csv_reader = csv.DictReader(file)
    
#     for row in csv_reader:
#         name = row['name']
#         student_code = row['student_code']
#         role = row['role']
#         event_id = int(row['event_id'])  # Cột event_id phải có trong file CSV

#         personnel = Personnel(
#             name=name,
#             student_code=student_code,
#             role=role,
#             event_id=event_id
#         )
        
#         db.add(personnel)
    
#     db.commit()
#     return {"message": "Personnel added successfully!"}
