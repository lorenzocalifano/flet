from sqlalchemy.orm import Session
from app.models.damage import Damage
from app.models.product import Product
from app.schemas.damage_schema import DamageCreate
from datetime import date

# === SERVIZI PER LA GESTIONE DEI DANNI ===
def report_damage(db: Session, damage_data: DamageCreate):
    # registra un nuovo danno per un prodotto
    nuovo_danno = Damage(
        prodotto_id=damage_data.prodotto_id,
        descrizione=damage_data.descrizione,
        data_segnalazione=damage_data.data_segnalazione or date.today()
    )
    db.add(nuovo_danno)
    db.commit()
    db.refresh(nuovo_danno)

    # marca il prodotto come non completamente disponibile (se ha danni lo gestiamo così)
    prodotto = db.query(Product).filter(Product.id == damage_data.prodotto_id).first()
    if prodotto:
        # in realtà la disponibilità è calcolata con i danni, ma qui lasciamo la logica pronta
        prodotto.disponibile = False
        db.commit()

    return nuovo_danno


def count_damages_for_product(db: Session, prodotto_id: int):
    # conta quanti danni sono segnalati per un determinato prodotto
    return db.query(Damage).filter(Damage.prodotto_id == prodotto_id).count()