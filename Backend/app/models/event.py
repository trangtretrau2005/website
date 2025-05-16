# backend/app/models/event.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from Backend.app.config.database import Base
from Backend.app.models.user_event import UserEvent  # Import bảng liên kết

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)  # Khóa chính
    name = Column(String(225), index=True)                    # Tên sự kiện
    event_date = Column(DateTime)                        # Ngày giờ sự kiện
    location = Column(String(225))                            # Địa điểm sự kiện
    description = Column(String(225))                         # Mô tả sự kiện

    # Quan hệ với bảng User (nhiều-nhiều qua bảng `user_event`)
    users = relationship("User", secondary="user_event", back_populates="events")
    guests = relationship("Guest", secondary="event_guest", back_populates="events")
    personnel = relationship("Personnel", secondary="event_personnel", back_populates="events")