# User schema
from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    LAVORATORE = "lavoratore"
    SEGRETERIA = "segreteria"
    RESPONSABILE = "responsabile"

class UserBase(BaseModel):
    nome: str
    cognome: str
    email: EmailStr
    ruolo: UserRole

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    nome: str | None = None
    cognome: str | None = None
    password: str | None = None

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True