from pydantic import BaseModel
from typing import Union, Optional
from datetime import date, time

# Used when CREATING patient (POST)
class Patient_details(BaseModel):
    patient_id: int
    patient_name: str
    patient_age: int
    disease: str
    admission_date: Union[str, date, time]

# Used when UPDATING patient (PATCH) — all fields optional
class Patient_update(BaseModel):
    patient_name: Optional[str] = None
    patient_age: Optional[int] = None
    disease: Optional[str] = None
    admission_date: Optional[Union[str, date, time]] = None