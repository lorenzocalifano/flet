import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base
from app.services.product_service import create_product, get_all_products
from app.schemas.product_schema import ProductCreate

class TestProductService(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        self.Session = sessionmaker(bind=engine)
        self.db = self.Session()

    def tearDown(self):
        self.db.close()

    def test_create_product_success(self):
        product = create_product(self.db, ProductCreate(
            nome="Cassa", categoria="Audio", quantita=10))
        self.assertIsNotNone(product.id)

    def test_get_all_products(self):
        create_product(self.db, ProductCreate(
            nome="Prod1", categoria="Cat", quantita=5))
        products = get_all_products(self.db)
        self.assertEqual(len(products), 1)

if __name__ == "__main__":
    unittest.main()