# app/models/product.py

from sqlalchemy import Column, Integer, String
from app.models.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    quantita = Column(Integer, nullable=False)
    modello = Column(String, nullable=True)
    dimensione = Column(String, nullable=True)
    brand = Column(String, nullable=True)
    potenza = Column(Integer, nullable=True)