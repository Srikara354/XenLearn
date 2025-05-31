import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import streamlit as st

class ProgressTracker:
    """Handles user progress tracking and analytics"""
    
    def __init__(self):
        self.progress_file = "data/user_progress.json"
        self.achievements_file = "data/achievements.json"
        self._ensure_data_directory()
        self._load_data()
        self._initialize_achievements()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        import os
        if not os.path.exists("data"):
            os.makedirs("data")
    
    def _load_data(self):
        """Load progress data from JSON files"""
        try:
            with open(self.progress_file, 'r') as f:
                self.user_progress = json.load(f)
        except FileNotFoundError:
            self.user_progress = {}
        
        try:
            with open(self.achievements_file, 'r') as f:
                self.achievements_data = json.load(f)
        except FileNotFoundError:
            self.achievements_data = {}
    
    def _save_progress(self):
        """Save progress data to JSON file"""
        try:
            with open(self.progress_file, 'w') as f:
                json.dump(self.user_progress, f, indent=2, default=str)
        except Exception as e:
            st.error(f"Error saving progress: {str(e)}")
    
    def _save_achievements(self):
        """Save achievements data to JSON file"""
        try:
            with open(self.achievements_file, 'w') as f:
                json.dump(self.achievements_data, f, indent=2, default=str)
        except Exception as e:
            st.error(f"Error saving achievements: {str(e)}")
    
    def _initialize_achievements(self):
        """Initialize achievement definitions if they don't exist"""
        if not self.achievements_data:
            self.achievements_data = {
                'definitions': {
                    'first_course': {
                        'title': 'Getting Started',
                        'description': 'Enrolled in your first course',
                        'icon': '🎯',
                        'points': 50
                    },
                    'first_completion': {
                        'title': 'Course Completer',
                        'description': 'Completed your first course',
                        'icon': '🏆',
                        'points': 100
                    },
                    'week_streak': {
                        'title': 'Week Warrior',
                        'description': 'Studied for 7 consecutive days',
                        'icon': '🔥',
                        'points': 150
                    },
                    'quiz_master': {
                        'title': 'Quiz Master',
                        'description': 'Scored 90% or higher on 5 quizzes',
                        'icon': '🧠',
                        'points': 200
                    },
                    'speed_learner': {
                        'title': 'Speed Learner',
                        'description': 'Completed 3 courses in a month',
                        'icon': '⚡',
                        'points': 300
                    }
                },
                'user_achievements': {}
            }
            self._save_achievements()
    
    def get_user_progress(self, user_id: str) -> Dict[str, Any]:
        """Get user's overall progress"""
        if user_id not in self.user_progress:
            self.user_progress[user_id] = {
                'enrolled_courses': [],
                'completed_courses': [],
                'completed_lessons': 0,
                'total_points': 0,
                'level': 1,
                'streak_days': 0,
                'time_studied_today': 0,
                'daily_goal_minutes': 30,
                'course_progress': {},
                'completed_lessons_by_course': {},
                'time_spent_by_course': {},
                'last_activity': None,
                'created_at': datetime.now().isoformat()
            }
            self._save_progress()
        
        return self.user_progress[user_id]
    
    def complete_lesson(self, user_id: str, course_id: str, lesson_id: str, time_spent: int = 0):
        """Mark a lesson as completed"""
        try:
            progress = self.get_user_progress(user_id)
            
            # Add to completed lessons
            if course_id not in progress['completed_lessons_by_course']:
                progress['completed_lessons_by_course'][course_id] = []
            
            if lesson_id not in progress['completed_lessons_by_course'][course_id]:
                progress['completed_lessons_by_course'][course_id].append(lesson_id)
                progress['completed_lessons'] += 1
                
                # Award points
                lesson_points = 20
                progress['total_points'] += lesson_points
                
                # Update time spent
                if time_spent > 0:
                    if course_id not in progress['time_spent_by_course']:
                        progress['time_spent_by_course'][course_id] = 0
                    progress['time_spent_by_course'][course_id] += time_spent
                    progress['time_studied_today'] += time_spent
                
                # Update course progress
                self._update_course_progress(user_id, course_id)
                
                # Check for achievements
                self._check_achievements(user_id)
                
                # Update activity
                progress['last_activity'] = datetime.now().isoformat()
                
                # Update level based on points
                new_level = (progress['total_points'] // 1000) + 1
                if new_level > progress['level']:
                    progress['level'] = new_level
                
                self._save_progress()
                return True
            
            return False
            
        except Exception as e:
            st.error(f"Error completing lesson: {str(e)}")
            return False
    
    def _update_course_progress(self, user_id: str, course_id: str):
        """Update progress percentage for a course"""
        try:
            from utils.course_manager import CourseManager
            course_manager = CourseManager()
            
            lessons = course_manager.get_course_lessons(course_id)
            if not lessons:
                return
            
            progress = self.get_user_progress(user_id)
            completed_lessons = progress['completed_lessons_by_course'].get(course_id, [])
            
            progress_percentage = (len(completed_lessons) / len(lessons)) * 100
            progress['course_progress'][course_id] = min(progress_percentage, 100)
            
            # Check if course is completed
            if progress_percentage >= 100 and course_id not in progress['completed_courses']:
                progress['completed_courses'].append(course_id)
                progress['total_points'] += 500  # Bonus points for course completion
                
                # Award achievement
                self._award_achievement(user_id, 'first_completion')
            
        except Exception as e:
            st.error(f"Error updating course progress: {str(e)}")
    
    def enroll_in_course(self, user_id: str, course_id: str):
        """Record course enrollment"""
        try:
            progress = self.get_user_progress(user_id)
            
            if course_id not in progress['enrolled_courses']:
                progress['enrolled_courses'].append(course_id)
                progress['course_progress'][course_id] = 0
                progress['completed_lessons_by_course'][course_id] = []
                progress['time_spent_by_course'][course_id] = 0
                
                # Award first course achievement
                if len(progress['enrolled_courses']) == 1:
                    self._award_achievement(user_id, 'first_course')
                
                self._save_progress()
                return True
            
            return False
            
        except Exception as e:
            st.error(f"Error enrolling in course: {str(e)}")
            return False
    
    def update_daily_activity(self, user_id: str, minutes_studied: int):
        """Update daily study activity and streak"""
        try:
            progress = self.get_user_progress(user_id)
            today = datetime.now().date()
            
            # Reset daily time if it's a new day
            last_activity = progress.get('last_activity')
            if last_activity:
                last_date = datetime.fromisoformat(last_activity).date()
                if today != last_date:
                    progress['time_studied_today'] = 0
            
            progress['time_studied_today'] += minutes_studied
            progress['last_activity'] = datetime.now().isoformat()
            
            # Update streak
            self._update_learning_streak(user_id)
            
            self._save_progress()
            
        except Exception as e:
            st.error(f"Error updating daily activity: {str(e)}")
    
    def _update_learning_streak(self, user_id: str):
        """Update user's learning streak"""
        try:
            progress = self.get_user_progress(user_id)
            today = datetime.now().date()
            
            last_activity = progress.get('last_activity')
            if not last_activity:
                progress['streak_days'] = 1
                return
            
            last_date = datetime.fromisoformat(last_activity).date()
            days_diff = (today - last_date).days
            
            if days_diff == 0:
                # Same day, maintain streak
                pass
            elif days_diff == 1:
                # Consecutive day, increment streak
                progress['streak_days'] += 1
                
                # Check for streak achievements
                if progress['streak_days'] >= 7:
                    self._award_achievement(user_id, 'week_streak')
            else:
                # Streak broken, reset
                progress['streak_days'] = 1
            
        except Exception as e:
            st.error(f"Error updating learning streak: {str(e)}")
    
    def _check_achievements(self, user_id: str):
        """Check and award achievements based on user progress"""
        try:
            progress = self.get_user_progress(user_id)
            
            # Check various achievement conditions
            if len(progress['completed_courses']) >= 3:
                # Check if completed 3 courses in a month
                completed_dates = []
                for course_id in progress['completed_courses']:
                    # This is simplified - in a real app, you'd track completion dates
                    completed_dates.append(datetime.now())
                
                if len(completed_dates) >= 3:
                    month_ago = datetime.now() - timedelta(days=30)
                    recent_completions = [d for d in completed_dates if d >= month_ago]
                    if len(recent_completions) >= 3:
                        self._award_achievement(user_id, 'speed_learner')
            
        except Exception as e:
            st.error(f"Error checking achievements: {str(e)}")
    
    def _award_achievement(self, user_id: str, achievement_id: str):
        """Award an achievement to a user"""
        try:
            if user_id not in self.achievements_data['user_achievements']:
                self.achievements_data['user_achievements'][user_id] = []
            
            user_achievements = self.achievements_data['user_achievements'][user_id]
            
            # Check if user already has this achievement
            if any(ach['achievement_id'] == achievement_id for ach in user_achievements):
                return False
            
            achievement_def = self.achievements_data['definitions'].get(achievement_id)
            if not achievement_def:
                return False
            
            # Award the achievement
            achievement_record = {
                'achievement_id': achievement_id,
                'title': achievement_def['title'],
                'description': achievement_def['description'],
                'icon': achievement_def['icon'],
                'points': achievement_def['points'],
                'date': datetime.now().isoformat()
            }
            
            user_achievements.append(achievement_record)
            
            # Add points to user's total
            progress = self.get_user_progress(user_id)
            progress['total_points'] += achievement_def['points']
            
            self._save_achievements()
            self._save_progress()
            
            return True
            
        except Exception as e:
            st.error(f"Error awarding achievement: {str(e)}")
            return False
    
    def get_detailed_progress(self, user_id: str) -> Dict[str, Any]:
        """Get detailed progress analytics for a user"""
        try:
            progress = self.get_user_progress(user_id)
            
            # Calculate additional metrics
            total_courses = len(progress['enrolled_courses'])
            completed_courses = len(progress['completed_courses'])
            completion_rate = (completed_courses / total_courses * 100) if total_courses > 0 else 0
            
            # Generate daily study time data (mock data for demo)
            daily_study_time = {}
            for i in range(7):
                date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
                daily_study_time[date] = max(0, progress['time_studied_today'] - (i * 5))
            
            # Get user achievements
            user_achievements = self.achievements_data['user_achievements'].get(user_id, [])
            
            detailed_progress = {
                'basic_stats': progress,
                'completion_rate': completion_rate,
                'daily_study_time': daily_study_time,
                'achievements': user_achievements,
                'total_study_hours': sum(progress['time_spent_by_course'].values()) / 60,
                'average_session_length': self._calculate_average_session_length(user_id),
                'learning_efficiency': self._calculate_learning_efficiency(user_id)
            }
            
            return detailed_progress
            
        except Exception as e:
            st.error(f"Error getting detailed progress: {str(e)}")
            return {}
    
    def _calculate_average_session_length(self, user_id: str) -> float:
        """Calculate average study session length"""
        # This would typically analyze actual session data
        # For demo purposes, return a reasonable estimate
        progress = self.get_user_progress(user_id)
        total_time = sum(progress['time_spent_by_course'].values())
        total_lessons = progress['completed_lessons']
        
        if total_lessons > 0:
            return total_time / total_lessons
        return 0.0
    
    def _calculate_learning_efficiency(self, user_id: str) -> float:
        """Calculate learning efficiency score"""
        # This would analyze completion times vs average times
        # For demo purposes, return a score based on streak and completion rate
        progress = self.get_user_progress(user_id)
        
        streak_factor = min(progress['streak_days'] / 30, 1.0)  # Max factor of 1.0 for 30+ day streak
        
        total_courses = len(progress['enrolled_courses'])
        completed_courses = len(progress['completed_courses'])
        completion_factor = (completed_courses / total_courses) if total_courses > 0 else 0
        
        efficiency = (streak_factor * 0.4 + completion_factor * 0.6) * 100
        return min(efficiency, 100)
    
    def record_quiz_result(self, user_id: str, quiz_topic: str, score_percentage: float):
        """Record quiz results for achievement tracking"""
        try:
            progress = self.get_user_progress(user_id)
            
            if 'quiz_results' not in progress:
                progress['quiz_results'] = []
            
            quiz_result = {
                'topic': quiz_topic,
                'score': score_percentage,
                'date': datetime.now().isoformat()
            }
            
            progress['quiz_results'].append(quiz_result)
            
            # Check for quiz master achievement
            high_scores = [r for r in progress['quiz_results'] if r['score'] >= 90]
            if len(high_scores) >= 5:
                self._award_achievement(user_id, 'quiz_master')
            
            self._save_progress()
            
        except Exception as e:
            st.error(f"Error recording quiz result: {str(e)}")
    
    def get_learning_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive learning analytics"""
        try:
            progress = self.get_user_progress(user_id)
            
            analytics = {
                'study_patterns': {
                    'total_time': sum(progress['time_spent_by_course'].values()),
                    'average_daily_time': progress.get('time_studied_today', 0),
                    'consistency_score': min(progress['streak_days'] / 30 * 100, 100)
                },
                'performance_metrics': {
                    'completion_rate': len(progress['completed_courses']) / max(len(progress['enrolled_courses']), 1) * 100,
                    'average_quiz_score': self._calculate_average_quiz_score(user_id),
                    'learning_velocity': len(progress['completed_lessons']) / max((datetime.now() - datetime.fromisoformat(progress['created_at'])).days, 1)
                },
                'engagement_metrics': {
                    'courses_enrolled': len(progress['enrolled_courses']),
                    'lessons_completed': progress['completed_lessons'],
                    'achievements_earned': len(self.achievements_data['user_achievements'].get(user_id, [])),
                    'current_level': progress['level']
                }
            }
            
            return analytics
            
        except Exception as e:
            st.error(f"Error getting learning analytics: {str(e)}")
            return {}
    
    def _calculate_average_quiz_score(self, user_id: str) -> float:
        """Calculate average quiz score"""
        progress = self.get_user_progress(user_id)
        quiz_results = progress.get('quiz_results', [])
        
        if not quiz_results:
            return 0.0
        
        total_score = sum(result['score'] for result in quiz_results)
        return total_score / len(quiz_results)