from pydantic import BaseModel
from datetime import date

# === SCHEMAS PER I NOLEGGI ===
# Usati per creare, aggiornare e restituire i dati dei noleggi

class RentalBase(BaseModel):
    # Base comune per tutte le operazioni sui noleggi
    prodotto_id: int           # prodotto noleggiato
    quantita: int              # quantità noleggiata
    cliente: str               # nome cliente
    data_inizio: date          # data inizio noleggio
    data_fine: date            # data fine noleggio
    stato: str = "attivo"      # stato di default "attivo" (può diventare "concluso")
    metodo_pagamento: str = "contanti"  # valore di default contanti


class RentalCreate(RentalBase):
    # Schema per creazione noleggio (uguale a RentalBase)
    pass


class RentalUpdate(BaseModel):
    # Schema per aggiornare solo alcuni campi di un noleggio
    quantita: int | None = None
    data_fine: date | None = None
    stato: str | None = None


class RentalResponse(RentalBase):
    # Schema per restituire un noleggio completo
    id: int

    class Config:
        from_attributes = True  # permette conversione automatica dagli oggetti ORM