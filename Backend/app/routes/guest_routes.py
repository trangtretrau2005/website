from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from Backend.app.config.database import SessionLocal
# from Backend.app.schemas.guest_response import GuestResponseSchema
# from Backend.app.models.guest_response import GuestResponse
import smtplib
from email.mime.text import MIMEText

# Import logic controller
from Backend.app.controllers.guestController import (
    add_guest_to_event,
    get_guests_for_event,
    update_guest,
    delete_guest,
)

from Backend.app.controllers.sendMailController import (
    send_invitations,
    respond_to_invitation,
)

router = APIRouter()

# --------------------- ROUTES ---------------------
#  kết nối cơ sở dữ liệu cho mỗi yêu cầu
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add a new guest to an event
@router.post("/create")
async def add_guest_route(guest_data: dict, db: Session = Depends(get_db)):
    return add_guest_to_event(guest_data, db)

# Get all guests for a specific event
@router.get("/event/{event_id}")
async def get_guests_route(event_id: int, db: Session = Depends(get_db)):
    print(f"Fetching guests for event_id: {event_id}")
    return get_guests_for_event(event_id, db)

# Update guest information
@router.put("/update/{guest_id}")
async def update_guest_route(guest_id: int, guest_data: dict, db: Session = Depends(get_db)):
    return update_guest(guest_id, guest_data, db)

# Delete a guest from an event
@router.delete("/delete/{guest_id}")
async def delete_guest_route(guest_id: int, db: Session = Depends(get_db)):
    return delete_guest(guest_id, db)

# Send invitations to a list of guests
@router.post("/send-invitations")
async def send_invitations_route(data: dict, db: Session = Depends(get_db)):
    """
    API endpoint to send email invitations to a list of guests.

    Args:
        data (invitationData): A Pydantic model containing a list of guest IDs and event ID.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: A dictionary containing the status of the email sending process.
    """
    try:
        result = send_invitations(data, db)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/respond")
def respond_to_invitation_route(event_id: int, guest_id: int, status: str, db: Session = Depends(get_db)):
    print(f"Responding to invitation with status: {status} for event_id: {event_id} and guest_id: {guest_id}")
    return respond_to_invitation(event_id, guest_id, status, db)

# @router.put("/guest/{guest_id}")
# async def update_guest_route(guest_id: int, guest_data: GuestSchema, db: Session = Depends(get_db)):
#     return update_guest(guest_id, guest_data.dict(), db)

# @router.post("/guest-response")
# def save_response(data: GuestResponseSchema, db: Session = Depends(get_db)):
#     response = GuestResponse(
#         email=data.email,
#         status=data.status
#     )
#     db.add(response)
#     db.commit()
#     return {"message": "Lưu phản hồi thành công"}

# @router.post("/send-invitations")
# async def send_invitations(data: GuestList):
#     success_count = 0

#     for guest in data.guests:
#         try:
#             subject = "Lời mời tham dự sự kiện"
#             accept_url = f"http://localhost:3000/respond?status=accept&email={guest.email}"
#             decline_url = f"http://localhost:3000/respond?status=decline&email={guest.email}"

#             html = f"""
#                 <p>Xin chào {guest.ten},</p>
#                 <p>Bạn được mời tham dự sự kiện của chúng tôi.</p>
#                 <p>Vui lòng chọn một trong hai tùy chọn dưới đây:</p>
#                 <p>
#                     <a href='{accept_url}'>✅ Tôi đồng ý tham gia</a><br>
#                     <a href='{decline_url}'>❌ Tôi không thể tham gia</a>
#                 </p>
#             """

#             msg = MIMEText(html, 'html')
#             msg['Subject'] = subject
#             msg['From'] = "your_email@gmail.com"
#             msg['To'] = guest.email

#             with smtplib.SMTP("smtp.gmail.com", 587) as server:
#                 server.starttls()
#                 server.login("your_email@gmail.com", "your_app_password")
#                 server.send_message(msg)

#             success_count += 1
#         except Exception as e:
#             print(f"❌ Lỗi gửi email cho {guest.email}: {e}")

#     if success_count == 0:
#         raise HTTPException(status_code=500, detail="Không gửi được email nào")

#     return {"message": f"✅ Đã gửi thành công {success_count} email"}

