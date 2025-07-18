import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base
from app.services.notification_service import create_notification, mark_notification_as_read, get_unread_notifications

class TestNotificationService(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        self.Session = sessionmaker(bind=engine)
        self.db = self.Session()

    def tearDown(self):
        self.db.close()

    def test_create_notification_success(self):
        notif = create_notification(self.db, messaggio="Test", tipo="info")
        self.assertEqual(notif.letto, 0)

    def test_mark_notification_as_read(self):
        notif = create_notification(self.db, messaggio="Test", tipo="info")
        mark_notification_as_read(self.db, notif.id)
        self.assertEqual(notif.letto, 1)

    def test_get_unread_notifications(self):
        create_notification(self.db, messaggio="Test", tipo="info")
        unread = get_unread_notifications(self.db)
        self.assertEqual(len(unread), 1)

if __name__ == "__main__":
    unittest.main()