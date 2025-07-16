# Product service
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.product import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate

# ✅ 1. Aggiungi un nuovo prodotto
def create_product(db: Session, product_data: ProductCreate):
    nuovo_prodotto = Product(
        nome=product_data.nome,
        categoria=product_data.categoria,
        brand=product_data.brand,
        modello=product_data.modello,
        potenza=product_data.potenza,
        dimensione=product_data.dimensione,
        quantita=product_data.quantita,
        disponibile=True if product_data.quantita > 0 else False
    )
    db.add(nuovo_prodotto)
    db.commit()
    db.refresh(nuovo_prodotto)
    return nuovo_prodotto

# ✅ 2. Ottieni tutti i prodotti (Catalogo)
def get_all_products(db: Session):
    return db.query(Product).all()

# ✅ 3. Cerca prodotti per nome o categoria (ricerca testuale)
def search_products(db: Session, query: str):
    return db.query(Product).filter(
        or_(
            Product.nome.ilike(f"%{query}%"),
            Product.categoria.ilike(f"%{query}%")
        )
    ).all()

# ✅ 4. Filtra prodotti per attributi
def filter_products(db: Session, categoria=None, brand=None, modello=None, potenza=None, dimensione=None):
    query = db.query(Product)
    if categoria:
        query = query.filter(Product.categoria == categoria)
    if brand:
        query = query.filter(Product.brand == brand)
    if modello:
        query = query.filter(Product.modello == modello)
    if potenza:
        query = query.filter(Product.potenza == potenza)
    if dimensione:
        query = query.filter(Product.dimensione == dimensione)
    return query.all()

# ✅ 5. Ottieni un prodotto per ID
def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

# ✅ 6. Modifica un prodotto
def update_product(db: Session, product_id: int, update_data: ProductUpdate):
    prodotto = get_product_by_id(db, product_id)
    if not prodotto:
        return None

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(prodotto, field, value)

    # Aggiorna stato disponibilità
    if prodotto.quantita == 0:
        prodotto.disponibile = False
    elif prodotto.quantita > 0:
        prodotto.disponibile = True

    db.commit()
    db.refresh(prodotto)
    return prodotto

# ✅ 7. Aggiornamento rapido quantità
def update_quantity(db: Session, product_id: int, nuova_quantita: int):
    prodotto = get_product_by_id(db, product_id)
    if not prodotto:
        return None

    prodotto.quantita = nuova_quantita
    prodotto.disponibile = True if nuova_quantita > 0 else False

    db.commit()
    db.refresh(prodotto)
    return prodotto

# ✅ 8. Elimina un prodotto
def delete_product(db: Session, product_id: int):
    prodotto = get_product_by_id(db, product_id)
    if not prodotto:
        return None

    db.delete(prodotto)
    db.commit()
    return True
