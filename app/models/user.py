from sqlalchemy import Column, Integer, String, Enum
from app.models.database import Base
import enum

class UserRole(enum.Enum):
    MAGAZZINIERE = "MAGAZZINIERE"
    SEGRETERIA = "SEGRETERIA"
    RESPONSABILE = "RESPONSABILE"

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cognome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    ruolo = Column(Enum(UserRole, values_callable=lambda x: [e.value for e in x]),
                   nullable=False, default=UserRole.MAGAZZINIERE)