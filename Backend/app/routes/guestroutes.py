# backend/app/routes/guestRoutes.py

from fastapi import APIRouter, Depends
from Backend.app.controllers.guestController import add_guest_to_event, get_guests_for_event
from Backend.app.config.database import SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Thêm khách mời vào sự kiện.
@router.post("/create")
async def add_guest_route(guest_data: dict, db: Session = Depends(get_db)):
    return add_guest_to_event(guest_data, db)
#Lấy danh sách khách mời của sự kiện.
@router.get("/event/{event_id}")
async def get_guests_route(event_id: int, db: Session = Depends(get_db)):
    return get_guests_for_event(event_id, db)
#Cập nhật trạng thái phản hồi của khách mời.
@router.put("/{guest_id}")
async def update_guest_status(guest_id: int, check_status: str, db: Session = Depends(get_db)):
    return update_guest_status(guest_id, check_status, db)
# Xóa khách mời.
# @router.delete("/{guest_id}")
# async def delete_guest_route(guest_id: int, db: Session = Depends(get_db)):
#     return delete_guest(guest_id, db)

#  để upload file CSV và thêm khách mời
# @router.post("/upload")
# async def upload_guests(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     try:
#         contents = await file.read()
#         string_io = StringIO(contents.decode('utf-8'))
        
#         # Kiểm tra header của file CSV (các cột cần có trong file CSV)
#         df = pd.read_csv(string_io)
#         if not all(col in df.columns for col in ['name', 'email', 'check_status', 'event_id']):
#             raise HTTPException(status_code=400, detail="CSV must contain 'name', 'email', 'check_status', 'event_id' columns")
        
#         # Thêm khách mời từ file CSV
#         return add_guests_from_csv(string_io, db)
#     except Exception as e:
#         return JSONResponse(status_code=400, content={"message": str(e)})