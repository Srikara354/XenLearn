import hashlib
import json
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
import streamlit as st

class AuthManager:
    """Handles user authentication and account management"""
    
    def __init__(self):
        self.users_file = "data/users.json"
        self._ensure_data_directory()
        self._load_users()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        import os
        if not os.path.exists("data"):
            os.makedirs("data")
    
    def _load_users(self):
        """Load users from JSON file"""
        try:
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            self.users = {}
            self._save_users()
    
    def _save_users(self):
        """Save users to JSON file"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=2, default=str)
        except Exception as e:
            st.error(f"Error saving user data: {str(e)}")
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username: str, email: str, password: str, preferences: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new user account"""
        try:
            # Check if username already exists
            if username in self.users:
                return None
            
            user_id = str(uuid.uuid4())
            hashed_password = self._hash_password(password)
            
            user_data = {
                'user_id': user_id,
                'username': username,
                'email': email,
                'password_hash': hashed_password,
                'preferences': preferences,
                'created_at': datetime.now().isoformat(),
                'last_login': None,
                'is_active': True
            }
            
            self.users[username] = user_data
            self._save_users()
            
            # Return user data without password hash
            user_return = user_data.copy()
            del user_return['password_hash']
            return user_return
            
        except Exception as e:
            st.error(f"Error creating user: {str(e)}")
            return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with username and password"""
        try:
            if username not in self.users:
                return None
            
            user_data = self.users[username]
            hashed_password = self._hash_password(password)
            
            if user_data['password_hash'] == hashed_password and user_data['is_active']:
                # Update last login
                user_data['last_login'] = datetime.now().isoformat()
                self.users[username] = user_data
                self._save_users()
                
                # Return user data without password hash
                user_return = user_data.copy()
                del user_return['password_hash']
                return user_return
            
            return None
            
        except Exception as e:
            st.error(f"Error authenticating user: {str(e)}")
            return None
    
    def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> bool:
        """Update user learning preferences"""
        try:
            for username, user_data in self.users.items():
                if user_data['user_id'] == user_id:
                    user_data['preferences'] = preferences
                    user_data['updated_at'] = datetime.now().isoformat()
                    self.users[username] = user_data
                    self._save_users()
                    return True
            return False
            
        except Exception as e:
            st.error(f"Error updating preferences: {str(e)}")
            return False
    
    def update_user_account(self, user_id: str, email: str, current_password: str, new_password: str = None) -> bool:
        """Update user account information"""
        try:
            for username, user_data in self.users.items():
                if user_data['user_id'] == user_id:
                    # Verify current password
                    if self._hash_password(current_password) != user_data['password_hash']:
                        return False
                    
                    # Update email
                    user_data['email'] = email
                    
                    # Update password if provided
                    if new_password:
                        user_data['password_hash'] = self._hash_password(new_password)
                    
                    user_data['updated_at'] = datetime.now().isoformat()
                    self.users[username] = user_data
                    self._save_users()
                    return True
            return False
            
        except Exception as e:
            st.error(f"Error updating account: {str(e)}")
            return False
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user data by user ID"""
        try:
            for user_data in self.users.values():
                if user_data['user_id'] == user_id:
                    user_return = user_data.copy()
                    del user_return['password_hash']
                    return user_return
            return None
            
        except Exception as e:
            st.error(f"Error retrieving user: {str(e)}")
            return None
    
    def deactivate_user(self, user_id: str) -> bool:
        """Deactivate a user account"""
        try:
            for username, user_data in self.users.items():
                if user_data['user_id'] == user_id:
                    user_data['is_active'] = False
                    user_data['deactivated_at'] = datetime.now().isoformat()
                    self.users[username] = user_data
                    self._save_users()
                    return True
            return False
            
        except Exception as e:
            st.error(f"Error deactivating user: {str(e)}")
            return False
    
    def get_all_users_stats(self) -> Dict[str, Any]:
        """Get overall user statistics"""
        try:
            total_users = len(self.users)
            active_users = sum(1 for user in self.users.values() if user.get('is_active', True))
            
            # Count users by learning style
            learning_styles = {}
            for user in self.users.values():
                style = user.get('preferences', {}).get('learning_style', 'Unknown')
                learning_styles[style] = learning_styles.get(style, 0) + 1
            
            return {
                'total_users': total_users,
                'active_users': active_users,
                'learning_styles_distribution': learning_styles,
                'registration_dates': [user.get('created_at') for user in self.users.values()]
            }
            
        except Exception as e:
            st.error(f"Error getting user statistics: {str(e)}")
            return {}