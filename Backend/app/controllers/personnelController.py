# backend/app/controllers/personnelController.py

from fastapi import HTTPException
from Backend.app.models.personnel import Personnel
from Backend.app.config.database import SessionLocal
from sqlalchemy.orm import Session
from Backend.app.models.event_personnel import EventPersonnel
from Backend.app.models.event import Event


def add_multiple_personnel_to_event(data, db: Session):
    event_id = data.event_id
    personnel_list = data.personnel_list

    added_personnel = []

    for person_data in personnel_list:
        # Kiểm tra xem đã có nhân sự với student_code chưa
        existing_personnel = db.query(Personnel).filter(Personnel.student_code == person_data.student_code).first()

        if existing_personnel:
            # Kiểm tra xem đã liên kết với event chưa
            existing_link = db.query(EventPersonnel).filter(
                EventPersonnel.event_id == event_id,
                EventPersonnel.personnel_id == existing_personnel.id
            ).first()

            if existing_link:
                added_personnel.append({
                    "name": existing_personnel.name,
                    "student_code": existing_personnel.student_code,
                    "role": existing_personnel.role,
                    "status": "Already joined this event"
                })
            else:
                # Nếu chưa có link thì thêm vào event
                event_personnel = EventPersonnel(
                    event_id=event_id,
                    personnel_id=existing_personnel.id
                )
                db.add(event_personnel)
                db.commit()
                added_personnel.append({
                    "name": existing_personnel.name,
                    "student_code": existing_personnel.student_code,
                    "role": existing_personnel.role,
                    "status": "Linked to event successfully"
                })
        else:
            # Nếu chưa tồn tại nhân sự -> tạo mới
            new_personnel = Personnel(
                name=person_data.name,
                student_code=person_data.student_code,
                role=person_data.role
            )
            db.add(new_personnel)
            db.commit()
            db.refresh(new_personnel)

            # Gán nhân sự mới vào sự kiện
            event_personnel = EventPersonnel(
                event_id=event_id,
                personnel_id=new_personnel.id
            )
            db.add(event_personnel)
            db.commit()

            added_personnel.append({
                "name": new_personnel.name,
                "student_code": new_personnel.student_code,
                "role": new_personnel.role,
                "status": "Created and linked to event successfully"
            })

    return {
        "event_id": event_id,
        "personnel_added": added_personnel
    }

def remove_personnel_from_event(data, db: Session):
    event_id = data.event_id
    personnel_id = data.personnel_id

    # 1. Xóa bản ghi trong event_personnel
    event_personnel = db.query(EventPersonnel).filter(
        EventPersonnel.event_id == event_id,
        EventPersonnel.personnel_id == personnel_id
    ).first()

    if not event_personnel:
        raise HTTPException(status_code=404, detail="Personnel not linked to this event")

    db.delete(event_personnel)
    db.commit()

    # 2. Xóa nhân sự trong personnel
    personnel = db.query(Personnel).filter(Personnel.id == personnel_id).first()

    if personnel:
        db.delete(personnel)
        db.commit()

    return {
        "message": "Personnel removed from event and deleted successfully",
        "personnel_id": personnel_id,
        "event_id": event_id
    }
