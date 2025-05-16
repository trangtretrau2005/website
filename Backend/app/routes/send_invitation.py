from fastapi import APIRouter
from pydantic import BaseModel
import smtplib

router = APIRouter(prefix="/api", tags=["Gửi mail"])

class Guest(BaseModel):
    ten: str
    email: str
    status: str

class GuestList(BaseModel):
    guests: list[Guest]

@router.post("/send-invitations")
def send_invitations(data: GuestList):
    success = []
    failed = []

    for guest in data.guests:
        try:
            # Soạn nội dung mail
            message = f"""Subject: Lời mời tham dự sự kiện

Xin chào {guest.ten},

Bạn vui lòng xác nhận tham dự bằng cách nhấn:
✅ Đồng ý: http://localhost:3000/respond?status=accept  
❌ Không tham gia: http://localhost:3000/respond?status=decline

Trân trọng,
Ban Tổ Chức"""

            # Gửi mail (ví dụ dùng Gmail)
            smtp = smtplib.SMTP("smtp.gmail.com", 587)
            smtp.starttls()
            smtp.login("YOUR_EMAIL@gmail.com", "APP_PASSWORD")
            smtp.sendmail("YOUR_EMAIL@gmail.com", guest.email, message)
            smtp.quit()
            success.append(guest.email)
        except Exception as e:
            print(f"Error sending to {guest.email}: {e}")
            failed.append(guest.email)

    return {"sent": success, "failed": failed}
