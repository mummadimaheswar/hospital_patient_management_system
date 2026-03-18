from pydantic import BaseModel
from typing import Union, Optional
from datetime import date, time

class Patient_details(BaseModel):
    patient_id: int
    patient_name: str
    patient_age: int
    disease: str
    admission_date: Union[str, date, time]

class Patient_update(BaseModel):
    patient_name: Optional[str] = None
    patient_age: Optional[int] = None
    disease: Optional[str] = None
    admission_date: Optional[Union[str, date, time]] = None

class Doctor_details(BaseModel):
    name: str
    specialization: str
    phone: str
    availability: str

class Doctor_update(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    phone: Optional[str] = None
    availability: Optional[str] = None

class MedicalRecord_details(BaseModel):
    patient_id: int
    diagnosis: str
    prescription: str
    visit_date: Union[str, date]

class MedicalRecord_update(BaseModel):
    patient_id: Optional[int] = None
    diagnosis: Optional[str] = None
    prescription: Optional[str] = None
    visit_date: Optional[Union[str, date]] = None

class Bill_details(BaseModel):
    patient_id: int
    amount: float
    payment_status: str
    bill_date: Union[str, date]

class Bill_update(BaseModel):
    patient_id: Optional[int] = None
    amount: Optional[float] = None
    payment_status: Optional[str] = None
    bill_date: Optional[Union[str, date]] = None