# XenLearn Setup Instructions for VS Code

## Method 1: Download Project Files Directly

Since you can't use git commands directly from this development environment, here are the steps to get the complete project into VS Code:

### Step 1: Download All Project Files

You'll need to manually download these files from the current environment:

**Main Files:**
- `app.py` - Main application
- `initialize_database.py` - Database setup script
- `README.md` - Project documentation
- `pyproject.toml` - Dependencies configuration

**Utils Directory:**
- `utils/__init__.py`
- `utils/auth_manager.py`
- `utils/course_manager.py`
- `utils/ai_engine.py`
- `utils/progress_tracker.py`
- `utils/quiz_generator.py`
- `utils/database.py`

**Configuration:**
- `.streamlit/config.toml`

### Step 2: Create Project Structure in VS Code

1. Open VS Code
2. Create a new folder called `XenLearn`
3. Create the following directory structure:
```
XenLearn/
├── app.py
├── initialize_database.py
├── README.md
├── requirements.txt
├── .streamlit/
│   └── config.toml
└── utils/
    ├── __init__.py
    ├── auth_manager.py
    ├── course_manager.py
    ├── ai_engine.py
    ├── progress_tracker.py
    ├── quiz_generator.py
    └── database.py
```

### Step 3: Create requirements.txt

Create a `requirements.txt` file with these dependencies:
```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
openai>=1.0.0
psycopg2-binary>=2.9.0
sqlalchemy>=2.0.0
plotly>=5.0.0
```

### Step 4: Copy File Contents

Copy the content of each file from this environment to your local VS Code project.

## Method 2: Using Git (Recommended)

### Step 1: Initialize Local Repository
```bash
cd path/to/your/projects
mkdir XenLearn
cd XenLearn
git init
```

### Step 2: Add Remote Repository
```bash
git remote add origin https://github.com/Srikara354/XenLearn.git
```

### Step 3: Create and Push Initial Files
After copying all the files to your local directory:
```bash
git add .
git commit -m "Initial commit: XenLearn personalized learning platform"
git branch -M main
git push -u origin main
```

## Environment Setup

### 1. Python Virtual Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup
- Install PostgreSQL
- Create database: `xenlearn`
- Set environment variables

### 4. Environment Variables
Create `.env` file:
```
DATABASE_URL=postgresql://username:password@localhost:5432/xenlearn
OPENAI_API_KEY=your_openai_api_key
```

### 5. Initialize Database
```bash
python initialize_database.py
```

### 6. Run Application
```bash
streamlit run app.py
```

## VS Code Extensions Recommended

- Python
- Pylance
- GitLens
- PostgreSQL
- Streamlit

## Troubleshooting

1. **Database Connection Issues**: Ensure PostgreSQL is running and credentials are correct
2. **OpenAI API Issues**: Verify your API key is valid and has credits
3. **Import Errors**: Make sure all dependencies are installed in your virtual environment

The application will be ready to run at `http://localhost:8501` once setup is complete.