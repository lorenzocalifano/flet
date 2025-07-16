# Damage model
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.models.database import Base

class Damage(Base):
    __tablename__ = "damages"
    __table_args__ = {'extend_existing': True}  # utile in sviluppo per evitare conflitti

    id = Column(Integer, primary_key=True, index=True)
    prodotto_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    descrizione = Column(String, nullable=False)
    data_segnalazione = Column(Date, nullable=False)