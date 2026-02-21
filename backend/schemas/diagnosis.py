from pydantic import BaseModel
from datetime import date
from typing import Optional


class DiagnosisCreate(BaseModel):
    appointment_id: int
    patient_id: int
    doctor_id: int
    diagnosis_date: date
    description: str
    prescription: Optional[str] = None
    notes: Optional[str] = None


class DiagnosisUpdate(BaseModel):
    description: Optional[str] = None
    prescription: Optional[str] = None
    notes: Optional[str] = None


class DiagnosisOut(DiagnosisCreate):
    id: int

    model_config = {"from_attributes": True}
