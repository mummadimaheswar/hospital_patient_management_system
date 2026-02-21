from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models.billing import Billing
from backend.schemas.billing import BillingCreate, BillingUpdate, BillingOut
from backend.auth.auth import get_current_user, require_role

router = APIRouter(prefix="/billing", tags=["Billing"])


@router.post("/", response_model=BillingOut, status_code=status.HTTP_201_CREATED)
def create_bill(bill_in: BillingCreate, db: Session = Depends(get_db), current_user=Depends(require_role("admin", "receptionist"))):
    bill = Billing(**bill_in.model_dump())
    db.add(bill)
    db.commit()
    db.refresh(bill)
    return bill


@router.get("/", response_model=List[BillingOut])
def list_bills(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Billing).offset(skip).limit(limit).all()


@router.get("/{bill_id}", response_model=BillingOut)
def get_bill(bill_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    bill = db.query(Billing).filter(Billing.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill


@router.get("/patient/{patient_id}", response_model=List[BillingOut])
def get_bills_by_patient(patient_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Billing).filter(Billing.patient_id == patient_id).all()


@router.put("/{bill_id}", response_model=BillingOut)
def update_bill(bill_id: int, bill_in: BillingUpdate, db: Session = Depends(get_db), current_user=Depends(require_role("admin", "receptionist"))):
    bill = db.query(Billing).filter(Billing.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    for field, value in bill_in.model_dump(exclude_unset=True).items():
        setattr(bill, field, value)
    db.commit()
    db.refresh(bill)
    return bill
