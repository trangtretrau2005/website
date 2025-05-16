# backend/app/models/user.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Backend.app.config.database import Base
from Backend.app.models.user_event import UserEvent  # Import bảng liên kết

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # Khóa chính
    name = Column(String(225), index=True)                    # Tên người dùng
    password = Column(String(225))                            # Mật khẩu người dùng

    # Quan hệ nhiều-nhiều với Event thông qua bảng liên kết `user_event`
    events = relationship("Event", secondary="user_event", back_populates="users")
