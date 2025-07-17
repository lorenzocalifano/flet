from pydantic import BaseModel
from datetime import date

# === SCHEMAS PER LE VENDITE ===
# Usati per creare, aggiornare e restituire i dati delle vendite

class SaleBase(BaseModel):
    # Base comune per tutte le operazioni sulle vendite
    prodotto_id: int            # ID del prodotto venduto
    quantita: int               # quantità venduta
    cliente: str                # nome cliente (gestito come str)
    data_vendita: date          # data della vendita
    stato: str = "confermato"   # stato di default "confermato"
    metodo_pagamento: str = "contanti"  # default contanti

class SaleCreate(SaleBase):
    # Schema per creare una nuova vendita (identico a SaleBase)
    pass

class SaleUpdate(BaseModel):
    # Schema per aggiornare solo lo stato della vendita (es. annullato)
    stato: str | None = None

class SaleResponse(SaleBase):
    # Schema per restituire i dati di una vendita completa
    id: int

    class Config:
        from_attributes = True  # permette di usare direttamente oggetti ORM