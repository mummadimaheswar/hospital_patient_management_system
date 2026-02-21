from pydantic import BaseModel, EmailStr
from datetime import date
from enum import Enum
from typing import Optional


class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: Gender
    phone: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    blood_group: Optional[str] = None


class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    blood_group: Optional[str] = None


class PatientOut(PatientCreate):
    id: int

    model_config = {"from_attributes": True}
