from sqlalchemy.orm import Session
from app.models.sale import Sale
from app.schemas.sale_schema import SaleCreate
from datetime import date

# ✅ Crea una nuova vendita
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
    return nuova

# ✅ Ottieni tutte le vendite
def get_all_sales(db: Session):
    return db.query(Sale).all()

# ✅ NUOVA: ottieni una vendita per ID
def get_sale_by_id(db: Session, sale_id: int):
    return db.query(Sale).filter(Sale.id == sale_id).first()