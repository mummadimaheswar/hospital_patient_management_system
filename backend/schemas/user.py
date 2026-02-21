from pydantic import BaseModel
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    doctor = "doctor"
    receptionist = "receptionist"


class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole
    full_name: str


class UserOut(BaseModel):
    id: int
    username: str
    role: UserRole
    full_name: str

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    role: str | None = None
