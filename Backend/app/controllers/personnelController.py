# backend/app/controllers/personnelController.py
import re
from fastapi import HTTPException
from Backend.app.models.personnel import Personnel
from Backend.app.config.database import SessionLocal
from sqlalchemy.orm import Session


# # Thêm nhân sự vào sự kiện
# def add_personnel_to_event(personnel_data: dict, db: Session):
#     personnel = Personnel(
#         name=personnel_data['name'],
#         student_code=personnel_data['student_code'],
#         role=personnel_data['role'],
#         event_id=personnel_data['event_id']
#     )
#     db.add(personnel)
#     db.commit()
#     db.refresh(personnel)

#     return personnel

def add_personnel_to_event(personnel_data: dict, db: Session):
    student_code = personnel_data.get('student_code', '')

    # Kiểm tra mã sinh viên hợp lệ: 3 chữ cái đầu + 4 số cuối
    if not re.fullmatch(r'[A-Za-z]{3}\d{4}', student_code):
        raise HTTPException(status_code=422, detail="Mã sinh viên không hợp lệ. Phải gồm 3 chữ cái đầu và 4 số cuối.")
    
    # Kiểm tra nhân sự đã tồn tại theo mã sinh viên chưa
    existing_personnel = db.query(Personnel).filter(Personnel.student_code == student_code).first()
    if existing_personnel:
        raise HTTPException(status_code=400, detail="Nhân sự với mã sinh viên này đã tồn tại")
    
    personnel = Personnel(
        name=personnel_data['name'],
        student_code=student_code,
        role=personnel_data['role'],
        event_id=personnel_data['event_id']
    )
    db.add(personnel)
    db.commit()
    db.refresh(personnel)
#     return personnel
# def add_personnel_to_event(personnel_data: dict, db: Session):
#     student_code = personnel_data.get('student_code', '')

#     # Kiểm tra mã sinh viên: 7 ký tự, 3 chữ cái đầu (a-z hoặc A-Z), 4 số cuối
#     if not re.fullmatch(r'[A-Za-z]{3}\d{4}', student_code):
#         return {"error": "Mã sinh viên không hợp lệ. Phải gồm 3 chữ cái đầu và 4 số cuối."}

#     personnel = Personnel(
#         name=personnel_data['name'],
#         student_code=student_code,
#         role=personnel_data['role'],
#         event_id=personnel_data['event_id']
#     )
#     db.add(personnel)
#     db.commit()
#     db.refresh(personnel)

#     return personnel
# Lấy danh sách nhân sự cho sự kiện
def get_personnel_for_event(event_id: int, db: Session):
    personnel = db.query(Personnel).filter(Personnel.event_id == event_id).all()
    return personnel

# Cập nhật thông tin nhân sự trong sự kiện
def update_personnel_to_event(student_code: str, personnel_data: dict, db: Session):
    personnel = db.query(Personnel).filter(Personnel.student_code == student_code).first()
    if not personnel:
        raise HTTPException(status_code=404, detail="Personnel not found")
    
    # Update personnel fields
    for key, value in personnel_data.items():
        setattr(personnel, key, value)
    
    db.commit()
    db.refresh(personnel)
    return personnel

# Xóa nhân sự khỏi sự kiện
def delete_personnel_to_event(student_code: str, db: Session):
    personnel = db.query(Personnel).filter(Personnel.student_code == student_code).first()
    if not personnel:
        raise HTTPException(status_code=404, detail="Personnel not found")
    
    db.delete(personnel)
    db.commit()
    return {"message": "Personnel deleted successfully"}

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
    
#     db.add(personnel)

#     db.commit()
#     return {"message": "Personnel added successfully!"}
