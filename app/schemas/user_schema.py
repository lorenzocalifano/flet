from pydantic import BaseModel, EmailStr
from enum import Enum

# === SCHEMAS PER GLI UTENTI ===
# Qui definiamo i modelli di validazione usati nei services e nelle API interne

class UserRole(str, Enum):
    # Ruoli disponibili nel sistema
    MAGAZZINIERE = "MAGAZZINIERE"
    SEGRETERIA = "SEGRETERIA"
    RESPONSABILE = "RESPONSABILE"

class UserBase(BaseModel):
    # Base comune per tutti gli schemi utente
    nome: str
    cognome: str
    email: EmailStr  # validazione automatica email
    ruolo: UserRole

class UserCreate(UserBase):
    # Schema per creare un nuovo utente (include la password)
    password: str

class UserResponse(UserBase):
    # Schema di risposta (ad es. quando ritorniamo un utente da un service)
    id: int

    class Config:
        from_attributes = True  # permette di usare direttamente gli oggetti ORM