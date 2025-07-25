from sqlalchemy.orm import Session
from app.models.damage import Damage
from app.models.product import Product
from app.schemas.damage_schema import DamageCreate
from datetime import date
from app.services.notification_service import create_notification

def report_damage(db: Session, damage_data: DamageCreate):
    """Segnala Un Nuovo Danno E Genera Una Notifica."""
    nuovo_danno = Damage(
        prodotto_id=damage_data.prodotto_id,
        descrizione=damage_data.descrizione,
        data_segnalazione=damage_data.data_segnalazione or date.today()
    )
    db.add(nuovo_danno)
    db.commit()
    db.refresh(nuovo_danno)

    create_notification(
        db,
        messaggio=f"Danno Segnalato Per Il Prodotto ID {nuovo_danno.prodotto_id}: {nuovo_danno.descrizione}",
        tipo="danno",
        operazione_id=nuovo_danno.id
    )
    return nuovo_danno

def count_damages_for_product(db: Session, prodotto_id: int):
    """Conta I Danni Registrati Per Un Determinato Prodotto."""
    return db.query(Damage).filter(Damage.prodotto_id == prodotto_id).count()