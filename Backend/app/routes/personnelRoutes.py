# backend/app/routes/personnelRoutes.py

from fastapi import APIRouter, Depends
from Backend.app.controllers.personnelController import add_personnel_to_event, get_personnel_for_event
from Backend.app.config.database import SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#Thêm nhân sự vào sự kiện.
@router.post("/create")
async def add_personnel_route(personnel_data: dict, db: Session = Depends(get_db)):
    return add_personnel_to_event(personnel_data, db)
#Lấy danh sách nhân sự của sự kiện.
@router.get("/event/{event_id}")
async def get_personnel_route(event_id: int, db: Session = Depends(get_db)):
    return get_personnel_for_event(event_id, db)
# #Cập nhật thông tin nhân sự.
# @router.put("/{personnel_id}")
# async def update_personnel_route(personnel_id: int, personnel_data: dict, db: Session = Depends(get_db)):
#     return update_personnel(personnel_id, personnel_data, db)
# #Xóa nhân sự.
# @router.delete("/{personnel_id}")
# async def delete_personnel_route(personnel_id: int, db: Session = Depends(get_db)):
#     return delete_personnel(personnel_id, db)

# #upload file CSV và thêm nhân sự
# @router.post("/upload")
# async def upload_personnel(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     try:
#         contents = await file.read()
#         string_io = StringIO(contents.decode('utf-8'))
        
#         # Kiểm tra header của file CSV (các cột cần có trong file CSV)
#         df = pd.read_csv(string_io)
#         if not all(col in df.columns for col in ['name', 'student_code', 'role', 'event_id']):
#             raise HTTPException(status_code=400, detail="CSV must contain 'name', 'student_code', 'role', 'event_id' columns")
        
#         # Thêm nhân sự từ file CSV
#         return add_personnel_from_csv(string_io, db)
#     except Exception as e:
#         return JSONResponse(status_code=400, content={"message": str(e)})