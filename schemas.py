from pydantic import BaseModel, EmailStr
from datetime import datetime

class FitnessClassOut(BaseModel):
    id: int
    name: str
    datetime: datetime
    instructor: str
    available_slots: int
    class Config:
        orm_mode = True

class BookingRequest(BaseModel):
    class_id: int
    client_name: str
    client_email: EmailStr

class BookingOut(BaseModel):
    id: int
    class_id: int
    client_name: str
    client_email: EmailStr
    class Config:
        orm_mode = True
