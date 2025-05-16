# backend/app/models/personnel.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Backend.app.config.database import Base

class Personnel(Base):
    __tablename__ = "personnel"
    __table_args__ = {"extend_existing": True}  # Allow redefinition if the table already exists

    id = Column(Integer, primary_key=True, index=True)  # Khóa chính
    name = Column(String(225))                               # Tên nhân sự
    student_code = Column(String(225))                       # Mã sinh viên
    role = Column(String(225))                               # Vai trò trong sự kiện

    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"))  # Khóa ngoại liên kết với bảng `event`

    # Quan hệ nhiều-nhiều với Event thông qua bảng liên kết `event_personnel`
    events = relationship("Event", secondary="event_personnel", back_populates="personnel")
