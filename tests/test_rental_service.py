import unittest
from datetime import date, timedelta
from app.models.database import SessionLocal, Base, engine
from app.models.rental import Rental
from app.models.product import Product
from app.schemas.rental_schema import RentalCreate
from app.services.rental_service import create_rental, update_rental, cancel_rental, conclude_rental

class TestRentalService(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()
        self.db.query(Rental).delete()
        self.db.query(Product).delete()
        self.db.commit()
        self.prodotto = Product(nome="Prodotto Test", categoria="Audio", quantita=10)
        self.db.add(self.prodotto)
        self.db.commit()
        self.db.refresh(self.prodotto)

    def tearDown(self):
        self.db.close()

    def test_create_rental_success(self):
        rental = create_rental(self.db, RentalCreate(
            prodotto_id=self.prodotto.id,
            quantita=2,
            cliente="Cliente Test",
            data_inizio=date.today(),
            data_fine=date.today() + timedelta(days=5),
            stato="in corso",
            metodo_pagamento="paypal"
        ))
        self.assertEqual(rental.quantita, 2)

    def test_create_rental_exceeding_quantity(self):
        with self.assertRaises(ValueError):
            create_rental(self.db, RentalCreate(
                prodotto_id=self.prodotto.id,
                quantita=50,
                cliente="Cliente Test",
                data_inizio=date.today(),
                data_fine=date.today() + timedelta(days=5),
                stato="in corso",
                metodo_pagamento="paypal"
            ))

    def test_update_rental_success(self):
        rental = create_rental(self.db, RentalCreate(
            prodotto_id=self.prodotto.id,
            quantita=1,
            cliente="Cliente Test",
            data_inizio=date.today(),
            data_fine=date.today() + timedelta(days=5),
            stato="in corso",
            metodo_pagamento="paypal"
        ))
        updated = update_rental(self.db, rental.id, quantita=2)
        self.assertEqual(updated.quantita, 2)

    def test_update_rental_exceeding_quantity(self):
        rental = create_rental(self.db, RentalCreate(
            prodotto_id=self.prodotto.id,
            quantita=1,
            cliente="Cliente Test",
            data_inizio=date.today(),
            data_fine=date.today() + timedelta(days=5),
            stato="in corso",
            metodo_pagamento="paypal"
        ))
        with self.assertRaises(ValueError):
            update_rental(self.db, rental.id, quantita=50)

    def test_cancel_rental(self):
        rental = create_rental(self.db, RentalCreate(
            prodotto_id=self.prodotto.id,
            quantita=1,
            cliente="Cliente Test",
            data_inizio=date.today(),
            data_fine=date.today() + timedelta(days=5),
            stato="in corso",
            metodo_pagamento="paypal"
        ))
        canceled = cancel_rental(self.db, rental.id)
        self.assertEqual(canceled.stato, "annullato")

    def test_conclude_rental(self):
        rental = create_rental(self.db, RentalCreate(
            prodotto_id=self.prodotto.id,
            quantita=1,
            cliente="Cliente Test",
            data_inizio=date.today(),
            data_fine=date.today() + timedelta(days=5),
            stato="in corso",
            metodo_pagamento="paypal"
        ))
        concluded = conclude_rental(self.db, rental.id)
        self.assertEqual(concluded.stato, "concluso")


if __name__ == "__main__":
    unittest.main()