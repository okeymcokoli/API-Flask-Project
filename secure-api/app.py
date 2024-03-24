from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_TOKEN_LOCATION'] = ['headers']

db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)


# User registration logic
def register_user(username, password):
    if not username or not password:
        return {'message': 'Username and password are required'}, 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return {'message': 'Username already exists'}, 400

    # Password validation
    if len(password) < 8:
        return {'message': 'Password must be at least 8 characters long'}, 400

    # Hash the password before storing it
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Create a new user
    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    # Generate an access token for the newly registered user
    access_token = create_access_token(identity=username)

    return {'message': 'User created successfully', 'access_token': access_token}, 201


class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        registration_result = register_user(username, password)

        return registration_result


class UserResource(Resource):
    @jwt_required()
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return {'id': user.id, 'username': user.username}

    @jwt_required()
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        data = request.get_json()

        # username validation
        # Additional validation checks
        if 'username' not in data or 'password' not in data:
            return {'message': 'Username and password are required in the update request'}, 400

        user.username = data['username']
        user.password_hash = generate_password_hash(
            data['password'], method='sha256')
        db.session.commit()
        return {'message': 'User updated successfully'}

    @jwt_required()
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}


class UserListResource(Resource):
    @jwt_required()
    def get(self):
        users = User.query.all()
        user_list = [{'id': user.id, 'username': user.username}
                     for user in users]
        return {'users': user_list}

    @jwt_required()
    def post(self):
        data = request.get_json()

        # Additional validation checks
        if 'username' not in data or 'password' not in data:
            return {'message': 'Username and password are required for user creation'}, 400

        if len(data['password']) < 8:
            return {'message': 'Password must be at least 8 characters long'}, 400

        new_user = User(username=data['username'], password_hash=generate_password_hash(
            data['password'], method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created successfully'}


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=username)
        return {'access_token': access_token}, 200
    else:
        return {'message': 'Invalid credentials'}, 401


api.add_resource(UserResource, '/user/<int:user_id>')
api.add_resource(UserListResource, '/users')
api.add_resource(RegisterResource, '/register')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5001)
