from sqlalchemy import Column, Integer, String, DateTime, func
from Backend.app.config.database import Base  # điều chỉnh đường dẫn nếu cần

class GuestResponse(Base):
    __tablename__ = "guest_responses"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    status = Column(String)  # "Đồng ý", "Không tham gia"
    responded_at = Column(DateTime, default=func.now())

