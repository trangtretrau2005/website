from sqlalchemy import Column, Integer, ForeignKey
from Backend.app.config.database import Base

class EventPersonnel(Base):
    __tablename__ = "event_personnel"

    personnel_id = Column(Integer, ForeignKey("personnel.id"), primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"), primary_key=True)
