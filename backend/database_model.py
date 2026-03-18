from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from database import Base

class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String)
    patient_age = Column(Integer)
    disease = Column(String)
    admission_date = Column(String)  # stored as "YYYY-MM-DD"


class Doctor(Base):
    __tablename__ = "doctors"

    doctor_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    specialization = Column(String)
    phone = Column(String)
    availability = Column(String)


class MedicalRecord(Base):
    __tablename__ = "medical_records"

    record_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"))
    diagnosis = Column(String)
    prescription = Column(String)
    visit_date = Column(String)  # stored as "YYYY-MM-DD"


class Bill(Base):
    __tablename__ = "bills"

    bill_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"))
    amount = Column(Numeric(10, 2))
    payment_status = Column(String)
    bill_date = Column(String)  # stored as "YYYY-MM-DD"