from unittest import TestCase
from model import Campsite, Request, User, connect_to_db, db
from server import app
import server

class FlaskTests(TestCase):
    def setUp(self):
        """To do before every test."""

        self.client = app.test_client()
        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        # Connect to test database
        connect_to_db(app)
        db.create_all()

    def test_homepage(self):
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)

    def test_date_selector(self):
        result = self.client.get("/dates")
        self.assertIn(b"When would you like to go", result.data)

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        # db.drop_all()

    def test_find_user(self):

        brittany = User.query.filter(User.phone == "2197188608").first()
        self.assertEqual(brittany.phone, "2197188608")

    def test_find_campsite(self):

        jtree = Campsite.query.filter(Campsite.name == "Tuolumne Meadows").first()
        self.assertEqual(jtree.name, "Tuolumne Meadows")

if __name__ == "__main__":
    import unittest

    unittest.main()
