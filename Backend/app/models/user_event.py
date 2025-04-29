from sqlalchemy import Column, Integer, ForeignKey
from Backend.app.config.database import Base

class UserEvent(Base):
    __tablename__ = "user_event"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"), primary_key=True)
    