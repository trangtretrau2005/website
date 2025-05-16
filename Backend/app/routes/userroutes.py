# backend/app/routes/userRoutes.py

from fastapi import APIRouter, Depends
from Backend.app.controllers.userController import get_user_and_events, create_user_in_db
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


# Tạo class Pydantic để định nghĩa dữ liệu yêu cầu từ body
class LoginRequest(BaseModel):
    username: str
    password: str

class CreateUserRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    username = request.username
    password = request.password
    user, events = get_user_and_events(username, password, db)
    return {
        "user": user.name,
        "events": [{"id": event.id, "name": event.name, "date": event.event_date} for event in events]
    }

#Tạo người dùng mới (đăng ký).
@router.post("/create")
async def create_user(request: CreateUserRequest, db: Session = Depends(get_db)):
    new_user = create_user_in_db(request.username, request.password, db)
    return {"id": new_user.id, "username": new_user.name}

# @router.post("/login")
# def login(username: str, password: str, db: Session = Depends(get_db)):
#     user, events = get_user_and_events(username, password, db)
#     return {
#         "user": user.name,
#         "events": [{"id": event.id, "name": event.name, "date": event.event_date} for event in events]
#     }


# Đăng nhập người dùng.

# @router.post("/login")
# async def login_user(credentials: dict, db: Session = Depends(get_db)):
#     return login_user_in_db(credentials, db)
# #Lấy danh sách sự kiện của người dùng.
# @router.get("/{user_id}/events")
# async def get_user_events(user_id: int, db: Session = Depends(get_db)):
#     return get_user_events_from_db(user_id, db)

