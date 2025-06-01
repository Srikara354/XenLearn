# XenLearn - AI-Powered Personalized Learning Platform

A comprehensive learning management system that adapts to individual learning preferences and provides AI-driven personalized education experiences.

## Features

- **User Authentication**: Secure account creation with personalized learning preferences
- **AI-Powered Recommendations**: Smart course suggestions based on learning style and interests
- **Automatic Quiz Generation**: Dynamic quiz creation using OpenAI for any topic
- **Progress Tracking**: Comprehensive analytics and achievement system
- **Course Management**: Full-featured course catalog with multiple subjects
- **Mobile-Friendly**: Responsive design optimized for all devices
- **Database Integration**: PostgreSQL for reliable data persistence (optional, now supports file-based mode)

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: PostgreSQL (optional)
- **AI Integration**: OpenAI GPT-4
- **Deployment**: Replit

## Project Structure

```
XenLearn/
├── app.py                      # Main Streamlit application
├── initialize_database.py      # Database setup script
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .streamlit/
│   └── config.toml            # Streamlit configuration
└── utils/
    ├── __init__.py
    ├── auth_manager.py        # User authentication
    ├── course_manager.py      # Course management
    ├── ai_engine.py           # AI recommendations
    ├── progress_tracker.py    # Progress tracking
    ├── quiz_generator.py      # Quiz generation
    ├── database.py            # Database operations
    └── file_user_manager.py   # File-based user management (no DB required)
```

## Setup Instructions

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. (Optional) Set up PostgreSQL database and configure environment variables (`DATABASE_URL`, `OPENAI_API_KEY`)
4. (Optional) Run database initialization: `python initialize_database.py`
5. Start the application: `streamlit run app.py`

- By default, the app now works in file-based mode for user authentication and preferences (no database required).
- For production or multi-user environments, configure PostgreSQL as described in `.env.example`.

## Environment Variables Required

- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API key for AI features

## Sample Courses Available

- Python Programming Fundamentals
- Data Science with Python
- Introduction to Machine Learning
- Digital Marketing Strategy
- Calculus I: Limits and Derivatives

## Features Overview

### User Authentication
- Secure signup/login system
- Learning preference profiling
- Password hashing and validation

### Course Management
- Browse courses by category and difficulty
- Search functionality
- Course enrollment and progress tracking
- Lesson completion tracking

### AI-Powered Features
- Personalized course recommendations
- Adaptive quiz generation
- Learning path optimization
- Performance analysis

### Progress Tracking
- Achievement system
- Learning streaks
- Study time analytics
- Progress visualization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support or questions, please open an issue on GitHub.
