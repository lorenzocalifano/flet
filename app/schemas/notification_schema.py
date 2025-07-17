from pydantic import BaseModel
from datetime import datetime

# === SCHEMAS PER LE NOTIFICHE ===
# Usati per creare e restituire informazioni sulle notifiche nel sistema

class NotificationBase(BaseModel):
    # Base comune per tutte le operazioni sulle notifiche
    messaggio: str             # testo della notifica
    data_creazione: datetime   # quando è stata creata
    letto: int                 # 0 = non letta, 1 = letta

class NotificationCreate(NotificationBase):
    # Schema per creare una nuova notifica
    pass

class NotificationResponse(NotificationBase):
    # Schema per restituire i dati completi di una notifica
    id: int

    class Config:
        from_attributes = True  # permette di usare direttamente oggetti ORM