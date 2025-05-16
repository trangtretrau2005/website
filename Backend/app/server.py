# backend/app/server.py

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fastapi import FastAPI
from Backend.app.routes import eventRoutes, guest_routes, personnelRoutes,userroutes,EventHistoryRoutes
# from app.routers import send_invitation  # ✅ Đường dẫn đến file gửi mail
from Backend.app.init import ok
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
ok()
# Kết nối các route vào ứng dụng
app.include_router(eventRoutes.router, prefix="/api/events", tags=["Events"])
app.include_router(guest_routes.router, prefix="/api/guests", tags=["Guests"])
app.include_router(personnelRoutes.router, prefix="/api/personnel", tags=["Personnel"])
app.include_router(userroutes.router, prefix="/api/user", tags=["user"])
app.include_router(EventHistoryRoutes.router, prefix="/api/EventHistory", tags=["EventHistory"])

# ✅ Đăng ký router gửi mail
# app.include_router(send_invitation.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
