# backend/app/models/user_event.py

from sqlalchemy import Column, Integer, ForeignKey
from Backend.app.config.database import Base

class UserEvent(Base):
    __tablename__ = "user_event"

    user_id = Column(Integer, ForeignKey("users.id",  ondelete="CASCADE"), primary_key=True)  # Khóa ngoại đến bảng users
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), primary_key=True)  # Khóa ngoại đến bảng events 