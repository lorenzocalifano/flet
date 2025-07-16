# Notification model
from sqlalchemy import Column, Integer, String, DateTime
from app.models.database import Base
from datetime import datetime

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    messaggio = Column(String, nullable=False)
    data_creazione = Column(DateTime, default=datetime.utcnow)
    letto = Column(Integer, default=0)  # 0 = non letto, 1 = letto