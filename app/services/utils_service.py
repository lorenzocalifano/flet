from sqlalchemy.orm import Session
from app.models.sale import Sale
from app.models.rental import Rental

def get_venduti_totali(db: Session, prodotto_id: int):
    """Restituisce il totale dei prodotti venduti"""
    return sum(v.quantita for v in db.query(Sale).filter(Sale.prodotto_id == prodotto_id).all())

def get_noleggiati_in_corso(db: Session, prodotto_id: int, exclude_rental_id: int = None):
    """Restituisce il totale dei prodotti noleggiati in corso (escludendo un noleggio specifico)"""
    query = db.query(Rental).filter(Rental.prodotto_id == prodotto_id, Rental.stato == "in corso")
    if exclude_rental_id:
        query = query.filter(Rental.id != exclude_rental_id)
    return sum(r.quantita for r in query.all())