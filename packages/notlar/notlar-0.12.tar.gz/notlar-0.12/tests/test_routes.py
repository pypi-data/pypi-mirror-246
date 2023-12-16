import unittest
from datetime import datetime
from flask import Flask, jsonify
from flask_testing import TestCase
from notlar import app, db
from notlar.models import User, Note

class NotlarTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()
        user = User(email='test@example.com', name='Test User', password='test_password')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_notes_authenticated(self):
        # Assuming you have a valid note in the test database for the given date
        with self.client:
            self.client.post('/login', data=dict(email='test@example.com', password='test_password'))
            response = self.client.get('/get_notes?date=2023-01-01')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertGreater(len(data), 0)

    def test_get_notes_unauthenticated(self):
        with self.client:
            response = self.client.get('/get_notes?date=2023-01-01')
            data = response.get_json()
            self.assertEqual(response.status_code, 401)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'User not authenticated')

    # Similar tests can be written for other routes

if __name__ == '__main__':
    unittest.main()
