# User model
from sqlalchemy import Column, Integer, String, Enum
from app.models.database import Base
import enum

class UserRole(enum.Enum):
    LAVORATORE = "lavoratore"
    SEGRETERIA = "segreteria"
    RESPONSABILE = "responsabile"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cognome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    ruolo = Column(Enum(UserRole), nullable=False, default=UserRole.LAVORATORE)