# backend/app/models/guest.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Backend.app.config.database import Base
from Backend.app.models.event_guest import EventGuest  # Import bảng liên kết

class Guest(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, index=True)  # Khóa chính
    name = Column(String(225))                               # Tên khách mời
    email = Column(String(225), index=True)                  # Email khách mời
    check_status = Column(String(225))                       # Trạng thái phản hồi (Đồng ý/Không đồng ý)

    # Quan hệ nhiều-nhiều với Event thông qua bảng liên kết `event_guest`
    events = relationship("Event", secondary="event_guest", back_populates="guests")
