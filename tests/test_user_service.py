import unittest
from app.models.database import SessionLocal, Base, engine
from app.services.user_service import create_user, delete_user, get_all_users
from app.schemas.user_schema import UserCreate, UserRole

class TestUserService(unittest.TestCase):

    def setUp(self):
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()
        self.db.query(get_all_users.__globals__['User']).delete()
        self.db.commit()

    def tearDown(self):
        self.db.close()

    def test_create_and_delete_user(self):
        user = create_user(self.db, UserCreate(
            nome="Mario",
            cognome="Bianchi",
            email="mario.bianchi@test.com",
            password="123456",
            ruolo=UserRole.SEGRETERIA
        ))
        self.assertIsNotNone(user.id)
        self.assertEqual(user.email, "mario.bianchi@test.com")

        delete_user(self.db, user.id)
        users = get_all_users(self.db)
        self.assertEqual(len(users), 0)

if __name__ == "__main__":
    unittest.main()