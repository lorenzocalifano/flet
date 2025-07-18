import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base
from app.services.auth_service import register_user, authenticate_user
from app.schemas.user_schema import UserCreate, UserRole
from sqlalchemy.exc import IntegrityError

class TestAuthService(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        self.Session = sessionmaker(bind=engine)
        self.db = self.Session()

    def tearDown(self):
        self.db.close()

    def test_register_user_success(self):
        user = register_user(self.db, UserCreate(
            nome="Test", cognome="User", email="test@test.com", password="123456", ruolo=UserRole.RESPONSABILE))
        self.assertIsNotNone(user.id)

    def test_register_user_duplicate_email(self):
        register_user(self.db, UserCreate(
            nome="Test", cognome="User", email="dup@test.com", password="123456", ruolo=UserRole.RESPONSABILE))
        with self.assertRaises(ValueError):
            register_user(self.db, UserCreate(
                nome="Dup", cognome="User", email="dup@test.com", password="123456", ruolo=UserRole.RESPONSABILE))

    def test_authenticate_user_success(self):
        register_user(self.db, UserCreate(
            nome="Test", cognome="User", email="auth@test.com", password="123456", ruolo=UserRole.SEGRETERIA))
        user = authenticate_user(self.db, "auth@test.com", "123456")
        self.assertIsNotNone(user)

    def test_authenticate_user_wrong_password(self):
        register_user(self.db, UserCreate(
            nome="Test", cognome="User", email="wrong@test.com", password="123456", ruolo=UserRole.MAGAZZINIERE))
        user = authenticate_user(self.db, "wrong@test.com", "wrongpass")
        self.assertIsNone(user)

if __name__ == "__main__":
    unittest.main()