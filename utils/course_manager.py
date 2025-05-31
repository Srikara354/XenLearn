import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
import streamlit as st

class CourseManager:
    """Handles course creation, management, and enrollment"""
    
    def __init__(self):
        self.courses_file = "data/courses.json"
        self.enrollments_file = "data/enrollments.json"
        self._ensure_data_directory()
        self._load_data()
        self._initialize_sample_courses()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        import os
        if not os.path.exists("data"):
            os.makedirs("data")
    
    def _load_data(self):
        """Load courses and enrollments from JSON files"""
        try:
            with open(self.courses_file, 'r') as f:
                self.courses = json.load(f)
        except FileNotFoundError:
            self.courses = {}
            
        try:
            with open(self.enrollments_file, 'r') as f:
                self.enrollments = json.load(f)
        except FileNotFoundError:
            self.enrollments = {}
    
    def _save_courses(self):
        """Save courses to JSON file"""
        try:
            with open(self.courses_file, 'w') as f:
                json.dump(self.courses, f, indent=2, default=str)
        except Exception as e:
            st.error(f"Error saving courses: {str(e)}")
    
    def _save_enrollments(self):
        """Save enrollments to JSON file"""
        try:
            with open(self.enrollments_file, 'w') as f:
                json.dump(self.enrollments, f, indent=2, default=str)
        except Exception as e:
            st.error(f"Error saving enrollments: {str(e)}")
    
    def _initialize_sample_courses(self):
        """Initialize with sample courses if none exist"""
        if not self.courses:
            sample_courses = [
                {
                    'course_id': str(uuid.uuid4()),
                    'title': 'Python Programming Fundamentals',
                    'description': 'Learn the basics of Python programming including variables, functions, loops, and data structures. Perfect for beginners starting their coding journey.',
                    'category': 'Technology',
                    'difficulty': 'Beginner',
                    'estimated_hours': 20,
                    'rating': 4.5,
                    'instructor': 'Dr. Sarah Johnson',
                    'tags': ['python', 'programming', 'coding', 'fundamentals'],
                    'prerequisites': [],
                    'learning_outcomes': [
                        'Understand Python syntax and basic programming concepts',
                        'Write simple Python programs',
                        'Work with data types and variables',
                        'Create functions and use loops'
                    ],
                    'created_at': datetime.now().isoformat()
                },
                {
                    'course_id': str(uuid.uuid4()),
                    'title': 'Data Science with Python',
                    'description': 'Comprehensive course covering data analysis, visualization, and machine learning using Python libraries like pandas, numpy, and scikit-learn.',
                    'category': 'Technology',
                    'difficulty': 'Intermediate',
                    'estimated_hours': 40,
                    'rating': 4.7,
                    'instructor': 'Prof. Michael Chen',
                    'tags': ['data science', 'python', 'machine learning', 'analytics'],
                    'prerequisites': ['Basic Python knowledge'],
                    'learning_outcomes': [
                        'Analyze and visualize data using pandas and matplotlib',
                        'Build machine learning models',
                        'Understand statistical concepts',
                        'Work with real-world datasets'
                    ],
                    'created_at': datetime.now().isoformat()
                },
                {
                    'course_id': str(uuid.uuid4()),
                    'title': 'Introduction to Machine Learning',
                    'description': 'Explore the fundamentals of machine learning including supervised and unsupervised learning, neural networks, and practical applications.',
                    'category': 'Technology',
                    'difficulty': 'Intermediate',
                    'estimated_hours': 35,
                    'rating': 4.6,
                    'instructor': 'Dr. Emily Rodriguez',
                    'tags': ['machine learning', 'AI', 'algorithms', 'neural networks'],
                    'prerequisites': ['Mathematics basics', 'Programming experience'],
                    'learning_outcomes': [
                        'Understand core ML algorithms',
                        'Implement classification and regression models',
                        'Evaluate model performance',
                        'Apply ML to real problems'
                    ],
                    'created_at': datetime.now().isoformat()
                },
                {
                    'course_id': str(uuid.uuid4()),
                    'title': 'Digital Marketing Strategy',
                    'description': 'Learn how to create effective digital marketing campaigns, understand SEO, social media marketing, and analytics.',
                    'category': 'Business',
                    'difficulty': 'Beginner',
                    'estimated_hours': 25,
                    'rating': 4.3,
                    'instructor': 'Maria Lopez',
                    'tags': ['marketing', 'digital', 'SEO', 'social media'],
                    'prerequisites': [],
                    'learning_outcomes': [
                        'Develop digital marketing strategies',
                        'Understand SEO principles',
                        'Create social media campaigns',
                        'Analyze marketing metrics'
                    ],
                    'created_at': datetime.now().isoformat()
                },
                {
                    'course_id': str(uuid.uuid4()),
                    'title': 'Calculus I: Limits and Derivatives',
                    'description': 'Foundation course in calculus covering limits, continuity, derivatives, and their applications in real-world problems.',
                    'category': 'Mathematics',
                    'difficulty': 'Intermediate',
                    'estimated_hours': 45,
                    'rating': 4.4,
                    'instructor': 'Dr. Robert Kim',
                    'tags': ['calculus', 'mathematics', 'derivatives', 'limits'],
                    'prerequisites': ['Algebra', 'Pre-calculus'],
                    'learning_outcomes': [
                        'Understand limits and continuity',
                        'Calculate derivatives',
                        'Apply derivatives to optimization',
                        'Solve related rates problems'
                    ],
                    'created_at': datetime.now().isoformat()
                }
            ]
            
            for course in sample_courses:
                self.courses[course['course_id']] = course
                
                # Add sample lessons for each course
                self._create_sample_lessons(course['course_id'])
            
            self._save_courses()
    
    def _create_sample_lessons(self, course_id: str):
        """Create sample lessons for a course"""
        course = self.courses[course_id]
        
        if 'Python Programming' in course['title']:
            lessons = [
                {'lesson_id': str(uuid.uuid4()), 'title': 'Introduction to Python', 'duration_minutes': 30, 'content': 'Learn what Python is and why it\'s popular.'},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Variables and Data Types', 'duration_minutes': 45, 'content': 'Understanding different data types in Python.'},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Control Structures', 'duration_minutes': 60, 'content': 'If statements, loops, and control flow.'},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Functions', 'duration_minutes': 50, 'content': 'Creating and using functions in Python.'},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Data Structures', 'duration_minutes': 70, 'content': 'Lists, dictionaries, and sets.'}
            ]
        elif 'Data Science' in course['title']:
            lessons = [
                {'lesson_id': str(uuid.uuid4()), 'title': 'Introduction to Data Science', 'duration_minutes': 40, 'content': 'Overview of data science field.'},
                {'lesson_id': str(uuid.uuid4()), 'title': 'NumPy Fundamentals', 'duration_minutes': 55, 'content': 'Working with numerical arrays.'},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Pandas for Data Analysis', 'duration_minutes': 75, 'content': 'Data manipulation and analysis.'},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Data Visualization', 'duration_minutes': 60, 'content': 'Creating charts and graphs.'},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Statistical Analysis', 'duration_minutes': 80, 'content': 'Statistical methods and hypothesis testing.'}
            ]
        elif 'Machine Learning' in course['title']:
            lessons = [
                {'lesson_id': str(uuid.uuid4()), 'title': 'What is Machine Learning?', 'duration_minutes': 35, 'content': 'Introduction to ML concepts.'},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Supervised Learning', 'duration_minutes': 65, 'content': 'Classification and regression algorithms.'},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Unsupervised Learning', 'duration_minutes': 55, 'content': 'Clustering and dimensionality reduction.'},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Model Evaluation', 'duration_minutes': 50, 'content': 'Metrics and validation techniques.'},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Neural Networks', 'duration_minutes': 70, 'content': 'Introduction to deep learning.'}
            ]
        elif 'Marketing' in course['title']:
            lessons = [
                {'lesson_id': str(uuid.uuid4()), 'title': 'Digital Marketing Overview', 'duration_minutes': 30, 'content': 'Understanding digital marketing landscape.'},
                {'lesson_id': str(uuid.uuid4()), 'title': 'SEO Fundamentals', 'duration_minutes': 45, 'content': 'Search engine optimization basics.'},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Social Media Marketing', 'duration_minutes': 40, 'content': 'Leveraging social platforms.'},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Content Marketing', 'duration_minutes': 50, 'content': 'Creating engaging content.'},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Analytics and Metrics', 'duration_minutes': 35, 'content': 'Measuring marketing success.'}
            ]
        else:  # Calculus
            lessons = [
                {'lesson_id': str(uuid.uuid4()), 'title': 'Introduction to Limits', 'duration_minutes': 50, 'content': 'Understanding the concept of limits.'},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Limit Laws and Theorems', 'duration_minutes': 60, 'content': 'Mathematical rules for limits.'},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Continuity', 'duration_minutes': 45, 'content': 'When functions are continuous.'},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Introduction to Derivatives', 'duration_minutes': 55, 'content': 'The derivative concept.'},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Derivative Rules', 'duration_minutes': 70, 'content': 'Power rule, product rule, chain rule.'}
            ]
        
        course['lessons'] = lessons
    
    def get_course(self, course_id: str) -> Optional[Dict[str, Any]]:
        """Get course by ID"""
        return self.courses.get(course_id)
    
    def get_all_courses(self) -> List[Dict[str, Any]]:
        """Get all courses"""
        return list(self.courses.values())
    
    def get_categories(self) -> List[str]:
        """Get all course categories"""
        categories = set()
        for course in self.courses.values():
            categories.add(course['category'])
        return sorted(list(categories))
    
    def search_courses(self, query: str = "", category: str = "All", difficulty: str = "All") -> List[Dict[str, Any]]:
        """Search courses with filters"""
        filtered_courses = []
        
        for course in self.courses.values():
            # Filter by category
            if category != "All" and course['category'] != category:
                continue
            
            # Filter by difficulty
            if difficulty != "All" and course['difficulty'] != difficulty:
                continue
            
            # Filter by search query
            if query:
                query_lower = query.lower()
                if not (query_lower in course['title'].lower() or 
                       query_lower in course['description'].lower() or
                       any(query_lower in tag.lower() for tag in course.get('tags', []))):
                    continue
            
            filtered_courses.append(course)
        
        # Sort by rating (highest first)
        filtered_courses.sort(key=lambda x: x.get('rating', 0), reverse=True)
        return filtered_courses
    
    def get_course_lessons(self, course_id: str) -> List[Dict[str, Any]]:
        """Get lessons for a specific course"""
        course = self.courses.get(course_id)
        if course:
            return course.get('lessons', [])
        return []
    
    def enroll_user(self, user_id: str, course_id: str) -> bool:
        """Enroll a user in a course"""
        try:
            if user_id not in self.enrollments:
                self.enrollments[user_id] = []
            
            # Check if already enrolled
            if course_id in self.enrollments[user_id]:
                return False
            
            # Add enrollment
            self.enrollments[user_id].append(course_id)
            self._save_enrollments()
            return True
            
        except Exception as e:
            st.error(f"Error enrolling user: {str(e)}")
            return False
    
    def get_user_enrollments(self, user_id: str) -> List[str]:
        """Get all courses a user is enrolled in"""
        return self.enrollments.get(user_id, [])
    
    def is_user_enrolled(self, user_id: str, course_id: str) -> bool:
        """Check if user is enrolled in a course"""
        user_enrollments = self.enrollments.get(user_id, [])
        return course_id in user_enrollments
    
    def get_course_stats(self, course_id: str) -> Dict[str, Any]:
        """Get statistics for a course"""
        enrollment_count = sum(1 for enrollments in self.enrollments.values() if course_id in enrollments)
        
        course = self.courses.get(course_id)
        if not course:
            return {}
        
        return {
            'enrollment_count': enrollment_count,
            'rating': course.get('rating', 0),
            'total_lessons': len(course.get('lessons', [])),
            'estimated_hours': course.get('estimated_hours', 0),
            'category': course.get('category', 'Unknown')
        }
    
    def get_recommended_courses(self, user_interests: List[str], user_difficulty: str, exclude_enrolled: List[str] = None) -> List[Dict[str, Any]]:
        """Get courses recommended based on user preferences"""
        if exclude_enrolled is None:
            exclude_enrolled = []
        
        recommendations = []
        
        for course in self.courses.values():
            if course['course_id'] in exclude_enrolled:
                continue
            
            score = 0
            
            # Score based on interests
            course_tags = course.get('tags', [])
            for interest in user_interests:
                if any(interest.lower() in tag.lower() for tag in course_tags):
                    score += 2
                if interest.lower() in course['category'].lower():
                    score += 3
            
            # Score based on difficulty preference
            if course['difficulty'] == user_difficulty:
                score += 1
            elif user_difficulty == "Mixed":
                score += 0.5
            
            # Add rating bonus
            score += course.get('rating', 0) * 0.5
            
            if score > 0:
                course_copy = course.copy()
                course_copy['recommendation_score'] = score
                recommendations.append(course_copy)
        
        # Sort by recommendation score
        recommendations.sort(key=lambda x: x['recommendation_score'], reverse=True)
        return recommendations[:10]  # Return top 10