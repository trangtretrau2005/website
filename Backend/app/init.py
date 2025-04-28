# backend/app/init_db.py

from Backend.app.config.database import engine  # Import engine kết nối cơ sở dữ liệu
from Backend.app.models import user, event, guest, personnel, event_history, event_guest, event_personnel, user_event  # Import các mô hình

def ok():
    # Tạo các bảng trong cơ sở dữ liệu nếu chưa có
    user.Base.metadata.create_all(bind=engine)
    event.Base.metadata.create_all(bind=engine)
    guest.Base.metadata.create_all(bind=engine)
    personnel.Base.metadata.create_all(bind=engine)
    event_history.Base.metadata.create_all(bind=engine)
    event_guest.Base.metadata.create_all(bind=engine)
    event_personnel.Base.metadata.create_all(bind=engine)
    user_event.Base.metadata.create_all(bind=engine)

    print("Các bảng đã được tạo thành công.")
