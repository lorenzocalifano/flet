# Product model
from sqlalchemy import Column, Integer, String, Float, Boolean
from app.models.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    brand = Column(String, nullable=True)
    modello = Column(String, nullable=True)
    potenza = Column(String, nullable=True)
    dimensione = Column(String, nullable=True)
    quantita = Column(Integer, nullable=False, default=0)
    disponibile = Column(Boolean, default=True)