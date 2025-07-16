# Rental schema
from pydantic import BaseModel
from datetime import date

class RentalBase(BaseModel):
    prodotto_id: int
    quantita: int
    cliente: str
    data_inizio: date
    data_fine: date
    stato: str

class RentalCreate(RentalBase):
    pass

class RentalUpdate(BaseModel):
    quantita: int | None = None
    data_fine: date | None = None
    stato: str | None = None

class RentalResponse(RentalBase):
    id: int

    class Config:
        from_attributes = True