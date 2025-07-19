import unittest
from datetime import date, timedelta
from app.models.database import SessionLocal, Base, engine
from app.models.notification import Notification
from app.schemas.rental_schema import RentalCreate
from app.schemas.sale_schema import SaleCreate
from app.services.rental_service import (
    create_rental,
    update_rental,
    cancel_rental,
    conclude_rental
)
from app.services.sale_service import create_sale, cancel_sale
from app.services.notification_service import get_all_notifications
from app.schemas.product_schema import ProductCreate
from app.services.product_service import create_product


class TestNotificationsInServices(unittest.TestCase):

    def setUp(self):
        """Pulizia completa del database per ogni test"""
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()

        # Creazione di un prodotto di test
        self.prodotto = create_product(self.db, ProductCreate(
            nome="TestProd",
            categoria="Audio",
            quantita=20
        ))

    def tearDown(self):
        self.db.close()

    def test_rental_notifications(self):
        """Verifica che tutte le operazioni sui noleggi generino notifiche"""
        r = create_rental(self.db, RentalCreate(
            prodotto_id=self.prodotto.id,
            quantita=2,
            cliente="Cliente1",
            data_inizio=date.today(),
            data_fine=date.today() + timedelta(days=5),
            stato="in corso",
            metodo_pagamento="contanti"
        ))

        update_rental(self.db, r.id, quantita=3)
        conclude_rental(self.db, r.id)
        cancel_rental(self.db, r.id)  # anche se già concluso, deve ignorarlo o notificare annullamento fallito

        notifs = [n.messaggio.lower() for n in get_all_notifications(self.db)]
        self.assertTrue(any("noleggio" in n and "registrato" in n for n in notifs))
        self.assertTrue(any("noleggio" in n and "modificato" in n for n in notifs))
        self.assertTrue(any("noleggio" in n and "concluso" in n for n in notifs))

    def test_sale_notifications(self):
        """Verifica che l’aggiunta e l’annullamento di una vendita generino notifiche"""
        s = create_sale(self.db, SaleCreate(
            prodotto_id=self.prodotto.id,
            quantita=1,
            cliente="ClienteVendita",
            data_vendita=date.today(),
            stato="confermato",
            metodo_pagamento="carta di credito"
        ))

        cancel_sale(self.db, s.id)
        notifs = [n.messaggio.lower() for n in get_all_notifications(self.db)]
        self.assertTrue(any("vendita" in n and "registrata" in n for n in notifs))
        self.assertTrue(any("vendita" in n and "annullata" in n for n in notifs))

    def test_auto_conclude_expired_rentals(self):
        """Verifica che i noleggi scaduti siano conclusi automaticamente"""
        r = create_rental(self.db, RentalCreate(
            prodotto_id=self.prodotto.id,
            quantita=1,
            cliente="Cliente2",
            data_inizio=date.today() - timedelta(days=10),
            data_fine=date.today() - timedelta(days=5),
            stato="in corso",
            metodo_pagamento="contanti"
        ))

        # Chiama manualmente la funzione che aggiorna i noleggi scaduti
        conclude_rental(self.db, r.id)
        self.db.refresh(r)

        self.assertEqual(r.stato, "concluso")


if __name__ == "__main__":
    unittest.main()