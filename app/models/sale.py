from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.models.database import Base

class Sale(Base):
    __tablename__ = "sales"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    prodotto_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantita = Column(Integer, nullable=False)
    cliente = Column(String, nullable=False)
    data_vendita = Column(Date, nullable=False)
    stato = Column(String, default="confermato")
    metodo_pagamento = Column(String, nullable=False, default="contanti")