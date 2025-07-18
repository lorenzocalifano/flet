import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base
from app.services.damage_service import report_damage, count_damages_for_product
from app.schemas.damage_schema import DamageCreate
from datetime import date

class TestDamageService(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        self.Session = sessionmaker(bind=engine)
        self.db = self.Session()

    def tearDown(self):
        self.db.close()

    def test_report_damage_success(self):
        damage = report_damage(self.db, DamageCreate(
            prodotto_id=1, descrizione="Danno test", data_segnalazione=date.today()))
        self.assertIsNotNone(damage.id)

    def test_count_damages_for_product(self):
        report_damage(self.db, DamageCreate(
            prodotto_id=1, descrizione="Danno", data_segnalazione=date.today()))
        count = count_damages_for_product(self.db, 1)
        self.assertEqual(count, 1)

if __name__ == "__main__":
    unittest.main()