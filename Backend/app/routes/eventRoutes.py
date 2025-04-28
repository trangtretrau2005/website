# backend/app/routes/eventRoutes.py

from fastapi import APIRouter, Depends
from Backend.app.controllers.eventController import create_event, get_events, get_event_by_id
from Backend.app.config.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import HTTPException

router = APIRouter()

# Để lấy kết nối cơ sở dữ liệu cho mỗi yêu cầu
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Tạo sự kiện mới.
@router.post("/create")
async def create_event_route(event_data: dict, db: Session = Depends(get_db)):
    return create_event(event_data, db)
#Lấy danh sách sự kiện.
@router.get("/")
async def get_events_route(db: Session = Depends(get_db)):
    return get_events(db)
#Lấy chi tiết sự kiện theo ID.
@router.get("/{event_id}")
async def get_event_route(event_id: int, db: Session = Depends(get_db)):
    return get_event_by_id(event_id, db)
#Cập nhật sự kiện.
# @router.put("/{event_id}")
# async def update_event_route(event_id: int, event_data: dict, db: Session = Depends(get_db)):
#     return update_event(event_id, event_data, db)
# Xóa sự kiện.
# @router.delete("/{event_id}")
# async def delete_event_route(event_id: int, db: Session = Depends(get_db)):
#     return delete_event(event_id, db)
