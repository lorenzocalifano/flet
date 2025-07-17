from pydantic import BaseModel
from typing import Optional

# === SCHEMAS PER I PRODOTTI ===
# Usati per validare i dati quando creiamo, aggiorniamo o leggiamo prodotti

class ProductBase(BaseModel):
    # Base comune per tutte le operazioni sui prodotti
    nome: str
    categoria: str
    quantita: int
    modello: Optional[str] = None
    dimensione: Optional[str] = None
    brand: Optional[str] = None

class ProductCreate(ProductBase):
    # Schema per creazione prodotto (per ora identico a ProductBase)
    pass

class ProductUpdate(ProductBase):
    # Schema per aggiornamento prodotto (stesso schema, ma concettualmente diverso)
    pass

class ProductResponse(ProductBase):
    # Schema usato per restituire un prodotto (ad esempio nei services o API)
    id: int  # l'ID viene aggiunto solo in risposta

    class Config:
        from_attributes = True  # permette di convertire direttamente da oggetti ORM