from sqlalchemy import Column, Integer, ForeignKey
from Backend.app.config.database import Base

class EventGuest(Base):
    __tablename__ = "event_guest"

    guest_id = Column(Integer, ForeignKey("guests.id"), primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"), primary_key=True)
    