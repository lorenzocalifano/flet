from sqlalchemy.orm import Session
from app.models.damage import Damage
from app.models.product import Product
from app.schemas.damage_schema import DamageCreate
from datetime import date

def report_damage(db: Session, damage_data: DamageCreate):
    nuovo_danno = Damage(
        prodotto_id=damage_data.prodotto_id,
        descrizione=damage_data.descrizione,
        data_segnalazione=damage_data.data_segnalazione or date.today()
    )
    db.add(nuovo_danno)
    db.commit()
    db.refresh(nuovo_danno)
    return nuovo_danno

    # ✅ Marca il prodotto come non disponibile
    prodotto = db.query(Product).filter(Product.id == damage_data.prodotto_id).first()
    if prodotto:
        prodotto.disponibile = False

    db.commit()
    db.refresh(nuovo_danno)
    return nuovo_danno

def count_damages_for_product(db: Session, prodotto_id: int):
    return db.query(Damage).filter(Damage.prodotto_id == prodotto_id).count()