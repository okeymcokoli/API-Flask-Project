# API FLask Project - Patterns

This repository contains two simple Flask API applications: one designed with security best practices and another intentionally including vulnerabilities for educational purposes.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Secure API](#secure-api)
- [Insecure API](#insecure-api)
- [Docker Compose](#docker-compose)
- [Getting Started](#getting-started)
- [Endpoints](#endpoints)
- [Security Practices](#security-practices)
- [Demonstrating Vulnerabilities](#demonstrating-vulnerabilities)

- [Contributing](#contributing)
- [License](#license)

### Prerequisites

- Docker
- Docker Compose

### Secure API

The secure API is designed with security best practices, including authentication, input validation, and HTTPS usage. It serves as an example of a secure Flask API implementation.

### Insecure API

The insecure API intentionally includes vulnerabilities for educational purposes. It should not be used in a production environment.

## Docker Compose

To easily deploy both API applications using Docker Compose, follow the instructions below.

### Getting Started

1. Clone the repository:
   git clone https://github.com/AdekunleAdeniran/Poison-Garden-API.git

2. cd Poison-Garden-API
   (Optional but suggested)
   python3 -m venv venv
   source venv/bin/activate

3. docker-compose up

   If errors:

   pip install --upgrade Werkzeug
   pip install --upgrade Flask
   pip install --upgrade Flask-SQLAlchemy

### Endpoints

Both APIs provide CRUD functionality for managing user records. Detailed documentation on API endpoints can be found in the respective app.py file

The secure API will be accessible at http://localhost:5001, and the insecure API will be accessible at http://localhost:5002.

### Security Practices

The secure API incorporates the following security practices:

Authentication and Authorization
Input Validation
Password Hashing

These are not properly implemented in the insecure app

### Demonstrating Vulnerabilities

#### Add user without any tokens

`curl -X POST -H "Content-Type: application/json" -d '{"username": "new_user", "password": "new_password"}' http://127.0.0.1:5002/insecure_users`

### Unauthenticated Access

#### Get all user data

`curl -X GET http://127.0.0.1:5002/insecure_users `

#### Get single user data

`curl -X GET http://127.0.0.1:5002/insecure_user/2`

#### Ignoring Input Validation

`bash curl -X POST -H "Content-Type: application/json" -d '{"username": "malicious_user"; DROP TABLE users --", "password": "password"}' http://127.0.0.1:5002/insecure_users`

#### Drop table

`curl -X PUT -H "Content-Type: application/json" -d '{"username": "attacker", "password": "'\''; DROP TABLE user_insecure; --"}' http://127.0.0.1:5002/insecure_users`

#### Password stored in plain text

`curl -X GET http://127.0.0.1:5002/insecure_user/2`
If password wasn't exposed in API end point, you could also check it directly from the table

`sqlite3 insecure-api/users_insecure.db`
`SELECT * FROM user_insecure;`

## Register a new user

`curl -X POST -H "Content-Type: application/json" -d '{"username": "new_user", "password": "new_password"}' http://localhost:5001/register`

## Authenticate and obtain JWT

`curl -X POST -H "Content-Type: application/json" -d '{"username": "new_user", "password": "new_password"}' http://localhost:5001/login`

## Use JWT to interact with use endpoint

Validating without authorization should fail
`curl -X GET http://127.0.0.1:5001/users`
`curl -X GET http://127.0.0.1:5001/user/1`

Use token obtaied to access endpoint
`curl -X GET -H "Authorization: Bearer <your_obtained_token>" http://localhost:5001/users`

## Contributing

Contributions are welcome! Feel free to open issues, submit pull requests, or provide suggestions to improve this project.

## License

This project is licensed under the MIT License.
