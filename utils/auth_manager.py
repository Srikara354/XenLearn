import hashlib
import json
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
import streamlit as st
from .database import DatabaseManager

class AuthManager:
    """Handles user authentication and account management"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username: str, email: str, password: str, preferences: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new user account"""
        try:
            # Check if username already exists
            existing_user = self.db.get_user_by_username(username)
            if existing_user:
                return None
            
            user_id = str(uuid.uuid4())
            hashed_password = self._hash_password(password)
            
            user_data = {
                'user_id': user_id,
                'username': username,
                'email': email,
                'password_hash': hashed_password,
                'preferences': json.dumps(preferences)
            }
            
            if self.db.create_user(user_data):
                # Initialize user stats
                stats = {
                    'total_points': 0,
                    'current_level': 1,
                    'streak_days': 0,
                    'time_studied_today': 0,
                    'daily_goal_minutes': preferences.get('daily_goal_minutes', 30),
                    'last_activity_date': datetime.now().date(),
                    'total_study_time': 0
                }
                self.db.update_user_stats(user_id, stats)
                
                # Return user data without password hash
                return {
                    'user_id': user_id,
                    'username': username,
                    'email': email,
                    'preferences': preferences
                }
            
            return None
            
        except Exception as e:
            st.error(f"Error creating user: {str(e)}")
            return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with username and password"""
        try:
            user_data = self.db.get_user_by_username(username)
            if not user_data:
                return None
            
            hashed_password = self._hash_password(password)
            
            if user_data['password_hash'] == hashed_password and user_data['is_active']:
                # Update last login
                self.db.update_user_login(username)
                
                # Parse preferences from JSON
                preferences = {}
                if user_data.get('preferences'):
                    try:
                        preferences = json.loads(user_data['preferences'])
                    except:
                        preferences = {}
                
                # Return user data without password hash
                return {
                    'user_id': user_data['user_id'],
                    'username': user_data['username'],
                    'email': user_data['email'],
                    'preferences': preferences
                }
            
            return None
            
        except Exception as e:
            st.error(f"Error authenticating user: {str(e)}")
            return None
    
    def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> bool:
        """Update user learning preferences"""
        try:
            return self.db.update_user_preferences(user_id, preferences)
            
        except Exception as e:
            st.error(f"Error updating preferences: {str(e)}")
            return False
    
    def update_user_account(self, user_id: str, email: str, current_password: str, new_password: str = None) -> bool:
        """Update user account information"""
        try:
            user_data = self.db.get_user_by_id(user_id)
            if not user_data:
                return False
            
            # Verify current password
            if self._hash_password(current_password) != user_data['password_hash']:
                return False
            
            # Update email
            query = "UPDATE users SET email = :email"
            params = {"email": email, "user_id": user_id}
            
            # Update password if provided
            if new_password:
                query += ", password_hash = :password_hash"
                params["password_hash"] = self._hash_password(new_password)
            
            query += " WHERE user_id = :user_id"
            
            return self.db.execute_update(query, params)
            
        except Exception as e:
            st.error(f"Error updating account: {str(e)}")
            return False
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user data by user ID"""
        try:
            user_data = self.db.get_user_by_id(user_id)
            if user_data:
                # Parse preferences and remove password hash
                preferences = {}
                if user_data.get('preferences'):
                    try:
                        preferences = json.loads(user_data['preferences'])
                    except:
                        preferences = {}
                
                return {
                    'user_id': user_data['user_id'],
                    'username': user_data['username'],
                    'email': user_data['email'],
                    'preferences': preferences
                }
            return None
            
        except Exception as e:
            st.error(f"Error retrieving user: {str(e)}")
            return None