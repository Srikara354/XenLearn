#!/usr/bin/env python3
"""
Database initialization script for the learning platform
Creates tables and loads sample data
"""
import json
import uuid
from datetime import datetime
from utils.database import DatabaseManager

def initialize_sample_courses(db):
    """Initialize database with sample courses"""
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
            'lessons': json.dumps([
                {'lesson_id': str(uuid.uuid4()), 'title': 'Introduction to Python', 'duration_minutes': 30},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Variables and Data Types', 'duration_minutes': 45},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Control Structures', 'duration_minutes': 60},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Functions', 'duration_minutes': 50},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Data Structures', 'duration_minutes': 70}
            ])
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
            'lessons': json.dumps([
                {'lesson_id': str(uuid.uuid4()), 'title': 'Introduction to Data Science', 'duration_minutes': 40},
                {'lesson_id': str(uuid.uuid4()), 'title': 'NumPy Fundamentals', 'duration_minutes': 55},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Pandas for Data Analysis', 'duration_minutes': 75},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Data Visualization', 'duration_minutes': 60},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Statistical Analysis', 'duration_minutes': 80}
            ])
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
            'lessons': json.dumps([
                {'lesson_id': str(uuid.uuid4()), 'title': 'What is Machine Learning?', 'duration_minutes': 35},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Supervised Learning', 'duration_minutes': 65},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Unsupervised Learning', 'duration_minutes': 55},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Model Evaluation', 'duration_minutes': 50},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Neural Networks', 'duration_minutes': 70}
            ])
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
            'lessons': json.dumps([
                {'lesson_id': str(uuid.uuid4()), 'title': 'Digital Marketing Overview', 'duration_minutes': 30},
                {'lesson_id': str(uuid.uuid4()), 'title': 'SEO Fundamentals', 'duration_minutes': 45},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Social Media Marketing', 'duration_minutes': 40},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Content Marketing', 'duration_minutes': 50},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Analytics and Metrics', 'duration_minutes': 35}
            ])
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
            'lessons': json.dumps([
                {'lesson_id': str(uuid.uuid4()), 'title': 'Introduction to Limits', 'duration_minutes': 50},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Limit Laws and Theorems', 'duration_minutes': 60},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Continuity', 'duration_minutes': 45},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Introduction to Derivatives', 'duration_minutes': 55},
                {'lesson_id': str(uuid.uuid4()), 'title': 'Derivative Rules', 'duration_minutes': 70}
            ])
        }
    ]
    
    # Insert sample courses
    for course in sample_courses:
        print(f"Creating course: {course['title']}")
        db.create_course(course)
    
    print(f"Successfully created {len(sample_courses)} sample courses")

def main():
    """Main initialization function"""
    print("Initializing learning platform database...")
    
    try:
        db = DatabaseManager()
        
        # Check if courses already exist
        existing_courses = db.get_all_courses()
        if existing_courses:
            print(f"Database already has {len(existing_courses)} courses")
            return
        
        # Initialize sample courses
        initialize_sample_courses(db)
        
        print("Database initialization completed successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {str(e)}")

if __name__ == "__main__":
    main()