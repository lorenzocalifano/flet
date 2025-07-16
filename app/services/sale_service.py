# Sale service
from sqlalchemy.orm import Session
from app.models.sale import Sale
from app.schemas.sale_schema import SaleCreate
from datetime import date

# ✅ 1. Registra una nuova vendita
def create_sale(db: Session, sale_data: SaleCreate):
    nuova_vendita = Sale(
        prodotto_id=sale_data.prodotto_id,
        quantita=sale_data.quantita,
        cliente=sale_data.cliente,
        data_vendita=sale_data.data_vendita,
        stato="confermato",
        metodo_pagamento=sale_data.metodo_pagamento  # ✅
    )
    db.add(nuova_vendita)
    db.commit()
    db.refresh(nuova_vendita)
    return nuova_vendita

# ✅ 2. Ottieni tutte le vendite (storico)
def get_all_sales(db: Session):
    return db.query(Sale).all()

# ✅ 3. Annulla una vendita
def cancel_sale(db: Session, sale_id: int):
    vendita = db.query(Sale).filter(Sale.id == sale_id).first()
    if not vendita:
        return None
    vendita.stato = "annullato"
    db.commit()
    db.refresh(vendita)
    return vendita