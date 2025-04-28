# backend/app/models/event_history.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from Backend.app.config.database import Base
from sqlalchemy.orm import relationship

class EventHistory(Base):
    __tablename__ = "event_history"

    id = Column(Integer, primary_key=True, index=True)  # Khóa chính
    event_id = Column(Integer, ForeignKey("events.id"))  # Khóa ngoại liên kết với bảng `event`
    status_change = Column(String(225))                        # Mô tả thay đổi trạng thái
    change_date = Column(DateTime)                        # Ngày giờ thay đổi

    # Quan hệ với bảng Event
    event = relationship("Event", back_populates="event_history")
