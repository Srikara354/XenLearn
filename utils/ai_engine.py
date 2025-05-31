import json
import random
from typing import List, Dict, Any, Optional
import streamlit as st
from datetime import datetime, timedelta

class AIEngine:
    """Handles AI-powered personalization and recommendations"""
    
    def __init__(self):
        self.recommendations_file = "data/ai_recommendations.json"
        self.user_interactions_file = "data/user_interactions.json"
        self._ensure_data_directory()
        self._load_data()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        import os
        if not os.path.exists("data"):
            os.makedirs("data")
    
    def _load_data(self):
        """Load AI data from JSON files"""
        try:
            with open(self.recommendations_file, 'r') as f:
                self.recommendations_cache = json.load(f)
        except FileNotFoundError:
            self.recommendations_cache = {}
        
        try:
            with open(self.user_interactions_file, 'r') as f:
                self.user_interactions = json.load(f)
        except FileNotFoundError:
            self.user_interactions = {}
    
    def _save_recommendations(self):
        """Save recommendations cache to JSON file"""
        try:
            with open(self.recommendations_file, 'w') as f:
                json.dump(self.recommendations_cache, f, indent=2, default=str)
        except Exception as e:
            st.error(f"Error saving recommendations: {str(e)}")
    
    def _save_interactions(self):
        """Save user interactions to JSON file"""
        try:
            with open(self.user_interactions_file, 'w') as f:
                json.dump(self.user_interactions, f, indent=2, default=str)
        except Exception as e:
            st.error(f"Error saving interactions: {str(e)}")
    
    def get_personalized_recommendations(self, user_id: str, preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate personalized course recommendations"""
        try:
            from utils.course_manager import CourseManager
            course_manager = CourseManager()
            
            # Get user's enrolled courses to exclude from recommendations
            enrolled_courses = course_manager.get_user_enrollments(user_id)
            
            # Get user interactions for better personalization
            user_interactions = self.user_interactions.get(user_id, {})
            
            # Get all courses
            all_courses = course_manager.get_all_courses()
            
            recommendations = []
            
            for course in all_courses:
                if course['course_id'] in enrolled_courses:
                    continue
                
                # Calculate recommendation score
                score = self._calculate_recommendation_score(course, preferences, user_interactions)
                
                if score > 0:
                    recommendation = {
                        'course_id': course['course_id'],
                        'confidence': min(score / 10.0, 1.0),  # Normalize to 0-1
                        'reason': self._generate_recommendation_reason(course, preferences, score)
                    }
                    recommendations.append(recommendation)
            
            # Sort by confidence score
            recommendations.sort(key=lambda x: x['confidence'], reverse=True)
            
            # Cache recommendations
            self.recommendations_cache[user_id] = {
                'recommendations': recommendations[:10],
                'generated_at': datetime.now().isoformat(),
                'preferences_hash': hash(str(preferences))
            }
            self._save_recommendations()
            
            return recommendations[:10]
            
        except Exception as e:
            st.error(f"Error generating recommendations: {str(e)}")
            return []
    
    def _calculate_recommendation_score(self, course: Dict[str, Any], preferences: Dict[str, Any], interactions: Dict[str, Any]) -> float:
        """Calculate recommendation score for a course"""
        score = 0.0
        
        # Base score from course rating
        score += course.get('rating', 0) * 2
        
        # Score based on user interests
        user_interests = preferences.get('interests', [])
        course_tags = course.get('tags', [])
        
        for interest in user_interests:
            # Check if interest matches course category
            if interest.lower() in course['category'].lower():
                score += 3
            
            # Check if interest matches course tags
            for tag in course_tags:
                if interest.lower() in tag.lower():
                    score += 2
            
            # Check if interest is in course title or description
            if (interest.lower() in course['title'].lower() or 
                interest.lower() in course['description'].lower()):
                score += 1
        
        # Score based on difficulty preference
        user_difficulty = preferences.get('difficulty_preference', 'Beginner')
        if course['difficulty'] == user_difficulty:
            score += 2
        elif user_difficulty == 'Mixed':
            score += 1
        
        # Score based on learning style (simplified mapping)
        learning_style = preferences.get('learning_style', 'Visual')
        if learning_style == 'Visual' and 'visualization' in course.get('tags', []):
            score += 1
        elif learning_style == 'Kinesthetic' and 'hands-on' in course.get('tags', []):
            score += 1
        
        # Adjust score based on estimated time vs user preference
        user_time_pref = preferences.get('study_time', '30-60 minutes')
        course_hours = course.get('estimated_hours', 0)
        
        if user_time_pref == '15-30 minutes' and course_hours <= 15:
            score += 1
        elif user_time_pref == '30-60 minutes' and 15 < course_hours <= 30:
            score += 1
        elif user_time_pref == '1-2 hours' and 30 < course_hours <= 50:
            score += 1
        elif user_time_pref == '2+ hours' and course_hours > 50:
            score += 1
        
        # Boost popular courses slightly
        # This would typically use actual enrollment data
        if course.get('rating', 0) >= 4.5:
            score += 0.5
        
        # Consider user's past interactions
        category_interactions = interactions.get('categories', {})
        if course['category'] in category_interactions:
            score += category_interactions[course['category']] * 0.1
        
        return score
    
    def _generate_recommendation_reason(self, course: Dict[str, Any], preferences: Dict[str, Any], score: float) -> str:
        """Generate a human-readable reason for the recommendation"""
        reasons = []
        
        user_interests = preferences.get('interests', [])
        
        # Check interest matches
        for interest in user_interests:
            if interest.lower() in course['category'].lower():
                reasons.append(f"Matches your interest in {interest}")
                break
        
        # Check difficulty match
        if course['difficulty'] == preferences.get('difficulty_preference', 'Beginner'):
            reasons.append(f"Perfect for your {course['difficulty'].lower()} level")
        
        # Check rating
        if course.get('rating', 0) >= 4.5:
            reasons.append(f"Highly rated ({course['rating']}/5 stars)")
        
        # Default reason
        if not reasons:
            reasons.append("Based on your learning preferences")
        
        return reasons[0]  # Return the primary reason
    
    def record_user_interaction(self, user_id: str, interaction_type: str, course_id: str, metadata: Dict[str, Any] = None):
        """Record user interaction for learning personalization"""
        try:
            if user_id not in self.user_interactions:
                self.user_interactions[user_id] = {
                    'course_views': [],
                    'enrollments': [],
                    'completions': [],
                    'categories': {},
                    'last_updated': datetime.now().isoformat()
                }
            
            interaction_data = {
                'course_id': course_id,
                'timestamp': datetime.now().isoformat(),
                'metadata': metadata or {}
            }
            
            # Record the interaction
            if interaction_type == 'view':
                self.user_interactions[user_id]['course_views'].append(interaction_data)
            elif interaction_type == 'enroll':
                self.user_interactions[user_id]['enrollments'].append(interaction_data)
            elif interaction_type == 'complete':
                self.user_interactions[user_id]['completions'].append(interaction_data)
            
            # Update category preferences
            if metadata and 'category' in metadata:
                category = metadata['category']
                categories = self.user_interactions[user_id]['categories']
                categories[category] = categories.get(category, 0) + 1
            
            self.user_interactions[user_id]['last_updated'] = datetime.now().isoformat()
            self._save_interactions()
            
        except Exception as e:
            st.error(f"Error recording interaction: {str(e)}")
    
    def get_learning_path(self, user_id: str, target_skill: str) -> List[Dict[str, Any]]:
        """Generate a suggested learning path for a specific skill"""
        try:
            from utils.course_manager import CourseManager
            course_manager = CourseManager()
            
            # Get courses related to the target skill
            related_courses = course_manager.search_courses(query=target_skill)
            
            if not related_courses:
                return []
            
            # Sort courses by difficulty and prerequisites
            beginner_courses = [c for c in related_courses if c['difficulty'] == 'Beginner']
            intermediate_courses = [c for c in related_courses if c['difficulty'] == 'Intermediate']
            advanced_courses = [c for c in related_courses if c['difficulty'] == 'Advanced']
            
            # Build learning path
            learning_path = []
            
            # Add beginner courses first
            for course in sorted(beginner_courses, key=lambda x: x.get('rating', 0), reverse=True)[:2]:
                learning_path.append({
                    'course_id': course['course_id'],
                    'title': course['title'],
                    'step': len(learning_path) + 1,
                    'estimated_hours': course['estimated_hours'],
                    'reason': 'Foundation course'
                })
            
            # Add intermediate courses
            for course in sorted(intermediate_courses, key=lambda x: x.get('rating', 0), reverse=True)[:2]:
                learning_path.append({
                    'course_id': course['course_id'],
                    'title': course['title'],
                    'step': len(learning_path) + 1,
                    'estimated_hours': course['estimated_hours'],
                    'reason': 'Build intermediate skills'
                })
            
            # Add advanced courses
            for course in sorted(advanced_courses, key=lambda x: x.get('rating', 0), reverse=True)[:1]:
                learning_path.append({
                    'course_id': course['course_id'],
                    'title': course['title'],
                    'step': len(learning_path) + 1,
                    'estimated_hours': course['estimated_hours'],
                    'reason': 'Master advanced concepts'
                })
            
            return learning_path
            
        except Exception as e:
            st.error(f"Error generating learning path: {str(e)}")
            return []
    
    def get_adaptive_content_suggestions(self, user_id: str, current_course_id: str) -> Dict[str, Any]:
        """Suggest adaptive content based on user performance"""
        try:
            user_interactions = self.user_interactions.get(user_id, {})
            
            # Analyze user's learning patterns
            suggestions = {
                'review_topics': [],
                'supplementary_materials': [],
                'difficulty_adjustment': 'maintain',
                'study_schedule': {}
            }
            
            # Simple heuristics for content adaptation
            completions = user_interactions.get('completions', [])
            recent_completions = [c for c in completions 
                                if (datetime.now() - datetime.fromisoformat(c['timestamp'])).days <= 7]
            
            if len(recent_completions) < 2:
                suggestions['difficulty_adjustment'] = 'reduce'
                suggestions['study_schedule']['recommended_pace'] = 'slower'
            elif len(recent_completions) > 5:
                suggestions['difficulty_adjustment'] = 'increase'
                suggestions['study_schedule']['recommended_pace'] = 'faster'
            
            # Add some sample suggestions
            suggestions['supplementary_materials'] = [
                'Practice exercises for better understanding',
                'Video tutorials for visual learning',
                'Interactive coding examples'
            ]
            
            return suggestions
            
        except Exception as e:
            st.error(f"Error generating adaptive suggestions: {str(e)}")
            return {}
    
    def analyze_learning_effectiveness(self, user_id: str) -> Dict[str, Any]:
        """Analyze user's learning effectiveness and provide insights"""
        try:
            user_interactions = self.user_interactions.get(user_id, {})
            
            analysis = {
                'learning_velocity': 'average',
                'retention_score': 0.8,
                'preferred_content_types': [],
                'optimal_study_times': [],
                'improvement_areas': []
            }
            
            # Analyze completion patterns
            completions = user_interactions.get('completions', [])
            if completions:
                # Calculate average time between enrollments and completions
                enrollments = user_interactions.get('enrollments', [])
                
                if enrollments and len(completions) >= len(enrollments) * 0.7:
                    analysis['learning_velocity'] = 'fast'
                elif len(completions) < len(enrollments) * 0.3:
                    analysis['learning_velocity'] = 'slow'
            
            # Analyze category preferences
            categories = user_interactions.get('categories', {})
            if categories:
                analysis['preferred_content_types'] = sorted(categories.items(), 
                                                           key=lambda x: x[1], reverse=True)[:3]
            
            return analysis
            
        except Exception as e:
            st.error(f"Error analyzing learning effectiveness: {str(e)}")
            return {}