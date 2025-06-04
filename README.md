## XenLearn 🌟
Welcome to XenLearn, a cutting-edge learning management system designed to deliver personalized education experiences through AI-driven insights and adaptive learning technologies. 🚀
### Overview 📚
XenLearn is a comprehensive platform that tailors learning paths to individual preferences, leveraging AI to provide dynamic course recommendations, automated quiz generation, and detailed progress tracking. With a mobile-friendly interface and flexible database options, XenLearn empowers learners to achieve their goals efficiently and effectively. 🌐
### Features ✨

🔒 User Authentication: Secure account creation with customizable learning preferences.
🧠 AI-Powered Recommendations: Intelligent course suggestions tailored to learning styles and interests.
📝 Automatic Quiz Generation: Dynamic quizzes created using OpenAI for any topic.
📊 Progress Tracking: In-depth analytics and achievement system to monitor learning progress.
📚 Course Management: Robust course catalog supporting multiple subjects.
📱 Mobile-Friendly: Responsive design optimized for seamless use across all devices.
💾 Database Integration: Optional PostgreSQL for reliable data persistence, with file-based mode for flexibility.

### Technology Stack 🛠️

Frontend: Streamlit for an intuitive and interactive user interface.
Backend: Python for robust and scalable application logic.
Database: PostgreSQL (optional) for efficient data management.
AI Integration: OpenAI GPT-4 for intelligent recommendations and quiz generation.

### Setup Instructions ⚙️
Follow these steps to set up XenLearn locally:

Clone the Repository 🗂️
```
git clone https://github.com/your-repo/xenlearn.git
cd XenLearn
```

Install Dependencies 📦
`pip install -r requirements.txt`


Configure Environment Variables 🔑

Set up the following environment variables in a .env file or your deployment platform:
DATABASE_URL: PostgreSQL connection string (optional, for database mode).
OPENAI_API_KEY: API key for OpenAI integration.


(Optional) Initialize Database 🗄️

If using PostgreSQL, run the database setup script:python initialize_database.py


Run the Application 🚀
streamlit run app.py


### Access XenLearn 🌍

Open your browser and navigate to http://localhost:8501 (or the URL provided by Replit).



### Usage 🖱️

Sign Up/Login: Create an account or log in to access personalized learning features.
Explore Courses: Browse the course catalog and receive AI-driven recommendations.
Take Quizzes: Engage with dynamically generated quizzes to test your knowledge.
Track Progress: Monitor your learning journey through detailed analytics and achievements.

### Contributing 🤝
We welcome contributions to XenLearn! To contribute:

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit your changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request.


Contact 📧
For questions, feedback, or support, please reach out to our team at srikara354@gmail.com or join our community on Discord.

Happy Learning with XenLearn! 🎓
