from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product_schema import ProductCreate

def create_product(db: Session, product_data: ProductCreate):
    nuovo = Product(
        nome=product_data.nome,
        categoria=product_data.categoria,
        quantita=product_data.quantita,
        modello=product_data.modello,
        dimensione=product_data.dimensione,
        brand=product_data.brand,
        potenza=product_data.potenza
    )
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

def get_all_products(db: Session):
    """Restituisce Tutti I Prodotti"""
    return db.query(Product).all()

def get_product_by_id(db: Session, product_id: int):
    """Restituisce Un Prodotto Per ID"""
    return db.query(Product).filter(Product.id == product_id).first()

def update_product_quantity(db: Session, product_id: int, new_quantity: int):
    """Aggiorna La Quantità Di Un Prodotto"""
    prodotto = db.query(Product).filter(Product.id == product_id).first()
    if prodotto:
        prodotto.quantita = new_quantity
        db.commit()
        db.refresh(prodotto)
    return prodotto

def delete_product(db: Session, product_id: int):
    """Elimina Un Prodotto Dal Database"""
    prodotto = db.query(Product).filter(Product.id == product_id).first()
    if prodotto:
        db.delete(prodotto)
        db.commit()
        return True
    return False