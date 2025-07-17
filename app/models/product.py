from sqlalchemy import Column, Integer, String
from app.models.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    quantita = Column(Integer, default=0)

    # NUOVI CAMPI
    modello = Column(String, nullable=True)
    dimensione = Column(String, nullable=True)
    brand = Column(String, nullable=True)