import unittest
from app.models.database import SessionLocal, Base, engine
from app.services.product_service import create_product, get_product_by_id, get_all_products, update_product_quantity
from app.schemas.product_schema import ProductCreate
from app.models.product import Product

class TestProductService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Creazione tabelle in un database temporaneo per i test
        Base.metadata.create_all(bind=engine)

    def setUp(self):
        # Pulizia database ad ogni test
        self.db = SessionLocal()
        self.db.query(Product).delete()
        self.db.commit()

    def tearDown(self):
        self.db.close()

    def test_create_product_with_potenza(self):
        """Verifica che un prodotto venga creato correttamente con la potenza (W)"""
        prodotto = create_product(
            self.db,
            ProductCreate(
                nome="Mixer Pro",
                categoria="Audio",
                quantita=10,
                modello="Pro 200",
                dimensione="Medio",
                brand="Yamaha",
                potenza=500
            )
        )
        self.assertIsNotNone(prodotto.id)
        self.assertEqual(prodotto.potenza, 500)

    def test_get_all_products_with_potenza(self):
        """Verifica che la potenza sia restituita correttamente tra tutti i prodotti"""
        create_product(
            self.db,
            ProductCreate(
                nome="Speaker Max",
                categoria="Audio",
                quantita=15,
                modello="Max 300",
                dimensione="Grande",
                brand="JBL",
                potenza=1200
            )
        )
        prodotti = get_all_products(self.db)
        self.assertGreater(len(prodotti), 0)
        self.assertTrue(any(p.potenza == 1200 for p in prodotti))

    def test_update_product_quantity_and_check_potenza(self):
        """Verifica che l'aggiornamento della quantità non modifichi la potenza del prodotto"""
        prodotto = create_product(
            self.db,
            ProductCreate(
                nome="Amplificatore Lite",
                categoria="Audio",
                quantita=8,
                modello="Lite 100",
                dimensione="Piccolo",
                brand="Behringer",
                potenza=350
            )
        )
        update_product_quantity(self.db, prodotto.id, 20)
        prodotto_modificato = get_product_by_id(self.db, prodotto.id)

        self.assertEqual(prodotto_modificato.quantita, 20)
        self.assertEqual(prodotto_modificato.potenza, 350)

if __name__ == "__main__":
    unittest.main()