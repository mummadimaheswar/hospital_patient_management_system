from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from backend.database import Base


class Diagnosis(Base):
    __tablename__ = "diagnoses"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    diagnosis_date = Column(Date, nullable=False)
    description = Column(Text, nullable=False)
    prescription = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
