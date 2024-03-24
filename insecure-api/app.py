from flask import Flask, request, jsonify, g
from flask_restful import Api, Resource
import sqlite3

app = Flask(__name__)
api = Api(app)

DATABASE = 'users_insecure.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_insecure (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            );
        ''')
        db.commit()


@app.before_request
def before_first_request():
    init_db()
    print('Database initialized.')


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


class InsecureUserResource(Resource):
    def get(self, user_id):
        query = f"SELECT * FROM user_insecure WHERE id = {user_id};"
        cursor = get_db().cursor()
        cursor.execute(query)
        user_data = cursor.fetchone()

        if user_data:
            return {'id': user_data[0], 'username': user_data[1], 'password': user_data[2]}
        else:
            return {'message': 'User not found'}, 404

    def put(self, user_id):
        # Retrieve raw JSON data from the request body
        data = request.get_json()

        # Extract username and password from the JSON data
        username = data.get('username')
        password = data.get('password')

        # Use the data directly in the SQL query without sanitization (for demonstration purposes only)
        query = f"UPDATE user_insecure SET username='{username}', password='{password}' WHERE id = {user_id};"
        print(f"Generated Query: {query}")
        cursor = get_db().cursor()
        cursor.execute(query)
        get_db().commit()

        return {'message': 'User updated successfully'}

    def delete(self, user_id):
        query = f"DELETE FROM user_insecure WHERE id = {user_id};"
        cursor = get_db().cursor()
        cursor.execute(query)
        get_db().commit()

        return {'message': 'User deleted successfully'}


class InsecureUserListResource(Resource):
    def get(self):
        query = "SELECT * FROM user_insecure;"
        cursor = get_db().cursor()
        cursor.execute(query)
        users = [{'id': row[0], 'username': row[1], 'password': row[2]}
                 for row in cursor.fetchall()]

        return {'users': users}

    def post(self):
        data = request.get_json()
        query = f"INSERT INTO user_insecure (username, password) VALUES ('{data['username']}', '{data['password']}');"
        cursor = get_db().cursor()
        cursor.execute(query)
        get_db().commit()

        return {'message': 'User created successfully'}


api.add_resource(InsecureUserResource, '/insecure_user/<int:user_id>')
api.add_resource(InsecureUserListResource, '/insecure_users')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
