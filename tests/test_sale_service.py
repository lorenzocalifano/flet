import unittest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base
from app.models.product import Product
from app.services.sale_service import create_sale
from app.schemas.sale_schema import SaleCreate

class TestSaleService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configura un database in memoria per i test"""
        engine = create_engine("sqlite:///:memory:")
        TestingSession = sessionmaker(bind=engine)
        Base.metadata.create_all(bind=engine)
        cls.db = TestingSession()

        # Prodotto di base
        cls.product = Product(
            nome="Prodotto Vendita Test",
            categoria="Video",
            quantita=8
        )
        cls.db.add(cls.product)
        cls.db.commit()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def test_create_sale_success(self):
        """Verifica che una vendita valida venga creata correttamente"""
        sale = create_sale(self.db, SaleCreate(
            prodotto_id=self.product.id,
            quantita=3,
            cliente="Mario Rossi",
            data_vendita=date.today(),
            metodo_pagamento="paypal",
            stato="confermato"
        ))
        self.assertIsNotNone(sale.id)
        self.assertEqual(sale.quantita, 3)

    def test_create_sale_exceeding_quantity(self):
        """Verifica che non si possa vendere più dei disponibili"""
        with self.assertRaises(ValueError):
            create_sale(self.db, SaleCreate(
                prodotto_id=self.product.id,
                quantita=50,  # maggiore dei disponibili
                cliente="Luca Bianchi",
                data_vendita=date.today(),
                metodo_pagamento="carta di credito",
                stato="confermato"
            ))

if __name__ == "__main__":
    unittest.main()