import json
import hashlib
import uuid
from datetime import datetime
import os

USERS_FILE = os.path.join(os.path.dirname(__file__), '../data/users.json')

def _load_users():
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def _save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class FileUserManager:
    def create_user(self, username, email, password, preferences):
        users = _load_users()
        for user in users.values():
            if user['username'] == username:
                return None
        user_id = str(uuid.uuid4())
        users[user_id] = {
            'user_id': user_id,
            'username': username,
            'email': email,
            'password_hash': hash_password(password),
            'preferences': preferences,
            'created_at': datetime.now().isoformat()
        }
        _save_users(users)
        return users[user_id]

    def authenticate_user(self, username, password):
        users = _load_users()
        for user in users.values():
            if user['username'] == username and user['password_hash'] == hash_password(password):
                return user
        return None

    def update_user_preferences(self, user_id, preferences):
        users = _load_users()
        if user_id in users:
            users[user_id]['preferences'] = preferences
            _save_users(users)
            return True
        return False

    def update_user_account(self, user_id, email, current_password, new_password=None):
        users = _load_users()
        if user_id in users:
            user = users[user_id]
            if user['password_hash'] != hash_password(current_password):
                return False
            user['email'] = email
            if new_password:
                user['password_hash'] = hash_password(new_password)
            _save_users(users)
            return True
        return False
