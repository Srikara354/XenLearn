# Complete Download Guide for XenLearn Project

## Quick Start: Get XenLearn into VS Code

### Option 1: Direct File Download (Easiest)

1. **Open VS Code** and create a new folder called `XenLearn`

2. **Download each file** by copying the content from this development environment:

   **Main Application Files:**
   - `app.py` (735 lines) - Main Streamlit application
   - `initialize_database.py` - Database setup with sample courses
   - `README.md` - Complete project documentation
   - `.env.example` - Environment variables template

   **Utils Directory Files:**
   - `utils/__init__.py`
   - `utils/auth_manager.py` - User authentication system
   - `utils/course_manager.py` - Course management with database integration
   - `utils/ai_engine.py` - AI recommendations and personalization
   - `utils/progress_tracker.py` - Progress tracking and achievements
   - `utils/quiz_generator.py` - AI-powered quiz generation
   - `utils/database.py` - PostgreSQL database operations

   **Configuration:**
   - `.streamlit/config.toml` - Streamlit server configuration

3. **Create requirements.txt** with these exact dependencies:
   ```
   streamlit>=1.28.0
   pandas>=2.0.0
   numpy>=1.24.0
   openai>=1.0.0
   psycopg2-binary>=2.9.0
   sqlalchemy>=2.0.0
   plotly>=5.0.0
   ```

### Option 2: GitHub Repository Method

1. **Create empty repository** on your GitHub account named `XenLearn`

2. **Clone to VS Code:**
   ```bash
   git clone https://github.com/Srikara354/XenLearn.git
   cd XenLearn
   ```

3. **Add all project files** to the cloned directory

4. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit: XenLearn AI Learning Platform"
   git push origin main
   ```

## Project Structure to Create

```
XenLearn/
├── app.py                      # Main application (735 lines)
├── initialize_database.py      # Database initialization
├── README.md                   # Documentation
├── requirements.txt            # Dependencies
├── .env.example               # Environment template
├── .streamlit/
│   └── config.toml            # Server configuration
└── utils/
    ├── __init__.py
    ├── auth_manager.py        # Authentication (160 lines)
    ├── course_manager.py      # Course management (275 lines)
    ├── ai_engine.py          # AI engine (285 lines)
    ├── progress_tracker.py   # Progress tracking (320 lines)
    ├── quiz_generator.py     # Quiz generation (350 lines)
    └── database.py           # Database operations (420 lines)
```

## Setup After Download

### 1. Python Environment
```bash
cd XenLearn
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Database Setup
- Install PostgreSQL locally
- Create database named `xenlearn`
- Copy `.env.example` to `.env` and fill in your database credentials

### 3. Environment Configuration
Edit `.env` file:
```
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/xenlearn
OPENAI_API_KEY=your_openai_api_key
```

### 4. Initialize Database
```bash
python initialize_database.py
```

### 5. Run Application
```bash
streamlit run app.py
```

## Features You'll Have

- Complete user authentication system
- 5 sample courses across different subjects
- AI-powered personalized recommendations
- Automatic quiz generation for any topic
- Progress tracking with achievements
- Mobile-responsive design
- PostgreSQL database integration

The application will run at `http://localhost:8501` and provide a full personalized learning experience with AI capabilities.

Would you like me to provide the content of any specific file to help you get started with the download process?