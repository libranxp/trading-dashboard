import json, os
from werkzeug.security import generate_password_hash, check_password_hash

USER_FILE = "auth/users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = generate_password_hash(password)
    save_users(users)
    return True

def validate_login(username, password):
    users = load_users()
    if username not in users:
        return False
    return check_password_hash(users[username], password)
