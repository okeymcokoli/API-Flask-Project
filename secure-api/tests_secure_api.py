import unittest
from flask_testing import TestCase
from app import app, db, User, register_user


class TestApp(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_users.db'
        return app

    def setUp(self):
        with app.app_context():
            db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_registration(self):
        response = self.client.post(
            '/register', json={'username': 'testuser', 'password': 'testpassword'})
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertIn('access_token', data)

    def test_duplicate_user_registration(self):
        # Register a user
        self.client.post(
            '/register', json={'username': 'testuser', 'password': 'testpassword'})

        # Try to register the same user again
        response = self.client.post(
            '/register', json={'username': 'testuser', 'password': 'testpassword'})
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Username already exists')

    def test_user_login(self):
        # Register a user
        self.client.post(
            '/register', json={'username': 'testuser', 'password': 'testpassword'})

        # Log in with the registered user
        response = self.client.post(
            '/login', json={'username': 'testuser', 'password': 'testpassword'})
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', data)

    def test_invalid_user_login(self):
        # Log in with an unregistered user
        response = self.client.post(
            '/login', json={'username': 'nonexistentuser', 'password': 'testpassword'})
        data = response.get_json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message'], 'Invalid credentials')


if __name__ == '__main__':
    unittest.main()
