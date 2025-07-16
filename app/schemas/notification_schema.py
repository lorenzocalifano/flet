# Notification schema
from pydantic import BaseModel
from datetime import datetime

class NotificationBase(BaseModel):
    messaggio: str
    data_creazione: datetime
    letto: int

class NotificationCreate(NotificationBase):
    pass

class NotificationResponse(NotificationBase):
    id: int

    class Config:
        from_attributes = True