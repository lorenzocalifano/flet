from sqlalchemy.orm import Session
from app.models.rental import Rental
from app.schemas.rental_schema import RentalCreate
from datetime import date

# Servizi Per I Noleggi
def create_rental(db: Session, rental: RentalCreate):
    # Crea un nuovo noleggio con stato di default "in corso"
    nuovo = Rental(
        prodotto_id=rental.prodotto_id,
        quantita=rental.quantita,
        cliente=rental.cliente,
        data_inizio=rental.data_inizio or date.today(),  # Se non specificata, oggi di default
        data_fine=rental.data_fine or date.today(),      # Potremmo forzare > data_inizio in futuro
        stato=rental.stato if rental.stato else "in corso",  # Forzato "in corso" se non passato
        metodo_pagamento=rental.metodo_pagamento
    )
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo


def get_all_rentals(db: Session):
    # Restituisce tutti i noleggi registrati
    return db.query(Rental).all()


def conclude_rental(db: Session, rental_id: int):
    # Cambia lo stato di un noleggio in "concluso"
    noleggio = db.query(Rental).filter(Rental.id == rental_id).first()
    if noleggio:
        noleggio.stato = "concluso"
        db.commit()
        db.refresh(noleggio)
    return noleggio


def get_rental_by_id(db: Session, rental_id: int):
    # Cerca un noleggio per ID, utile per i dettagli nelle notifiche
    return db.query(Rental).filter(Rental.id == rental_id).first()