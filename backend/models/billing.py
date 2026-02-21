from sqlalchemy import Column, Integer, String, Date, Numeric, Enum, ForeignKey
from backend.database import Base
import enum


class PaymentStatus(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    partial = "partial"


class Billing(Base):
    __tablename__ = "billing"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=True)
    billing_date = Column(Date, nullable=False)
    description = Column(String(255), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.pending)
