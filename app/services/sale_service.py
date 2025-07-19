from sqlalchemy.orm import Session
from app.models.sale import Sale
from app.schemas.sale_schema import SaleCreate
from app.services.notification_service import create_notification
from datetime import date

def create_sale(db: Session, sale: SaleCreate):
    nuova = Sale(
        prodotto_id=sale.prodotto_id,
        quantita=sale.quantita,
        cliente=sale.cliente,
        data_vendita=sale.data_vendita or date.today(),
        stato=sale.stato or "confermato",
        metodo_pagamento=sale.metodo_pagamento
    )
    db.add(nuova)
    db.commit()
    db.refresh(nuova)

    # Notifica coerente con i test
    create_notification(
        db,
        messaggio=f"Vendita registrata: ID {nuova.id}, Cliente {nuova.cliente}, Quantità {nuova.quantita}",
        tipo="vendita",
        operazione_id=nuova.id
    )

    return nuova

def get_all_sales(db: Session):
    return db.query(Sale).all()

def get_sale_by_id(db: Session, sale_id: int):
    return db.query(Sale).filter(Sale.id == sale_id).first()

def cancel_sale(db: Session, sale_id: int):
    vendita = db.query(Sale).filter(Sale.id == sale_id).first()
    if vendita:
        vendita.stato = "annullato"
        db.commit()
        db.refresh(vendita)
        create_notification(
            db,
            messaggio=f"Vendita annullata: ID {vendita.id}, Cliente {vendita.cliente}",
            tipo="vendita",
            operazione_id=vendita.id
        )
    return vendita