# Sale schema
from pydantic import BaseModel
from datetime import date


class SaleBase(BaseModel):
    prodotto_id: int
    quantita: int
    cliente: str
    data_vendita: date
    stato: str = "confermato"
    metodo_pagamento: str = "contanti"

class SaleCreate(SaleBase):
    pass

class SaleUpdate(BaseModel):
    stato: str | None = None

class SaleResponse(SaleBase):
    id: int

    class Config:
        from_attributes = True