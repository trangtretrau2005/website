from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Backend.app.config.database import Base

class Personnel(Base):
    __tablename__ = "personnel"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(225))
    student_code = Column(String(225))
    role = Column(String(225))

    events = relationship("Event", secondary="event_personnel", back_populates="personnel")
