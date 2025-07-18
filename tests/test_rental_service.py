import unittest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base
from app.models.rental import Rental
from app.schemas.rental_schema import RentalCreate
from app.services.rental_service import create_rental, conclude_rental

class TestRentalService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Usa un DB SQLite in memoria per i test
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        cls.Session = sessionmaker(bind=engine)

    def setUp(self):
        self.db = self.Session()

    def tearDown(self):
        self.db.close()

    def test_create_rental_success(self):
        rental = create_rental(self.db, RentalCreate(
            prodotto_id=1,
            quantita=2,
            cliente="Mario Rossi",
            data_inizio=date.today(),
            data_fine=date.today(),
            stato="in corso",  # Stringa valida
            metodo_pagamento="contanti"
        ))
        self.assertIsInstance(rental, Rental)
        self.assertEqual(rental.stato, "in corso")
        self.assertEqual(rental.quantita, 2)

    def test_conclude_rental(self):
        rental = create_rental(self.db, RentalCreate(
            prodotto_id=1,
            quantita=1,
            cliente="Luca Bianchi",
            data_inizio=date.today(),
            data_fine=date.today(),
            stato="in corso",  # Stringa valida
            metodo_pagamento="paypal"
        ))
        concluded = conclude_rental(self.db, rental.id)
        self.assertEqual(concluded.stato, "concluso")

if __name__ == "__main__":
    unittest.main()