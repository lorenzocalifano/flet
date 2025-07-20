from sqlalchemy.orm import Session
from app.models.sale import Sale
from app.models.product import Product
from app.models.rental import Rental
from app.schemas.sale_schema import SaleCreate
from app.services.notification_service import create_notification
from datetime import date


def create_sale(db: Session, sale: SaleCreate):
    prodotto = db.query(Product).filter(Product.id == sale.prodotto_id).first()

    if not prodotto:
        raise ValueError("Prodotto non trovato")

    # Calcolo quantità disponibili (considerando solo noleggi e non vendite annullate)
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

    if sale.quantita > disponibili:
        raise ValueError(f"Quantità non disponibile. Disponibili: {disponibili}")

    nuova_vendita = Sale(
        prodotto_id=sale.prodotto_id,
        quantita=sale.quantita,
        cliente=sale.cliente,
        data_vendita=sale.data_vendita or date.today(),
        stato=sale.stato or "confermato",
        metodo_pagamento=sale.metodo_pagamento
    )

    db.add(nuova_vendita)
    db.commit()
    db.refresh(nuova_vendita)
    create_notification(db, f"Vendita registrata per {nuova_vendita.cliente}", tipo="vendita",
                        operazione_id=nuova_vendita.id)
    return nuova_vendita


def get_all_sales(db: Session):
    return db.query(Sale).all()


def get_sale_by_id(db: Session, sale_id: int):
    """Restituisce una vendita per ID"""
    return db.query(Sale).filter(Sale.id == sale_id).first()


def cancel_sale(db: Session, sale_id: int):
    vendita = db.query(Sale).filter(Sale.id == sale_id).first()
    if vendita and vendita.stato == "confermato":
        vendita.stato = "annullato"
        db.commit()
        db.refresh(vendita)
        create_notification(db, f"Vendita annullata per {vendita.cliente}", tipo="vendita",
                            operazione_id=vendita.id)
    return vendita