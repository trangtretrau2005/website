# backend/app/models/event_guest.py
from sqlalchemy import Column, Integer, String, ForeignKey
from Backend.app.config.database import Base

class EventGuest(Base):
    __tablename__ = "event_guest"

    guest_id = Column(Integer, ForeignKey("guests.id",  ondelete="CASCADE"), primary_key=True)  # Khóa ngoại đến bảng guests
    event_id = Column(Integer, ForeignKey("events.id",  ondelete="CASCADE"), primary_key=True)  # Khóa ngoại đến bảng events
    response_status = Column(String(225))  # Trạng thái phản hồi (Đồng ý/Không đồng ý/ Chưa phản hồi)
