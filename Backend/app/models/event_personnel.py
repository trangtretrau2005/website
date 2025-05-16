# backend/app/models/event_personnel.py

from sqlalchemy import Column, Integer, ForeignKey
from Backend.app.config.database import Base

class EventPersonnel(Base):
    __tablename__ = "event_personnel"

    personnel_id = Column(Integer, ForeignKey("personnel.id", ondelete="CASCADE"), primary_key=True)  # Khóa ngoại đến bảng personnel
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), primary_key=True)  # Khóa ngoại đến bảng events
