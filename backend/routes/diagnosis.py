from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models.diagnosis import Diagnosis
from backend.schemas.diagnosis import DiagnosisCreate, DiagnosisUpdate, DiagnosisOut
from backend.auth.auth import get_current_user, require_role

router = APIRouter(prefix="/diagnoses", tags=["Diagnoses"])


@router.post("/", response_model=DiagnosisOut, status_code=status.HTTP_201_CREATED)
def create_diagnosis(diag_in: DiagnosisCreate, db: Session = Depends(get_db), current_user=Depends(require_role("admin", "doctor"))):
    diag = Diagnosis(**diag_in.model_dump())
    db.add(diag)
    db.commit()
    db.refresh(diag)
    return diag


@router.get("/", response_model=List[DiagnosisOut])
def list_diagnoses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Diagnosis).offset(skip).limit(limit).all()


@router.get("/{diagnosis_id}", response_model=DiagnosisOut)
def get_diagnosis(diagnosis_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    diag = db.query(Diagnosis).filter(Diagnosis.id == diagnosis_id).first()
    if not diag:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    return diag


@router.get("/patient/{patient_id}", response_model=List[DiagnosisOut])
def get_diagnoses_by_patient(patient_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Diagnosis).filter(Diagnosis.patient_id == patient_id).all()


@router.put("/{diagnosis_id}", response_model=DiagnosisOut)
def update_diagnosis(diagnosis_id: int, diag_in: DiagnosisUpdate, db: Session = Depends(get_db), current_user=Depends(require_role("admin", "doctor"))):
    diag = db.query(Diagnosis).filter(Diagnosis.id == diagnosis_id).first()
    if not diag:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    for field, value in diag_in.model_dump(exclude_unset=True).items():
        setattr(diag, field, value)
    db.commit()
    db.refresh(diag)
    return diag
