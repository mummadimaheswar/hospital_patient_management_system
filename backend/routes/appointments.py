from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models.appointment import Appointment
from backend.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentOut
from backend.auth.auth import get_current_user

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("/", response_model=AppointmentOut, status_code=status.HTTP_201_CREATED)
def create_appointment(appt_in: AppointmentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    appt = Appointment(**appt_in.model_dump())
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt


@router.get("/", response_model=List[AppointmentOut])
def list_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Appointment).offset(skip).limit(limit).all()


@router.get("/{appointment_id}", response_model=AppointmentOut)
def get_appointment(appointment_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt


@router.get("/patient/{patient_id}", response_model=List[AppointmentOut])
def get_appointments_by_patient(patient_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Appointment).filter(Appointment.patient_id == patient_id).all()


@router.put("/{appointment_id}", response_model=AppointmentOut)
def update_appointment(appointment_id: int, appt_in: AppointmentUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    for field, value in appt_in.model_dump(exclude_unset=True).items():
        setattr(appt, field, value)
    db.commit()
    db.refresh(appt)
    return appt


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(appt)
    db.commit()
