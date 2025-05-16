import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
from sqlalchemy.orm import Session
from Backend.app.models.guest import Guest
from Backend.app.models.event import Event
from Backend.app.models.event_guest import EventGuest
from fastapi.responses import HTMLResponse

FROM_EMAIL = "thuychi1112005@gmail.com"
PASSWORD = "uhei dtds hdjs dpgp"
# Dynamically set BASE_URL based on environment variable or default to localhost
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:3000")

def send_invitations(invidationData: dict, db: Session):
    guest_ids = invidationData.get("guest_ids")
    event_id = invidationData.get("event_id")
    # Query the database to get event details
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found for the provided ID.")
    # Query the database to get guest details
    guests = db.query(Guest).filter(Guest.id.in_(guest_ids)).all()

    if not guests:
        raise HTTPException(status_code=404, detail="No guests found for the provided IDs.")

    formatted_event_date = event.event_date.strftime("%H:%M %d/%m/%Y") if event.event_date else "N/A"

    success_count = 0
    failure_count = 0
    failed_emails = []

    for guest in guests:
        try:
            # Generate accept and decline links
            accept_link = f"{BASE_URL}/api/guests/respond?status=accept&guest_id={guest.id}&event_id={event.id}"
            decline_link = f"{BASE_URL}/api/guests/respond?status=decline&guest_id={guest.id}&event_id={event.id}"

            # Compose the HTML email content
            html = f"""
            <html>
              <body>
                <p>Xin chào {guest.name},</p>
                <p>Bạn có đồng ý tham gia sự kiện {event.name} sắp diễn ra vào {formatted_event_date} tại {event.location} không?</p>
                <p>
                  <a href="{accept_link}" style="padding:10px 20px; background:#10b981; color:white; text-decoration:none; border-radius:5px;">Đồng ý</a>
                  &nbsp;
                  <a href="{decline_link}" style="padding:10px 20px; background:#ef4444; color:white; text-decoration:none; border-radius:5px;">Không tham gia</a>
                </p>
                <br/>
                <p>Trân trọng,</p>
                <p>Ban Tổ Chức</p>
              </body>
            </html>
            """

            # Configure the email
            msg = MIMEMultipart("alternative")
            msg["Subject"] = "Thư mời tham dự sự kiện"
            msg["From"] = FROM_EMAIL
            msg["To"] = guest.email
            msg.attach(MIMEText(html, "html"))

            # Send the email
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.ehlo()
                server.starttls()
                server.login(FROM_EMAIL, PASSWORD)
                server.sendmail(FROM_EMAIL, guest.email, msg.as_string())
                success_count += 1
        except Exception as e:
            failure_count += 1
            failed_emails.append({"email": guest.email, "error": str(e)})

    return {
        "success_count": success_count,
        "failure_count": failure_count,
        "failed_emails": failed_emails,
    }

def respond_to_invitation(event_id: int, guest_id: int, status: str, db: Session):
    # Check if the guest exists in the database
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found.")

    # Check if the event exists in the database
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")

    # Update the response_status in EventGuest table
    event_guest = db.query(EventGuest).filter(
        EventGuest.guest_id == guest_id,
        EventGuest.event_id == event_id
    ).first()
    if not event_guest:
        raise HTTPException(status_code=404, detail="EventGuest record not found.")
    if status == "accept":
        event_guest.response_status = "Đồng ý"
        message = "Cảm ơn bạn đã xác nhận tham gia sự kiện!"
        color = "#10b981"
    elif status == "decline":
        event_guest.response_status = "Không đồng ý"
        message = "Bạn đã từ chối tham gia sự kiện. Cảm ơn bạn đã phản hồi!"
        color = "#ef4444"
    else:
        raise HTTPException(status_code=400, detail="Invalid status.")

    db.commit()

    html_content = f"""
    <html>
      <head>
        <title>Phản hồi thư mời</title>
      </head>
      <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
        <div style="display: inline-block; padding: 30px 50px; border-radius: 10px; background: {color}; color: white;">
          <h2>{message}</h2>
        </div>
      </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)