# app/schemas/product_schema.py

from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    nome: str
    categoria: str
    quantita: int
    modello: Optional[str] = None
    dimensione: Optional[str] = None
    brand: Optional[str] = None
    potenza: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True