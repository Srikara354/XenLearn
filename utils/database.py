import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import psycopg2

class DatabaseManager:
    """Manages PostgreSQL database operations for the learning platform"""
    
    def __init__(self):
        self.database_url = os.environ.get('DATABASE_URL')
        self.engine = None
        self.Session = None
        self._initialize_connection()
        self._create_tables()
    
    def _initialize_connection(self):
        """Initialize database connection"""
        try:
            if not self.database_url:
                st.error("Database URL not found. Please ensure PostgreSQL is configured.")
                return
                
            self.engine = create_engine(self.database_url)
            self.Session = sessionmaker(bind=self.engine)
            
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                
        except Exception as e:
            st.error(f"Failed to connect to database: {str(e)}")
    
    def _create_tables(self):
        """Create all necessary tables for the learning platform"""
        try:
            with self.engine.connect() as conn:
                # Users table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id VARCHAR(36) PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        email VARCHAR(100) NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        preferences JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP,
                        is_active BOOLEAN DEFAULT TRUE
                    )
                """))
                
                # Courses table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS courses (
                        course_id VARCHAR(36) PRIMARY KEY,
                        title VARCHAR(200) NOT NULL,
                        description TEXT,
                        category VARCHAR(50),
                        difficulty VARCHAR(20),
                        estimated_hours INTEGER,
                        rating DECIMAL(3,2),
                        instructor VARCHAR(100),
                        tags TEXT[],
                        prerequisites TEXT[],
                        learning_outcomes TEXT[],
                        lessons JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Enrollments table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS enrollments (
                        enrollment_id SERIAL PRIMARY KEY,
                        user_id VARCHAR(36) REFERENCES users(user_id),
                        course_id VARCHAR(36) REFERENCES courses(course_id),
                        enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        progress_percentage DECIMAL(5,2) DEFAULT 0,
                        completed_at TIMESTAMP,
                        UNIQUE(user_id, course_id)
                    )
                """))
                
                # User progress table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS user_progress (
                        progress_id SERIAL PRIMARY KEY,
                        user_id VARCHAR(36) REFERENCES users(user_id),
                        course_id VARCHAR(36) REFERENCES courses(course_id),
                        lesson_id VARCHAR(36),
                        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        time_spent_minutes INTEGER DEFAULT 0,
                        UNIQUE(user_id, course_id, lesson_id)
                    )
                """))
                
                # Quiz results table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS quiz_results (
                        result_id SERIAL PRIMARY KEY,
                        user_id VARCHAR(36) REFERENCES users(user_id),
                        quiz_id VARCHAR(36),
                        topic VARCHAR(100),
                        difficulty VARCHAR(20),
                        score_percentage DECIMAL(5,2),
                        correct_answers INTEGER,
                        total_questions INTEGER,
                        user_answers JSONB,
                        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Achievements table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS user_achievements (
                        achievement_id SERIAL PRIMARY KEY,
                        user_id VARCHAR(36) REFERENCES users(user_id),
                        achievement_type VARCHAR(50),
                        title VARCHAR(100),
                        description TEXT,
                        points INTEGER,
                        earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # User interactions table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS user_interactions (
                        interaction_id SERIAL PRIMARY KEY,
                        user_id VARCHAR(36) REFERENCES users(user_id),
                        interaction_type VARCHAR(50),
                        course_id VARCHAR(36),
                        metadata JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # User stats table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS user_stats (
                        user_id VARCHAR(36) PRIMARY KEY REFERENCES users(user_id),
                        total_points INTEGER DEFAULT 0,
                        current_level INTEGER DEFAULT 1,
                        streak_days INTEGER DEFAULT 0,
                        time_studied_today INTEGER DEFAULT 0,
                        daily_goal_minutes INTEGER DEFAULT 30,
                        last_activity_date DATE,
                        total_study_time INTEGER DEFAULT 0
                    )
                """))
                
                conn.commit()
                
        except Exception as e:
            st.error(f"Error creating database tables: {str(e)}")
    
    def execute_query(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), params or {})
                columns = result.keys()
                return [dict(zip(columns, row)) for row in result.fetchall()]
        except Exception as e:
            st.error(f"Error executing query: {str(e)}")
            return []
    
    def execute_update(self, query: str, params: Dict[str, Any] = None) -> bool:
        """Execute an INSERT, UPDATE, or DELETE query"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text(query), params or {})
                conn.commit()
                return True
        except Exception as e:
            st.error(f"Error executing update: {str(e)}")
            return False
    
    # User management methods
    def create_user(self, user_data: Dict[str, Any]) -> bool:
        """Create a new user in the database"""
        query = """
            INSERT INTO users (user_id, username, email, password_hash, preferences)
            VALUES (:user_id, :username, :email, :password_hash, :preferences)
        """
        return self.execute_update(query, user_data)
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        query = "SELECT * FROM users WHERE username = :username"
        results = self.execute_query(query, {"username": username})
        return results[0] if results else None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        query = "SELECT * FROM users WHERE user_id = :user_id"
        results = self.execute_query(query, {"user_id": user_id})
        return results[0] if results else None
    
    def update_user_login(self, username: str) -> bool:
        """Update user's last login timestamp"""
        query = "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE username = :username"
        return self.execute_update(query, {"username": username})
    
    def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> bool:
        """Update user preferences"""
        query = "UPDATE users SET preferences = :preferences WHERE user_id = :user_id"
        return self.execute_update(query, {
            "user_id": user_id,
            "preferences": json.dumps(preferences)
        })
    
    # Course management methods
    def create_course(self, course_data: Dict[str, Any]) -> bool:
        """Create a new course"""
        query = """
            INSERT INTO courses (course_id, title, description, category, difficulty, 
                               estimated_hours, rating, instructor, tags, prerequisites, 
                               learning_outcomes, lessons)
            VALUES (:course_id, :title, :description, :category, :difficulty, 
                   :estimated_hours, :rating, :instructor, :tags, :prerequisites, 
                   :learning_outcomes, :lessons)
        """
        return self.execute_update(query, course_data)
    
    def get_all_courses(self) -> List[Dict[str, Any]]:
        """Get all courses"""
        query = "SELECT * FROM courses ORDER BY rating DESC"
        return self.execute_query(query)
    
    def get_course_by_id(self, course_id: str) -> Optional[Dict[str, Any]]:
        """Get course by ID"""
        query = "SELECT * FROM courses WHERE course_id = :course_id"
        results = self.execute_query(query, {"course_id": course_id})
        return results[0] if results else None
    
    def search_courses(self, search_term: str = "", category: str = "", difficulty: str = "") -> List[Dict[str, Any]]:
        """Search courses with filters"""
        query = "SELECT * FROM courses WHERE 1=1"
        params = {}
        
        if search_term:
            query += " AND (title ILIKE :search OR description ILIKE :search OR :search = ANY(tags))"
            params["search"] = f"%{search_term}%"
        
        if category and category != "All":
            query += " AND category = :category"
            params["category"] = category
        
        if difficulty and difficulty != "All":
            query += " AND difficulty = :difficulty"
            params["difficulty"] = difficulty
        
        query += " ORDER BY rating DESC"
        return self.execute_query(query, params)
    
    def get_course_categories(self) -> List[str]:
        """Get all unique course categories"""
        query = "SELECT DISTINCT category FROM courses ORDER BY category"
        results = self.execute_query(query)
        return [row["category"] for row in results]
    
    # Enrollment methods
    def enroll_user(self, user_id: str, course_id: str) -> bool:
        """Enroll user in a course"""
        query = """
            INSERT INTO enrollments (user_id, course_id)
            VALUES (:user_id, :course_id)
            ON CONFLICT (user_id, course_id) DO NOTHING
        """
        return self.execute_update(query, {"user_id": user_id, "course_id": course_id})
    
    def get_user_enrollments(self, user_id: str) -> List[str]:
        """Get course IDs user is enrolled in"""
        query = "SELECT course_id FROM enrollments WHERE user_id = :user_id"
        results = self.execute_query(query, {"user_id": user_id})
        return [row["course_id"] for row in results]
    
    def update_course_progress(self, user_id: str, course_id: str, progress: float) -> bool:
        """Update course progress percentage"""
        query = """
            UPDATE enrollments 
            SET progress_percentage = :progress,
                completed_at = CASE WHEN :progress >= 100 THEN CURRENT_TIMESTAMP ELSE completed_at END
            WHERE user_id = :user_id AND course_id = :course_id
        """
        return self.execute_update(query, {
            "user_id": user_id,
            "course_id": course_id,
            "progress": progress
        })
    
    # Progress tracking methods
    def record_lesson_completion(self, user_id: str, course_id: str, lesson_id: str, time_spent: int = 0) -> bool:
        """Record lesson completion"""
        query = """
            INSERT INTO user_progress (user_id, course_id, lesson_id, time_spent_minutes)
            VALUES (:user_id, :course_id, :lesson_id, :time_spent)
            ON CONFLICT (user_id, course_id, lesson_id) DO NOTHING
        """
        return self.execute_update(query, {
            "user_id": user_id,
            "course_id": course_id,
            "lesson_id": lesson_id,
            "time_spent": time_spent
        })
    
    def get_user_completed_lessons(self, user_id: str, course_id: str) -> List[str]:
        """Get completed lesson IDs for a course"""
        query = """
            SELECT lesson_id FROM user_progress 
            WHERE user_id = :user_id AND course_id = :course_id
        """
        results = self.execute_query(query, {"user_id": user_id, "course_id": course_id})
        return [row["lesson_id"] for row in results]
    
    def get_user_stats(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user statistics"""
        query = "SELECT * FROM user_stats WHERE user_id = :user_id"
        results = self.execute_query(query, {"user_id": user_id})
        return results[0] if results else None
    
    def update_user_stats(self, user_id: str, stats: Dict[str, Any]) -> bool:
        """Update user statistics"""
        query = """
            INSERT INTO user_stats (user_id, total_points, current_level, streak_days, 
                                  time_studied_today, daily_goal_minutes, last_activity_date, total_study_time)
            VALUES (:user_id, :total_points, :current_level, :streak_days, 
                   :time_studied_today, :daily_goal_minutes, :last_activity_date, :total_study_time)
            ON CONFLICT (user_id) DO UPDATE SET
                total_points = EXCLUDED.total_points,
                current_level = EXCLUDED.current_level,
                streak_days = EXCLUDED.streak_days,
                time_studied_today = EXCLUDED.time_studied_today,
                daily_goal_minutes = EXCLUDED.daily_goal_minutes,
                last_activity_date = EXCLUDED.last_activity_date,
                total_study_time = EXCLUDED.total_study_time
        """
        return self.execute_update(query, {**stats, "user_id": user_id})
    
    # Quiz methods
    def save_quiz_result(self, result_data: Dict[str, Any]) -> bool:
        """Save quiz result"""
        query = """
            INSERT INTO quiz_results (user_id, quiz_id, topic, difficulty, score_percentage,
                                    correct_answers, total_questions, user_answers)
            VALUES (:user_id, :quiz_id, :topic, :difficulty, :score_percentage,
                   :correct_answers, :total_questions, :user_answers)
        """
        return self.execute_update(query, result_data)
    
    def get_user_quiz_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's quiz history"""
        query = """
            SELECT * FROM quiz_results 
            WHERE user_id = :user_id 
            ORDER BY completed_at DESC
        """
        return self.execute_query(query, {"user_id": user_id})
    
    # Achievement methods
    def award_achievement(self, user_id: str, achievement_data: Dict[str, Any]) -> bool:
        """Award achievement to user"""
        query = """
            INSERT INTO user_achievements (user_id, achievement_type, title, description, points)
            VALUES (:user_id, :achievement_type, :title, :description, :points)
        """
        return self.execute_update(query, {**achievement_data, "user_id": user_id})
    
    def get_user_achievements(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's achievements"""
        query = """
            SELECT * FROM user_achievements 
            WHERE user_id = :user_id 
            ORDER BY earned_at DESC
        """
        return self.execute_query(query, {"user_id": user_id})
    
    # Interaction tracking
    def record_interaction(self, user_id: str, interaction_type: str, course_id: str, metadata: Dict[str, Any] = None) -> bool:
        """Record user interaction"""
        query = """
            INSERT INTO user_interactions (user_id, interaction_type, course_id, metadata)
            VALUES (:user_id, :interaction_type, :course_id, :metadata)
        """
        return self.execute_update(query, {
            "user_id": user_id,
            "interaction_type": interaction_type,
            "course_id": course_id,
            "metadata": json.dumps(metadata or {})
        })
    
    def get_user_interactions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's interactions"""
        query = """
            SELECT * FROM user_interactions 
            WHERE user_id = :user_id 
            ORDER BY created_at DESC
        """
        return self.execute_query(query, {"user_id": user_id})
    
    def initialize_sample_data(self) -> bool:
        """Initialize database with sample courses if empty"""
        try:
            # Check if courses already exist
            existing_courses = self.get_all_courses()
            if existing_courses:
                return True
            
            # Import sample data from course manager
            from utils.course_manager import CourseManager
            course_manager = CourseManager()
            
            # Get sample courses and save them to database
            for course_data in course_manager.courses.values():
                # Convert arrays to proper format for PostgreSQL
                course_db_data = {
                    "course_id": course_data["course_id"],
                    "title": course_data["title"],
                    "description": course_data["description"],
                    "category": course_data["category"],
                    "difficulty": course_data["difficulty"],
                    "estimated_hours": course_data["estimated_hours"],
                    "rating": course_data["rating"],
                    "instructor": course_data["instructor"],
                    "tags": course_data.get("tags", []),
                    "prerequisites": course_data.get("prerequisites", []),
                    "learning_outcomes": course_data.get("learning_outcomes", []),
                    "lessons": json.dumps(course_data.get("lessons", []))
                }
                self.create_course(course_db_data)
            
            return True
            
        except Exception as e:
            st.error(f"Error initializing sample data: {str(e)}")
            return False