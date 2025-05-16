from pydantic import BaseModel

class GuestResponseSchema(BaseModel):
    email: str
    status: str

 