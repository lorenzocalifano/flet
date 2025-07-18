import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base
from app.models.user import UserRole
from app.schemas.user_schema import UserCreate
from app.services.user_service import create_user, update_user_role

class TestUserService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        cls.Session = sessionmaker(bind=engine)

    def setUp(self):
        self.db = self.Session()

    def tearDown(self):
        self.db.close()

    def test_update_user_role(self):
        user = create_user(self.db, UserCreate(
            nome="Mario",
            cognome="Rossi",
            email="test@test.com",
            password="123456",
            ruolo=UserRole.SEGRETERIA
        ))
        updated_user = update_user_role(self.db, user.id, UserRole.MAGAZZINIERE)
        self.assertEqual(updated_user.ruolo.value, UserRole.MAGAZZINIERE.value)

if __name__ == "__main__":
    unittest.main()