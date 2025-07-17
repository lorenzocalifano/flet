from sqlalchemy.orm import Session
from app.models.sale import Sale
from app.schemas.sale_schema import SaleCreate
from datetime import date

# === SERVIZI PER LE VENDITE ===
def create_sale(db: Session, sale: SaleCreate):
    # crea una nuova vendita e la salva nel database
    nuova = Sale(
        prodotto_id=sale.prodotto_id,
        quantita=sale.quantita,
        cliente=sale.cliente,
        data_vendita=sale.data_vendita or date.today(),  # se non passata, usa la data di oggi
        stato=sale.stato or "confermato",
        metodo_pagamento=sale.metodo_pagamento
    )
    db.add(nuova)
    db.commit()
    db.refresh(nuova)
    return nuova


def get_all_sales(db: Session):
    # restituisce tutte le vendite registrate
    return db.query(Sale).all()


def get_sale_by_id(db: Session, sale_id: int):
    # cerca una vendita specifica per ID
    return db.query(Sale).filter(Sale.id == sale_id).first()