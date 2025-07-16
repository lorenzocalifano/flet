# Product schema
from pydantic import BaseModel

class ProductBase(BaseModel):
    nome: str
    categoria: str
    brand: str | None = None
    modello: str | None = None
    potenza: str | None = None
    dimensione: str | None = None
    quantita: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    nome: str | None = None
    categoria: str | None = None
    brand: str | None = None
    modello: str | None = None
    potenza: str | None = None
    dimensione: str | None = None
    quantita: int | None = None

class ProductResponse(ProductBase):
    id: int
    disponibile: bool

    class Config:
        from_attributes = True