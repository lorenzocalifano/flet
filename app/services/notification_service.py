from sqlalchemy.orm import Session
from app.models.notification import Notification
from datetime import datetime

# === SERVIZI PER LA GESTIONE DELLE NOTIFICHE ===
def create_notification(db: Session, messaggio: str, tipo: str = None, operazione_id: int = None):
    # crea e salva una nuova notifica nel database
    nuova_notifica = Notification(
        messaggio=messaggio,
        data_creazione=datetime.utcnow(),  # uso UTC così siamo coerenti, anche se per ora non ci serve timezone
        letto=0,  # 0 = non letta, 1 = letta
        tipo=tipo,
        operazione_id=operazione_id
    )
    db.add(nuova_notifica)
    db.commit()
    db.refresh(nuova_notifica)
    return nuova_notifica


def get_all_notifications(db: Session):
    # restituisce tutte le notifiche ordinate dalla più recente alla più vecchia
    return db.query(Notification).order_by(Notification.data_creazione.desc()).all()


def get_unread_notifications(db: Session):
    # restituisce solo le notifiche non lette
    return db.query(Notification).filter(Notification.letto == 0).all()


def mark_notification_as_read(db: Session, notification_id: int):
    # segna una notifica come letta (usato quando l'utente apre il dettaglio)
    notifica = db.query(Notification).filter(Notification.id == notification_id).first()
    if notifica and notifica.letto == 0:
        notifica.letto = 1
        db.commit()
        db.refresh(notifica)
    return notifica


def get_notification_by_id(db: Session, notification_id: int):
    # cerca una notifica specifica per ID (utile per pagina dettaglio)
    return db.query(Notification).filter(Notification.id == notification_id).first()