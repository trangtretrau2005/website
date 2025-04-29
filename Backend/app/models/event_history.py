from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from Backend.app.config.database import Base

class EventHistory(Base):
    __tablename__ = "event_history"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    status_change = Column(String(225))
    change_date = Column(DateTime)

    event = relationship("Event", backref="event_history")
