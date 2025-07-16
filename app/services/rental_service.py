# Rental service
from sqlalchemy.orm import Session
from app.models.rental import Rental
from app.schemas.rental_schema import RentalCreate
from datetime import date

# ✅ 1. Registra un nuovo noleggio
def create_rental(db: Session, rental_data: RentalCreate):
    nuovo_noleggio = Rental(
        prodotto_id=rental_data.prodotto_id,
        quantita=rental_data.quantita,
        cliente=rental_data.cliente,
        data_inizio=rental_data.data_inizio,
        data_fine=rental_data.data_fine,
        stato="attivo",
        metodo_pagamento=rental_data.metodo_pagamento  # ✅
    )
    db.add(nuovo_noleggio)
    db.commit()
    db.refresh(nuovo_noleggio)
    return nuovo_noleggio

# ✅ 2. Ottieni tutti i noleggi (storico)
def get_all_rentals(db: Session):
    return db.query(Rental).all()

# ✅ 3. Modifica un noleggio
def update_rental(db: Session, rental_id: int, data_fine: date = None, stato: str = None):
    noleggio = db.query(Rental).filter(Rental.id == rental_id).first()
    if not noleggio:
        return None

    if data_fine:
        noleggio.data_fine = data_fine
    if stato:
        noleggio.stato = stato

    db.commit()
    db.refresh(noleggio)
    return noleggio

# ✅ 4. Concludi un noleggio
def conclude_rental(db: Session, rental_id: int):
    return update_rental(db, rental_id, stato="concluso")

# ✅ 5. Annulla un noleggio
def cancel_rental(db: Session, rental_id: int):
    return update_rental(db, rental_id, stato="annullato")
