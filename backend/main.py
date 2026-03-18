from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from database import create_db_and_tables, get_session
from database_model import Patient, Doctor, MedicalRecord, Bill
from models import (
    Patient_details, Patient_update,
    Doctor_details, Doctor_update,
    MedicalRecord_details, MedicalRecord_update,
    Bill_details, Bill_update,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "Welcome to Hospital Patient Management System"}

@app.get("/patients/")
def get_all_patients(session: Session = Depends(get_session)):
    patients = session.query(Patient).all()
    return patients

@app.get("/patients/{patient_id}")
def get_patient(patient_id: int, session: Session = Depends(get_session)):
    patient = session.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.post("/patients/")
def create_patient(patient: Patient_details, session: Session = Depends(get_session)):
    existing = session.query(Patient).filter(Patient.patient_id == patient.patient_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    admission = patient.admission_date if isinstance(patient.admission_date, str) else str(patient.admission_date)
    db_patient = Patient(
        patient_id=patient.patient_id,
        patient_name=patient.patient_name,
        patient_age=patient.patient_age,
        disease=patient.disease,
        admission_date=admission,
    )
    session.add(db_patient)
    session.commit()
    session.refresh(db_patient)
    return db_patient

@app.patch("/patients/{patient_id}")
def update_patient(patient_id: int, patient: Patient_update, session: Session = Depends(get_session)):
    db_patient = session.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    update_data = patient.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "admission_date" and value is not None and not isinstance(value, str):
            value = str(value)
        setattr(db_patient, key, value)
    session.commit()
    session.refresh(db_patient)
    return db_patient

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, session: Session = Depends(get_session)):
    patient = session.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    session.delete(patient)
    session.commit()
    return {"message": f"Patient {patient_id} deleted successfully"}


@app.get("/doctors/")
def get_all_doctors(session: Session = Depends(get_session)):
    return session.query(Doctor).all()

@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int, session: Session = Depends(get_session)):
    doctor = session.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@app.post("/doctors/")
def create_doctor(doctor: Doctor_details, session: Session = Depends(get_session)):
    db_doctor = Doctor(
        name=doctor.name,
        specialization=doctor.specialization,
        phone=doctor.phone,
        availability=doctor.availability,
    )
    session.add(db_doctor)
    session.commit()
    session.refresh(db_doctor)
    return db_doctor

@app.patch("/doctors/{doctor_id}")
def update_doctor(doctor_id: int, doctor: Doctor_update, session: Session = Depends(get_session)):
    db_doctor = session.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    for key, value in doctor.model_dump(exclude_unset=True).items():
        setattr(db_doctor, key, value)
    session.commit()
    session.refresh(db_doctor)
    return db_doctor

@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int, session: Session = Depends(get_session)):
    doctor = session.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    session.delete(doctor)
    session.commit()
    return {"message": f"Doctor {doctor_id} deleted successfully"}

@app.get("/records/")
def get_all_records(session: Session = Depends(get_session)):
    return session.query(MedicalRecord).all()

@app.get("/records/{record_id}")
def get_record(record_id: int, session: Session = Depends(get_session)):
    rec = session.query(MedicalRecord).filter(MedicalRecord.record_id == record_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Record not found")
    return rec

@app.get("/records/patient/{patient_id}")
def get_records_by_patient(patient_id: int, session: Session = Depends(get_session)):
    return session.query(MedicalRecord).filter(MedicalRecord.patient_id == patient_id).all()

@app.post("/records/")
def create_record(record: MedicalRecord_details, session: Session = Depends(get_session)):
    patient = session.query(Patient).filter(Patient.patient_id == record.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    visit = record.visit_date if isinstance(record.visit_date, str) else str(record.visit_date)
    db_rec = MedicalRecord(
        patient_id=record.patient_id,
        diagnosis=record.diagnosis,
        prescription=record.prescription,
        visit_date=visit,
    )
    session.add(db_rec)
    session.commit()
    session.refresh(db_rec)
    return db_rec

@app.patch("/records/{record_id}")
def update_record(record_id: int, record: MedicalRecord_update, session: Session = Depends(get_session)):
    db_rec = session.query(MedicalRecord).filter(MedicalRecord.record_id == record_id).first()
    if not db_rec:
        raise HTTPException(status_code=404, detail="Record not found")
    for key, value in record.model_dump(exclude_unset=True).items():
        if key == "visit_date" and value is not None and not isinstance(value, str):
            value = str(value)
        setattr(db_rec, key, value)
    session.commit()
    session.refresh(db_rec)
    return db_rec

@app.delete("/records/{record_id}")
def delete_record(record_id: int, session: Session = Depends(get_session)):
    rec = session.query(MedicalRecord).filter(MedicalRecord.record_id == record_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Record not found")
    session.delete(rec)
    session.commit()
    return {"message": f"Record {record_id} deleted successfully"}

@app.get("/bills/")
def get_all_bills(session: Session = Depends(get_session)):
    return session.query(Bill).all()

@app.get("/bills/{bill_id}")
def get_bill(bill_id: int, session: Session = Depends(get_session)):
    bill = session.query(Bill).filter(Bill.bill_id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill

@app.get("/bills/patient/{patient_id}")
def get_bills_by_patient(patient_id: int, session: Session = Depends(get_session)):
    return session.query(Bill).filter(Bill.patient_id == patient_id).all()

@app.post("/bills/")
def create_bill(bill: Bill_details, session: Session = Depends(get_session)):
    patient = session.query(Patient).filter(Patient.patient_id == bill.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    bdate = bill.bill_date if isinstance(bill.bill_date, str) else str(bill.bill_date)
    db_bill = Bill(
        patient_id=bill.patient_id,
        amount=bill.amount,
        payment_status=bill.payment_status,
        bill_date=bdate,
    )
    session.add(db_bill)
    session.commit()
    session.refresh(db_bill)
    return db_bill

@app.patch("/bills/{bill_id}")
def update_bill(bill_id: int, bill: Bill_update, session: Session = Depends(get_session)):
    db_bill = session.query(Bill).filter(Bill.bill_id == bill_id).first()
    if not db_bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    for key, value in bill.model_dump(exclude_unset=True).items():
        if key == "bill_date" and value is not None and not isinstance(value, str):
            value = str(value)
        setattr(db_bill, key, value)
    session.commit()
    session.refresh(db_bill)
    return db_bill

@app.delete("/bills/{bill_id}")
def delete_bill(bill_id: int, session: Session = Depends(get_session)):
    bill = session.query(Bill).filter(Bill.bill_id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    session.delete(bill)
    session.commit()
    return {"message": f"Bill {bill_id} deleted successfully"}