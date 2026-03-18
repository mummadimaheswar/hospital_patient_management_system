from sqlalchemy import Column, Integer, String
from database import Base

class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String)
    patient_age = Column(Integer)
    disease = Column(String)
    admission_date = Column(String)  # stored as "YYYY-MM-DD"