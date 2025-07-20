from sqlalchemy.orm import Session
from app.models.rental import Rental
from app.models.product import Product
from app.models.sale import Sale
from app.schemas.rental_schema import RentalCreate
from datetime import date
from app.services.notification_service import create_notification

def create_rental(db: Session, rental: RentalCreate):
    prodotto = db.query(Product).filter(Product.id == rental.prodotto_id).first()

    if not prodotto:
        raise ValueError("Prodotto non trovato")

    # Calcolo disponibili
    noleggiati = sum(
        n.quantita for n in db.query(Rental).filter(
            Rental.prodotto_id == prodotto.id,
            Rental.stato == "in corso"
        ).all()
    )
    venduti = sum(
        s.quantita for s in db.query(Sale).filter(
            Sale.prodotto_id == prodotto.id,
            Sale.stato == "confermato"
        ).all()
    )
    disponibili = max(0, prodotto.quantita - venduti - noleggiati)

    if rental.quantita > disponibili:
        raise ValueError(f"Quantità non disponibile. Disponibili: {disponibili}")

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
    create_notification(db, f"Noleggio registrato per {nuovo.cliente}", tipo="noleggio", operazione_id=nuovo.id)
    return nuovo


def get_all_rentals(db: Session):
    return db.query(Rental).all()


def get_rental_by_id(db: Session, rental_id: int):
    return db.query(Rental).filter(Rental.id == rental_id).first()


def conclude_rental(db: Session, rental_id: int):
    noleggio = db.query(Rental).filter(Rental.id == rental_id).first()
    if noleggio and noleggio.stato != "annullato":
        noleggio.stato = "concluso"
        db.commit()
        db.refresh(noleggio)
        create_notification(db, f"Noleggio concluso per {noleggio.cliente}", tipo="noleggio", operazione_id=noleggio.id)
    return noleggio


def cancel_rental(db: Session, rental_id: int):
    noleggio = db.query(Rental).filter(Rental.id == rental_id).first()
    if noleggio and noleggio.stato != "concluso":
        noleggio.stato = "annullato"
        db.commit()
        db.refresh(noleggio)
        create_notification(db, f"Noleggio annullato per {noleggio.cliente}", tipo="noleggio", operazione_id=noleggio.id)
    return noleggio


def update_rental(db: Session, rental_id: int, quantita: int = None, data_fine: date = None, metodo_pagamento: str = None):
    noleggio = db.query(Rental).filter(Rental.id == rental_id).first()
    if noleggio and noleggio.stato == "in corso":
        if quantita is not None:
            prodotto = db.query(Product).filter(Product.id == noleggio.prodotto_id).first()

            altri_noleggiati = sum(
                n.quantita for n in db.query(Rental).filter(
                    Rental.prodotto_id == prodotto.id,
                    Rental.stato == "in corso",
                    Rental.id != noleggio.id
                ).all()
            )
            venduti = sum(
                s.quantita for s in db.query(Sale).filter(
                    Sale.prodotto_id == prodotto.id,
                    Sale.stato == "confermato"
                ).all()
            )
            disponibili = max(0, prodotto.quantita - venduti - altri_noleggiati)
            massimo_consentito = disponibili + noleggio.quantita

            if quantita > massimo_consentito:
                raise ValueError(f"Quantità non disponibile. Disponibili: {massimo_consentito}")

            noleggio.quantita = quantita

        if data_fine is not None:
            noleggio.data_fine = data_fine

        if metodo_pagamento is not None:
            noleggio.metodo_pagamento = metodo_pagamento

        db.commit()
        db.refresh(noleggio)
        create_notification(db, f"Noleggio modificato per {noleggio.cliente}", tipo="noleggio", operazione_id=noleggio.id)
    return noleggio