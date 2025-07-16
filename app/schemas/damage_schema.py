# Damage schema
from pydantic import BaseModel
from datetime import date

class DamageBase(BaseModel):
    prodotto_id: int
    descrizione: str
    data_segnalazione: date

class DamageCreate(DamageBase):
    pass

class DamageResponse(DamageBase):
    id: int

    class Config:
        from_attributes = True