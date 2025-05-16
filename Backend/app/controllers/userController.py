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
    events = db.query(Event).join(Event.users).filter(User.id == user.id).all()
    
    return user, events

def create_user_in_db(username: str, password: str, db: Session):
    # Kiểm tra xem người dùng đã tồn tại chưa
    existing_user = db.query(User).filter(User.name == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Tạo người dùng mới
    new_user = User(name=username, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user