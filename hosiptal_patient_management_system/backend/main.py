from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from database import create_db_and_tables, get_session
from database_model import Patient
from models import Patient_details, Patient_update

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# ---------- ROOT ----------
@app.get("/")
def root():
    return {"message": "Welcome to Hospital Patient Management System"}

# ---------- GET ALL ----------
@app.get("/patients/")
def get_all_patients(session: Session = Depends(get_session)):
    patients = session.query(Patient).all()
    return patients

# ---------- GET BY ID ----------
@app.get("/patients/{patient_id}")
def get_patient(patient_id: int, session: Session = Depends(get_session)):
    patient = session.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

# ---------- CREATE ----------
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

# ---------- UPDATE (PATCH) ----------
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

# ---------- DELETE ----------
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, session: Session = Depends(get_session)):
    patient = session.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    session.delete(patient)
    session.commit()
    return {"message": f"Patient {patient_id} deleted successfully"}