from pydantic import BaseModel
from datetime import date

# === SCHEMAS PER I DANNI ===
# Usati per segnalare e restituire informazioni sui danni ai prodotti

class DamageBase(BaseModel):
    # Base comune per tutte le operazioni sui danni
    prodotto_id: int            # ID del prodotto danneggiato
    descrizione: str            # descrizione breve del danno
    data_segnalazione: date     # quando è stato segnalato

class DamageCreate(DamageBase):
    # Schema per creare una nuova segnalazione di danno
    pass

class DamageResponse(DamageBase):
    # Schema per restituire i dettagli di un danno
    id: int

    class Config:
        from_attributes = True  # permette conversione diretta dagli oggetti ORM