from sqlalchemy.orm import Session
from app.models.rental import Rental
from app.schemas.rental_schema import RentalCreate
from datetime import date

# === SERVIZI PER I NOLEGGI ===
def create_rental(db: Session, rental: RentalCreate):
    # crea un nuovo noleggio
    nuovo = Rental(
        prodotto_id=rental.prodotto_id,
        quantita=rental.quantita,
        cliente=rental.cliente,
        data_inizio=rental.data_inizio or date.today(),  # se non specificata, oggi di default
        data_fine=rental.data_fine or date.today(),  # forse potremmo forzare > data_inizio
        stato=rental.stato or "in corso",
        metodo_pagamento=rental.metodo_pagamento
    )
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo


def get_all_rentals(db: Session):
    # restituisce tutti i noleggi registrati
    return db.query(Rental).all()


def conclude_rental(db: Session, rental_id: int):
    # cambia lo stato di un noleggio in "concluso"
    noleggio = db.query(Rental).filter(Rental.id == rental_id).first()
    if noleggio:
        noleggio.stato = "concluso"
        db.commit()
        db.refresh(noleggio)
    return noleggio


def get_rental_by_id(db: Session, rental_id: int):
    # cerca un noleggio per ID, utile per i dettagli nelle notifiche
    return db.query(Rental).filter(Rental.id == rental_id).first()