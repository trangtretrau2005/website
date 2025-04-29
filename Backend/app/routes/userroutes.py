# backend/app/routes/userRoutes.py

from fastapi import APIRouter, Depends
from Backend.app.controllers.userController import register_user,login_and_get_user_events
from Backend.app.config.database import SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel

router = APIRouter()

# Để lấy kết nối cơ sở dữ liệu cho mỗi yêu cầu
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class RegisterRequest(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    return register_user(request.username, request.password, db)
@router.post("/log")
async def log(request: RegisterRequest, db: Session = Depends(get_db)):
    return login_and_get_user_events(request.username, request.password, db)

