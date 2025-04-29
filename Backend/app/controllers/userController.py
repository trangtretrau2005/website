from fastapi import HTTPException
from sqlalchemy.orm import Session
from Backend.app.models.user import User
from fastapi import HTTPException
from Backend.app.models.user_event import UserEvent
from Backend.app.models.event import Event


def register_user(username: str, password: str, db: Session):
    # Kiểm tra xem username đã tồn tại chưa
    existing_user = db.query(User).filter(User.name == username).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists.")
    
    # Tạo user mới
    new_user = User(name=username, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # cập nhật lại đối tượng new_user
    
    return {"message": "User registered successfully.", "user_id": new_user.id}


def login_and_get_user_events(username: str, password: str, db: Session):
    # Kiểm tra người dùng có tồn tại
    user = db.query(User).filter(User.name == username, User.password == password).first()
    if not user:
        raise HTTPException(status_code=404, detail="No user found. Please register first.")

    # Lấy danh sách event_id từ bảng trung gian UserEvent
    user_event_ids = db.query(UserEvent.event_id).filter(UserEvent.user_id == user.id).all()
    event_ids = [eid for (eid,) in user_event_ids]  # chuyển [(1,), (2,), ...] -> [1, 2, ...]

    # Truy vấn bảng Event để lấy thông tin chi tiết
    events = db.query(Event).filter(Event.id.in_(event_ids)).all()

    event_list = [
        {
            "id": event.id,
            "name": event.name,
            "event_date": event.event_date,
            "location": event.location,
            "description": event.description
        }
        for event in events
    ]

    return {
        "username": user.name,
        "events": event_list
    }
