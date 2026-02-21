from sqlalchemy import Column, Integer, String, Enum
from backend.database import Base
import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    doctor = "doctor"
    receptionist = "receptionist"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.receptionist)
    full_name = Column(String(100), nullable=False)
