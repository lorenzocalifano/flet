from sqlalchemy.orm import Session
from app.models.rental import Rental
from app.schemas.rental_schema import RentalCreate
from datetime import date

# ✅ Crea un nuovo noleggio
def create_rental(db: Session, rental: RentalCreate):
    nuovo = Rental(
        prodotto_id=rental.prodotto_id,
        quantita=rental.quantita,
        cliente=rental.cliente,
        data_inizio=rental.data_inizio or date.today(),
        data_fine=rental.data_fine or date.today(),
        stato=rental.stato or "in corso",
        metodo_pagamento=rental.metodo_pagamento
    )
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

# ✅ Ottieni tutti i noleggi
def get_all_rentals(db: Session):
    return db.query(Rental).all()

# ✅ CONCLUSIONE NOLEGGIO (se già presente)
def conclude_rental(db: Session, rental_id: int):
    noleggio = db.query(Rental).filter(Rental.id == rental_id).first()
    if noleggio:
        noleggio.stato = "concluso"
        db.commit()
        db.refresh(noleggio)
    return noleggio

# ✅ NUOVA: ottieni un noleggio per ID
def get_rental_by_id(db: Session, rental_id: int):
    return db.query(Rental).filter(Rental.id == rental_id).first()