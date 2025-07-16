from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.models.database import Base

class Rental(Base):
    __tablename__ = "rentals"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    prodotto_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantita = Column(Integer, nullable=False)
    cliente = Column(String, nullable=False)
    data_inizio = Column(Date, nullable=False)
    data_fine = Column(Date, nullable=False)
    stato = Column(String, default="attivo")
    metodo_pagamento = Column(String, nullable=False, default="contanti")