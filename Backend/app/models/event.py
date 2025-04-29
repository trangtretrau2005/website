from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from Backend.app.config.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(225), index=True)
    event_date = Column(DateTime)
    location = Column(String(225))
    description = Column(String(225))

    users = relationship("User", secondary="user_event", back_populates="events")
    guests = relationship("Guest", secondary="event_guest", back_populates="events")
    personnel = relationship("Personnel", secondary="event_personnel", back_populates="events")
