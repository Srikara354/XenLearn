# XenLearn - AI-Powered Personalized Learning Platform

A comprehensive learning management system that adapts to individual learning preferences and provides AI-driven personalized education experiences.

## Features

- **User Authentication**: Secure account creation with personalized learning preferences
- **AI-Powered Recommendations**: Smart course suggestions based on learning style and interests
- **Automatic Quiz Generation**: Dynamic quiz creation using OpenAI for any topic
- **Progress Tracking**: Comprehensive analytics and achievement system
- **Course Management**: Full-featured course catalog with multiple subjects
- **Mobile-Friendly**: Responsive design optimized for all devices
- **Database Integration**: PostgreSQL for reliable data persistence

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: PostgreSQL
- **AI Integration**: OpenAI GPT-4
- **Deployment**: Replit

## Setup Instructions

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up PostgreSQL database
4. Configure environment variables (DATABASE_URL, OPENAI_API_KEY)
5. Run database initialization: `python initialize_database.py`
6. Start the application: `streamlit run app.py`

## Environment Variables Required

- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API key for AI features

## Sample Courses Available

- Python Programming Fundamentals
- Data Science with Python
- Introduction to Machine Learning
- Digital Marketing Strategy
- Calculus I: Limits and Derivatives
