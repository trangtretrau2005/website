from fastapi import APIRouter, Depends
from Backend.app.config.database import SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()

# Để lấy kết nối cơ sở dữ liệu cho mỗi yêu cầu
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#Lấy lịch sử thay đổi của sự kiện.
@router.get("/{event_id}")
async def get_event_history(event_id: int, db: Session = Depends(get_db)):
    return get_event_history(event_id, db)


