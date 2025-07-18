import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base
from app.services.sale_service import create_sale, get_all_sales
from app.schemas.sale_schema import SaleCreate
from datetime import date

class TestSaleService(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        self.Session = sessionmaker(bind=engine)
        self.db = self.Session()

    def tearDown(self):
        self.db.close()

    def test_create_sale_success(self):
        sale = create_sale(self.db, SaleCreate(
            prodotto_id=1, quantita=1, cliente="Luca", data_vendita=date.today(),
            metodo_pagamento="carta"))
        self.assertEqual(sale.stato, "confermato")

    def test_get_all_sales(self):
        create_sale(self.db, SaleCreate(
            prodotto_id=1, quantita=1, cliente="Luca", data_vendita=date.today()))
        sales = get_all_sales(self.db)
        self.assertEqual(len(sales), 1)

if __name__ == "__main__":
    unittest.main()