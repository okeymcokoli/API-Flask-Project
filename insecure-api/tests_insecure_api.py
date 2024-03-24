import unittest
from flask import json
from app import app


class InsecureAppTests(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_get_user(self):
        response = self.app.get('/insecure_user/1')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 404)
        self.assertIn('message', data)

    def test_get_users(self):
        response = self.app.get('/insecure_users')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertIn('users', data)
        self.assertIsInstance(data['users'], list)

    def test_create_user(self):
        user_data = {'username': 'test_user', 'password': 'test_password'}
        response = self.app.post('/insecure_users', json=user_data)
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'User created successfully')

    def test_update_user(self):
        user_data = {'username': 'updated_user',
                     'password': 'updated_password'}
        response = self.app.put('/insecure_user/1', json=user_data)
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'User updated successfully')

    def test_delete_user(self):
        response = self.app.delete('/insecure_user/1')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'User deleted successfully')


if __name__ == '__main__':
    unittest.main()
