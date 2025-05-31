import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import hashlib
from utils.auth_manager import AuthManager
from utils.course_manager import CourseManager
from utils.ai_engine import AIEngine
from utils.progress_tracker import ProgressTracker
from utils.quiz_generator import QuizGenerator

# Configure page
st.set_page_config(
    page_title="EduLearn AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'current_course' not in st.session_state:
    st.session_state.current_course = None
if 'learning_preferences' not in st.session_state:
    st.session_state.learning_preferences = {}
if 'user_progress' not in st.session_state:
    st.session_state.user_progress = {}

def main():
    # Initialize managers
    auth_manager = AuthManager()
    course_manager = CourseManager()
    ai_engine = AIEngine()
    progress_tracker = ProgressTracker()
    quiz_generator = QuizGenerator()
    
    # Check authentication
    if st.session_state.user is None:
        show_auth_page(auth_manager)
    else:
        show_main_app(course_manager, ai_engine, progress_tracker, quiz_generator, auth_manager)

def show_auth_page(auth_manager):
    """Display authentication page"""
    st.title("🎓 EduLearn AI")
    st.markdown("**Personalized Learning Platform with AI-Powered Recommendations**")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            st.subheader("Login to Your Account")
            
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login", type="primary", use_container_width=True):
                user = auth_manager.authenticate_user(username, password)
                if user:
                    st.session_state.user = user
                    st.session_state.learning_preferences = user.get('preferences', {})
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        with tab2:
            st.subheader("Create New Account")
            
            new_username = st.text_input("Choose Username", key="signup_username")
            new_email = st.text_input("Email Address", key="signup_email")
            new_password = st.text_input("Create Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
            
            # Learning preferences setup
            st.write("**Learning Preferences:**")
            
            col_a, col_b = st.columns(2)
            with col_a:
                learning_style = st.selectbox(
                    "Learning Style",
                    ["Visual", "Auditory", "Kinesthetic", "Reading/Writing"],
                    key="signup_style"
                )
                difficulty_preference = st.selectbox(
                    "Preferred Difficulty",
                    ["Beginner", "Intermediate", "Advanced", "Mixed"],
                    key="signup_difficulty"
                )
            
            with col_b:
                study_time = st.selectbox(
                    "Daily Study Time",
                    ["15-30 minutes", "30-60 minutes", "1-2 hours", "2+ hours"],
                    key="signup_time"
                )
                interests = st.multiselect(
                    "Subject Interests",
                    ["Technology", "Science", "Mathematics", "Languages", "Business", "Arts", "History"],
                    key="signup_interests"
                )
            
            if st.button("Create Account", type="primary", use_container_width=True):
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters")
                elif not new_username or not new_email:
                    st.error("Please fill in all required fields")
                else:
                    preferences = {
                        'learning_style': learning_style,
                        'difficulty_preference': difficulty_preference,
                        'study_time': study_time,
                        'interests': interests
                    }
                    
                    user = auth_manager.create_user(new_username, new_email, new_password, preferences)
                    if user:
                        st.session_state.user = user
                        st.session_state.learning_preferences = preferences
                        st.success("Account created successfully!")
                        st.rerun()
                    else:
                        st.error("Username already exists")

def show_main_app(course_manager, ai_engine, progress_tracker, quiz_generator, auth_manager):
    """Display main application interface"""
    user = st.session_state.user
    
    # Sidebar
    with st.sidebar:
        st.title(f"Welcome, {user['username']}!")
        
        # Navigation
        page = st.selectbox(
            "Navigate",
            ["Dashboard", "Browse Courses", "My Learning", "AI Recommendations", "Quizzes", "Progress", "Settings"]
        )
        
        st.divider()
        
        # Quick stats
        user_progress = progress_tracker.get_user_progress(user['user_id'])
        st.metric("Courses Enrolled", len(user_progress.get('enrolled_courses', [])))
        st.metric("Completed Lessons", user_progress.get('completed_lessons', 0))
        st.metric("Learning Streak", user_progress.get('streak_days', 0))
        
        st.divider()
        
        if st.button("Logout", type="secondary"):
            st.session_state.user = None
            st.session_state.current_course = None
            st.rerun()
    
    # Main content area
    if page == "Dashboard":
        show_dashboard(course_manager, ai_engine, progress_tracker)
    elif page == "Browse Courses":
        show_course_browser(course_manager, ai_engine)
    elif page == "My Learning":
        show_my_learning(course_manager, progress_tracker)
    elif page == "AI Recommendations":
        show_ai_recommendations(ai_engine, course_manager)
    elif page == "Quizzes":
        show_quizzes(quiz_generator, course_manager)
    elif page == "Progress":
        show_progress_tracking(progress_tracker)
    elif page == "Settings":
        show_settings(auth_manager)

def show_dashboard(course_manager, ai_engine, progress_tracker):
    """Display user dashboard"""
    st.title("📊 Your Learning Dashboard")
    
    user = st.session_state.user
    user_progress = progress_tracker.get_user_progress(user['user_id'])
    
    # Welcome message and daily goal
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"### Good day, {user['username']}! 👋")
        daily_goal = user_progress.get('daily_goal_minutes', 30)
        time_today = user_progress.get('time_studied_today', 0)
        
        progress_pct = min(time_today / daily_goal * 100, 100) if daily_goal > 0 else 0
        st.progress(progress_pct / 100)
        st.write(f"Daily Goal: {time_today}/{daily_goal} minutes ({progress_pct:.0f}%)")
    
    with col2:
        st.metric("Total Points", user_progress.get('total_points', 0))
    
    with col3:
        st.metric("Current Level", user_progress.get('level', 1))
    
    # Recent activity and recommendations
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🔥 Continue Learning")
        
        enrolled_courses = user_progress.get('enrolled_courses', [])
        if enrolled_courses:
            for course_id in enrolled_courses[:3]:
                course = course_manager.get_course(course_id)
                if course:
                    with st.container():
                        st.write(f"**{course['title']}**")
                        course_progress = user_progress.get('course_progress', {}).get(course_id, 0)
                        st.progress(course_progress / 100)
                        st.write(f"Progress: {course_progress}%")
                        
                        if st.button(f"Continue", key=f"continue_{course_id}"):
                            st.session_state.current_course = course_id
                            st.rerun()
        else:
            st.info("No courses enrolled yet. Browse courses to get started!")
    
    with col2:
        st.subheader("🤖 AI Recommendations")
        
        # Get AI recommendations
        recommendations = ai_engine.get_personalized_recommendations(
            user['user_id'], 
            st.session_state.learning_preferences
        )
        
        for rec in recommendations[:3]:
            course = course_manager.get_course(rec['course_id'])
            if course:
                with st.container():
                    st.write(f"**{course['title']}**")
                    st.write(f"Match: {rec['confidence']:.0%}")
                    st.write(course['description'][:100] + "...")
                    
                    if st.button(f"View Course", key=f"view_{course['course_id']}"):
                        st.session_state.current_course = course['course_id']
                        st.rerun()

def show_course_browser(course_manager, ai_engine):
    """Display course browser with filtering and search"""
    st.title("📚 Browse Courses")
    
    # Search and filters
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_query = st.text_input("Search courses...", placeholder="Enter keywords")
    
    with col2:
        category_filter = st.selectbox(
            "Category",
            ["All"] + course_manager.get_categories()
        )
    
    with col3:
        difficulty_filter = st.selectbox(
            "Difficulty",
            ["All", "Beginner", "Intermediate", "Advanced"]
        )
    
    # Get filtered courses
    courses = course_manager.search_courses(search_query, category_filter, difficulty_filter)
    
    # Display courses
    if courses:
        for i in range(0, len(courses), 2):
            cols = st.columns(2)
            
            for j, col in enumerate(cols):
                if i + j < len(courses):
                    course = courses[i + j]
                    
                    with col:
                        with st.container():
                            st.subheader(course['title'])
                            st.write(f"**Category:** {course['category']}")
                            st.write(f"**Difficulty:** {course['difficulty']}")
                            st.write(f"**Duration:** {course['estimated_hours']} hours")
                            st.write(f"**Rating:** {'⭐' * int(course.get('rating', 0))} ({course.get('rating', 0)}/5)")
                            
                            st.write(course['description'])
                            
                            col_a, col_b = st.columns(2)
                            with col_a:
                                if st.button("View Details", key=f"view_details_{course['course_id']}"):
                                    show_course_details(course, course_manager)
                            
                            with col_b:
                                if st.button("Enroll", key=f"enroll_{course['course_id']}", type="primary"):
                                    enroll_in_course(course['course_id'], course_manager)
    else:
        st.info("No courses found matching your criteria.")

def show_course_details(course, course_manager):
    """Display detailed course information"""
    with st.expander(f"📚 Course Details: {course['title']}", expanded=True):
        st.write(f"**Description:** {course['description']}")
        st.write(f"**Category:** {course['category']}")
        st.write(f"**Difficulty Level:** {course['difficulty']}")
        st.write(f"**Estimated Duration:** {course['estimated_hours']} hours")
        
        # Course curriculum
        st.subheader("📋 Course Curriculum")
        lessons = course_manager.get_course_lessons(course['course_id'])
        
        for i, lesson in enumerate(lessons, 1):
            st.write(f"{i}. {lesson['title']} ({lesson['duration_minutes']} min)")
        
        # Prerequisites
        if course.get('prerequisites'):
            st.subheader("📚 Prerequisites")
            for prereq in course['prerequisites']:
                st.write(f"• {prereq}")
        
        # Learning outcomes
        if course.get('learning_outcomes'):
            st.subheader("🎯 Learning Outcomes")
            for outcome in course['learning_outcomes']:
                st.write(f"• {outcome}")

def enroll_in_course(course_id, course_manager):
    """Enroll user in a course"""
    user = st.session_state.user
    
    if course_manager.enroll_user(user['user_id'], course_id):
        st.success("Successfully enrolled in the course!")
        st.rerun()
    else:
        st.error("Failed to enroll. You may already be enrolled in this course.")

def show_my_learning(course_manager, progress_tracker):
    """Display user's enrolled courses and progress"""
    st.title("📖 My Learning")
    
    user = st.session_state.user
    user_progress = progress_tracker.get_user_progress(user['user_id'])
    enrolled_courses = user_progress.get('enrolled_courses', [])
    
    if not enrolled_courses:
        st.info("You haven't enrolled in any courses yet. Browse courses to get started!")
        return
    
    # Display enrolled courses
    for course_id in enrolled_courses:
        course = course_manager.get_course(course_id)
        if course:
            with st.expander(f"📚 {course['title']}", expanded=True):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    course_progress = user_progress.get('course_progress', {}).get(course_id, 0)
                    st.progress(course_progress / 100)
                    st.write(f"Progress: {course_progress}%")
                    
                    # Display lessons
                    lessons = course_manager.get_course_lessons(course_id)
                    completed_lessons = user_progress.get('completed_lessons_by_course', {}).get(course_id, [])
                    
                    for lesson in lessons:
                        is_completed = lesson['lesson_id'] in completed_lessons
                        status_icon = "✅" if is_completed else "⏳"
                        
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            st.write(f"{status_icon} {lesson['title']}")
                        with col_b:
                            if not is_completed:
                                if st.button("Start", key=f"start_{lesson['lesson_id']}"):
                                    start_lesson(lesson, course_id, progress_tracker)
                            else:
                                st.write("✓ Done")
                
                with col2:
                    st.metric("Lessons Completed", f"{len(completed_lessons)}/{len(lessons)}")
                    
                    time_spent = user_progress.get('time_spent_by_course', {}).get(course_id, 0)
                    st.metric("Time Spent", f"{time_spent} min")

def start_lesson(lesson, course_id, progress_tracker):
    """Start a lesson"""
    st.session_state.current_lesson = lesson
    st.session_state.current_course = course_id
    
    # Display lesson content
    st.subheader(f"📝 {lesson['title']}")
    
    # Lesson content (this would typically be rich content)
    st.write(lesson.get('content', 'Lesson content would be displayed here.'))
    
    # Mark as completed
    if st.button("Mark as Completed", type="primary"):
        progress_tracker.complete_lesson(
            st.session_state.user['user_id'],
            course_id,
            lesson['lesson_id']
        )
        st.success("Lesson completed! Great job!")
        st.rerun()

def show_ai_recommendations(ai_engine, course_manager):
    """Display AI-powered course recommendations"""
    st.title("🤖 AI-Powered Recommendations")
    
    user = st.session_state.user
    preferences = st.session_state.learning_preferences
    
    # Get personalized recommendations
    recommendations = ai_engine.get_personalized_recommendations(user['user_id'], preferences)
    
    if recommendations:
        st.subheader("Recommended for You")
        
        for rec in recommendations:
            course = course_manager.get_course(rec['course_id'])
            if course:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"### {course['title']}")
                        st.write(f"**Match Score:** {rec['confidence']:.0%}")
                        st.write(f"**Reason:** {rec['reason']}")
                        st.write(course['description'])
                        
                        # Tags
                        if course.get('tags'):
                            tag_text = " ".join([f"`{tag}`" for tag in course['tags']])
                            st.markdown(tag_text)
                    
                    with col2:
                        st.write(f"**Difficulty:** {course['difficulty']}")
                        st.write(f"**Duration:** {course['estimated_hours']} hours")
                        
                        if st.button(f"Enroll Now", key=f"ai_enroll_{course['course_id']}", type="primary"):
                            enroll_in_course(course['course_id'], course_manager)
                
                st.divider()
    else:
        st.info("No recommendations available. Try updating your learning preferences in Settings.")

def show_quizzes(quiz_generator, course_manager):
    """Display quiz interface"""
    st.title("🧠 Quizzes & Assessments")
    
    user = st.session_state.user
    
    # Quiz options
    tab1, tab2 = st.tabs(["Take Quiz", "Quiz History"])
    
    with tab1:
        st.subheader("Generate AI Quiz")
        
        # Quiz configuration
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.text_input("Quiz Topic", placeholder="e.g., Python basics, Machine Learning")
            difficulty = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
        
        with col2:
            num_questions = st.slider("Number of Questions", 5, 20, 10)
            quiz_type = st.selectbox("Quiz Type", ["Multiple Choice", "True/False", "Mixed"])
        
        if st.button("Generate Quiz", type="primary"):
            if topic:
                with st.spinner("Generating quiz questions..."):
                    quiz = quiz_generator.generate_quiz(topic, difficulty, num_questions, quiz_type)
                    
                    if quiz:
                        st.session_state.current_quiz = quiz
                        st.success("Quiz generated successfully!")
                        show_quiz_interface(quiz, quiz_generator)
                    else:
                        st.error("Failed to generate quiz. Please try again or check your topic.")
            else:
                st.warning("Please enter a quiz topic.")
    
    with tab2:
        st.subheader("Your Quiz History")
        
        quiz_history = quiz_generator.get_user_quiz_history(user['user_id'])
        
        if quiz_history:
            for quiz_record in quiz_history:
                with st.expander(f"Quiz: {quiz_record['topic']} - Score: {quiz_record['score']}%"):
                    st.write(f"**Date:** {quiz_record['date']}")
                    st.write(f"**Questions:** {quiz_record['total_questions']}")
                    st.write(f"**Correct:** {quiz_record['correct_answers']}")
                    st.write(f"**Time Taken:** {quiz_record['time_taken']} minutes")
        else:
            st.info("No quiz history available. Take your first quiz above!")

def show_quiz_interface(quiz, quiz_generator):
    """Display quiz taking interface"""
    st.subheader(f"Quiz: {quiz['topic']}")
    
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    
    # Display questions
    for i, question in enumerate(quiz['questions']):
        st.write(f"**Question {i+1}:** {question['question']}")
        
        if question['type'] == 'multiple_choice':
            answer = st.radio(
                f"Select your answer:",
                question['options'],
                key=f"q_{i}",
                index=None
            )
            st.session_state.quiz_answers[i] = answer
            
        elif question['type'] == 'true_false':
            answer = st.radio(
                f"True or False?",
                ["True", "False"],
                key=f"q_{i}",
                index=None
            )
            st.session_state.quiz_answers[i] = answer
        
        st.divider()
    
    # Submit quiz
    if st.button("Submit Quiz", type="primary"):
        score = quiz_generator.calculate_score(quiz, st.session_state.quiz_answers)
        
        st.success(f"Quiz completed! Your score: {score['percentage']}%")
        st.write(f"Correct answers: {score['correct']}/{score['total']}")
        
        # Save quiz result
        quiz_generator.save_quiz_result(
            st.session_state.user['user_id'],
            quiz,
            st.session_state.quiz_answers,
            score
        )
        
        # Clear quiz state
        del st.session_state.current_quiz
        del st.session_state.quiz_answers

def show_progress_tracking(progress_tracker):
    """Display progress tracking and analytics"""
    st.title("📈 Progress Tracking")
    
    user = st.session_state.user
    progress_data = progress_tracker.get_detailed_progress(user['user_id'])
    
    # Progress overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Study Time", f"{progress_data.get('total_minutes', 0)} min")
    
    with col2:
        st.metric("Courses Completed", progress_data.get('completed_courses', 0))
    
    with col3:
        st.metric("Current Streak", f"{progress_data.get('streak_days', 0)} days")
    
    with col4:
        st.metric("Achievement Points", progress_data.get('total_points', 0))
    
    # Progress charts
    tab1, tab2, tab3 = st.tabs(["Learning Trends", "Course Progress", "Achievements"])
    
    with tab1:
        st.subheader("📊 Learning Trends")
        
        # Daily study time chart
        if progress_data.get('daily_study_time'):
            dates = list(progress_data['daily_study_time'].keys())
            times = list(progress_data['daily_study_time'].values())
            
            chart_data = pd.DataFrame({
                'Date': pd.to_datetime(dates),
                'Study Time (minutes)': times
            })
            
            st.line_chart(chart_data.set_index('Date'))
        else:
            st.info("Start learning to see your progress trends!")
    
    with tab2:
        st.subheader("📚 Course Progress")
        
        course_progress = progress_data.get('course_progress', {})
        if course_progress:
            for course_id, progress in course_progress.items():
                course_manager = CourseManager()
                course = course_manager.get_course(course_id)
                if course:
                    st.write(f"**{course['title']}**")
                    st.progress(progress / 100)
                    st.write(f"{progress}% completed")
        else:
            st.info("Enroll in courses to track your progress!")
    
    with tab3:
        st.subheader("🏆 Achievements")
        
        achievements = progress_data.get('achievements', [])
        if achievements:
            for achievement in achievements:
                with st.container():
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.write(achievement['icon'])
                    with col2:
                        st.write(f"**{achievement['title']}**")
                        st.write(achievement['description'])
                        st.write(f"Earned: {achievement['date']}")
        else:
            st.info("Keep learning to earn achievements!")

def show_settings(auth_manager):
    """Display user settings and preferences"""
    st.title("⚙️ Settings")
    
    user = st.session_state.user
    
    tab1, tab2, tab3 = st.tabs(["Learning Preferences", "Account Settings", "Notifications"])
    
    with tab1:
        st.subheader("🎯 Learning Preferences")
        
        with st.form("preferences_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                learning_style = st.selectbox(
                    "Learning Style",
                    ["Visual", "Auditory", "Kinesthetic", "Reading/Writing"],
                    index=["Visual", "Auditory", "Kinesthetic", "Reading/Writing"].index(
                        st.session_state.learning_preferences.get('learning_style', 'Visual')
                    )
                )
                
                difficulty_preference = st.selectbox(
                    "Preferred Difficulty",
                    ["Beginner", "Intermediate", "Advanced", "Mixed"],
                    index=["Beginner", "Intermediate", "Advanced", "Mixed"].index(
                        st.session_state.learning_preferences.get('difficulty_preference', 'Beginner')
                    )
                )
            
            with col2:
                study_time = st.selectbox(
                    "Daily Study Time",
                    ["15-30 minutes", "30-60 minutes", "1-2 hours", "2+ hours"],
                    index=["15-30 minutes", "30-60 minutes", "1-2 hours", "2+ hours"].index(
                        st.session_state.learning_preferences.get('study_time', '30-60 minutes')
                    )
                )
                
                interests = st.multiselect(
                    "Subject Interests",
                    ["Technology", "Science", "Mathematics", "Languages", "Business", "Arts", "History"],
                    default=st.session_state.learning_preferences.get('interests', [])
                )
            
            daily_goal = st.slider(
                "Daily Study Goal (minutes)",
                15, 180, 
                st.session_state.learning_preferences.get('daily_goal_minutes', 30),
                step=15
            )
            
            if st.form_submit_button("Save Preferences", type="primary"):
                new_preferences = {
                    'learning_style': learning_style,
                    'difficulty_preference': difficulty_preference,
                    'study_time': study_time,
                    'interests': interests,
                    'daily_goal_minutes': daily_goal
                }
                
                if auth_manager.update_user_preferences(user['user_id'], new_preferences):
                    st.session_state.learning_preferences = new_preferences
                    st.success("Preferences updated successfully!")
                else:
                    st.error("Failed to update preferences.")
    
    with tab2:
        st.subheader("👤 Account Settings")
        
        with st.form("account_form"):
            new_email = st.text_input("Email", value=user.get('email', ''))
            
            st.write("**Change Password**")
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_new_password = st.text_input("Confirm New Password", type="password")
            
            if st.form_submit_button("Update Account", type="primary"):
                if new_password and new_password != confirm_new_password:
                    st.error("New passwords do not match")
                elif new_password and len(new_password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    if auth_manager.update_user_account(user['user_id'], new_email, current_password, new_password):
                        st.success("Account updated successfully!")
                    else:
                        st.error("Failed to update account. Check your current password.")
    
    with tab3:
        st.subheader("🔔 Notification Settings")
        
        with st.form("notifications_form"):
            email_notifications = st.checkbox("Email Notifications", value=True)
            daily_reminders = st.checkbox("Daily Study Reminders", value=True)
            achievement_alerts = st.checkbox("Achievement Notifications", value=True)
            course_updates = st.checkbox("Course Update Notifications", value=True)
            
            reminder_time = st.time_input("Daily Reminder Time", value=datetime.strptime("18:00", "%H:%M").time())
            
            if st.form_submit_button("Save Notification Settings", type="primary"):
                notification_settings = {
                    'email_notifications': email_notifications,
                    'daily_reminders': daily_reminders,
                    'achievement_alerts': achievement_alerts,
                    'course_updates': course_updates,
                    'reminder_time': reminder_time.strftime("%H:%M")
                }
                
                st.success("Notification settings saved!")

if __name__ == "__main__":
    main()