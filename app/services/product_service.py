from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product_schema import ProductCreate

def create_product(db: Session, product: ProductCreate):
    # crea un nuovo prodotto nel db
    nuovo = Product(
        nome=product.nome,
        categoria=product.categoria,
        quantita=product.quantita,
        modello=product.modello,
        dimensione=product.dimensione,
        brand=product.brand
    )
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo


def get_all_products(db: Session):
    # restituisce tutti i prodotti
    return db.query(Product).all()


def get_product_by_id(db: Session, product_id: int):
    # cerca un prodotto per ID, restituisce None se non trovato
    return db.query(Product).filter(Product.id == product_id).first()


def update_product_quantity(db: Session, product_id: int, quantity_change: int):
    # aggiorna la quantità di un prodotto
    prodotto = db.query(Product).filter(Product.id == product_id).first()
    if prodotto:
        prodotto.quantita += quantity_change
        db.commit()
        db.refresh(prodotto)
    return prodotto


def delete_product(db: Session, product_id: int):
    # elimina un prodotto dal db
    prodotto = db.query(Product).filter(Product.id == product_id).first()
    if prodotto:
        db.delete(prodotto)
        db.commit()
    return prodotto