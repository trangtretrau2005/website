from fastapi import HTTPException
from Backend.app.models.personnel import Personnel
from Backend.app.config.database import SessionLocal
from sqlalchemy.orm import Session
from Backend.app.models.user import User
from Backend.app.models.event import Event

def get_user_and_events(username: str, password: str, db: Session):
    # Kiểm tra người dùng trong cơ sở dữ liệu
    user = db.query(User).filter(User.name == username, User.password == password).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found or invalid credentials")
    
    # Lấy danh sách sự kiện của người dùng
    events = db.query(Event).filter(Event.user_id == user.id).all()
    
    return user, events