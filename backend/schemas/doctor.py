from pydantic import BaseModel, EmailStr
from typing import Optional


class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    specialization: str
    phone: str
    email: Optional[EmailStr] = None
    available_days: Optional[str] = None


class DoctorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    specialization: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    available_days: Optional[str] = None


class DoctorOut(DoctorCreate):
    id: int

    model_config = {"from_attributes": True}
