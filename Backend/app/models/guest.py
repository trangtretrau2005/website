from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Backend.app.config.database import Base

class Guest(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(225))
    email = Column(String(225), index=True)
    check_status = Column(String(225))

    events = relationship("Event", secondary="event_guest", back_populates="guests")
