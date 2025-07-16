from sqlalchemy import Column, Integer, String, DateTime
from app.models.database import Base
from datetime import datetime

class Notification(Base):
    __tablename__ = "notifications"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    messaggio = Column(String, nullable=False)
    data_creazione = Column(DateTime, default=datetime.utcnow)
    letto = Column(Integer, default=0)
    tipo = Column(String, nullable=True)  # "noleggio" o "vendita"
    operazione_id = Column(Integer, nullable=True)