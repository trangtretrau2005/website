from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Backend.app.config.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(225), index=True)
    password = Column(String(225))

    events = relationship("Event", secondary="user_event", back_populates="users")
