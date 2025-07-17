from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product_schema import ProductCreate

def create_product(db: Session, product: ProductCreate):
    nuovo_prodotto = Product(
        nome=product.nome,
        categoria=product.categoria,
        quantita=product.quantita,
        modello=product.modello,
        dimensione=product.dimensione,
        brand=product.brand
    )
    db.add(nuovo_prodotto)
    db.commit()
    db.refresh(nuovo_prodotto)
    return nuovo_prodotto

def get_all_products(db: Session):
    return db.query(Product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def update_quantity(db: Session, product_id: int, new_quantity: int):
    prodotto = get_product_by_id(db, product_id)
    if prodotto:
        prodotto.quantita = new_quantity
        db.commit()
        db.refresh(prodotto)
    return prodotto