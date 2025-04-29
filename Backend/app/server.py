# backend/app/server.py

from fastapi import FastAPI
from Backend.app.routes import eventRoutes, guestroutes, personnelRoutes,userroutes,EventHistoryRoutes
from Backend.app.init import ok

app = FastAPI(debug=True)
ok()
# Kết nối các route vào ứng dụng
app.include_router(eventRoutes.router, prefix="/api/events", tags=["Events"])
app.include_router(guestroutes.router, prefix="/api/guests", tags=["Guests"])
app.include_router(personnelRoutes.router, prefix="/api/personnel", tags=["Personnel"])
app.include_router(userroutes.router, prefix="/api/user", tags=["user"])
app.include_router(EventHistoryRoutes.router, prefix="/api/EventHistory", tags=["EventHistory"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
