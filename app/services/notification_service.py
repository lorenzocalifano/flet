from sqlalchemy.orm import Session
from app.models.notification import Notification
from datetime import datetime

# ✅ 1. Crea una nuova notifica
def create_notification(db: Session, messaggio: str, tipo: str = None, operazione_id: int = None):
    nuova_notifica = Notification(
        messaggio=messaggio,
        data_creazione=datetime.utcnow(),
        letto=0,
        tipo=tipo,
        operazione_id=operazione_id
    )
    db.add(nuova_notifica)
    db.commit()
    db.refresh(nuova_notifica)
    return nuova_notifica

# ✅ 2. Ottieni tutte le notifiche
def get_all_notifications(db: Session):
    return db.query(Notification).order_by(Notification.data_creazione.desc()).all()

# ✅ 3. Ottieni solo notifiche non lette
def get_unread_notifications(db: Session):
    return db.query(Notification).filter(Notification.letto == 0).all()

# ✅ 4. Segna una notifica come letta (compatibile con pagina dettaglio)
def mark_notification_as_read(db: Session, notification_id: int):
    notifica = db.query(Notification).filter(Notification.id == notification_id).first()
    if notifica and notifica.letto == 0:
        notifica.letto = 1
        db.commit()
        db.refresh(notifica)
    return notifica

# ✅ 5. Ottieni una notifica per ID (necessario per pagina dettaglio)
def get_notification_by_id(db: Session, notification_id: int):
    return db.query(Notification).filter(Notification.id == notification_id).first()