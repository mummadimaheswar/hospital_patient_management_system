from pydantic import BaseModel
from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional


class PaymentStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    partial = "partial"


class BillingCreate(BaseModel):
    patient_id: int
    appointment_id: Optional[int] = None
    billing_date: date
    description: str
    amount: Decimal
    payment_status: PaymentStatus = PaymentStatus.pending


class BillingUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[Decimal] = None
    payment_status: Optional[PaymentStatus] = None


class BillingOut(BillingCreate):
    id: int

    model_config = {"from_attributes": True}
