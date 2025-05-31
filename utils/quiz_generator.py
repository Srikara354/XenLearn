import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
import streamlit as st

class QuizGenerator:
    """Handles AI-powered quiz generation and management"""
    
    def __init__(self):
        self.quizzes_file = "data/quizzes.json"
        self.quiz_results_file = "data/quiz_results.json"
        self._ensure_data_directory()
        self._load_data()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        import os
        if not os.path.exists("data"):
            os.makedirs("data")
    
    def _load_data(self):
        """Load quiz data from JSON files"""
        try:
            with open(self.quizzes_file, 'r') as f:
                self.quizzes = json.load(f)
        except FileNotFoundError:
            self.quizzes = {}
        
        try:
            with open(self.quiz_results_file, 'r') as f:
                self.quiz_results = json.load(f)
        except FileNotFoundError:
            self.quiz_results = {}
    
    def _save_quizzes(self):
        """Save quizzes to JSON file"""
        try:
            with open(self.quizzes_file, 'w') as f:
                json.dump(self.quizzes, f, indent=2, default=str)
        except Exception as e:
            st.error(f"Error saving quizzes: {str(e)}")
    
    def _save_quiz_results(self):
        """Save quiz results to JSON file"""
        try:
            with open(self.quiz_results_file, 'w') as f:
                json.dump(self.quiz_results, f, indent=2, default=str)
        except Exception as e:
            st.error(f"Error saving quiz results: {str(e)}")
    
    def generate_quiz(self, topic: str, difficulty: str, num_questions: int, quiz_type: str) -> Optional[Dict[str, Any]]:
        """Generate a quiz using AI or predefined templates"""
        try:
            # Check if we need OpenAI API for dynamic quiz generation
            has_openai = self._check_openai_availability()
            
            if has_openai:
                return self._generate_ai_quiz(topic, difficulty, num_questions, quiz_type)
            else:
                return self._generate_template_quiz(topic, difficulty, num_questions, quiz_type)
                
        except Exception as e:
            st.error(f"Error generating quiz: {str(e)}")
            return None
    
    def _check_openai_availability(self) -> bool:
        """Check if OpenAI API is available"""
        try:
            import os
            return bool(os.environ.get("OPENAI_API_KEY"))
        except:
            return False
    
    def _generate_ai_quiz(self, topic: str, difficulty: str, num_questions: int, quiz_type: str) -> Optional[Dict[str, Any]]:
        """Generate quiz using OpenAI API"""
        try:
            from openai import OpenAI
            import os
            
            client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            
            # Create prompt for quiz generation
            prompt = self._create_quiz_prompt(topic, difficulty, num_questions, quiz_type)
            
            response = client.chat.completions.create(
                model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
                messages=[
                    {"role": "system", "content": "You are an expert quiz generator. Create educational quizzes in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            quiz_data = json.loads(response.choices[0].message.content)
            
            # Add metadata
            quiz_id = str(uuid.uuid4())
            quiz = {
                'quiz_id': quiz_id,
                'topic': topic,
                'difficulty': difficulty,
                'num_questions': num_questions,
                'quiz_type': quiz_type,
                'questions': quiz_data.get('questions', []),
                'created_at': datetime.now().isoformat(),
                'generated_by': 'ai'
            }
            
            # Save quiz
            self.quizzes[quiz_id] = quiz
            self._save_quizzes()
            
            return quiz
            
        except Exception as e:
            st.error(f"Error generating AI quiz: {str(e)}")
            # Fall back to template quiz
            return self._generate_template_quiz(topic, difficulty, num_questions, quiz_type)
    
    def _create_quiz_prompt(self, topic: str, difficulty: str, num_questions: int, quiz_type: str) -> str:
        """Create prompt for AI quiz generation"""
        prompt = f"""
        Generate a {difficulty.lower()} level quiz about "{topic}" with {num_questions} questions.
        
        Requirements:
        - Quiz type: {quiz_type}
        - Difficulty: {difficulty}
        - Questions should be educational and accurate
        - Include clear, concise questions
        - Provide 4 options for multiple choice questions
        - Mark the correct answer
        
        Return the quiz in this JSON format:
        {{
            "questions": [
                {{
                    "question": "Question text here",
                    "type": "multiple_choice" or "true_false",
                    "options": ["A", "B", "C", "D"] (for multiple choice only),
                    "correct_answer": "correct option text",
                    "explanation": "Brief explanation of why this is correct"
                }}
            ]
        }}
        
        Make sure all questions are relevant to {topic} and appropriate for {difficulty} level learners.
        """
        return prompt
    
    def _generate_template_quiz(self, topic: str, difficulty: str, num_questions: int, quiz_type: str) -> Dict[str, Any]:
        """Generate quiz using predefined templates"""
        quiz_id = str(uuid.uuid4())
        
        # Template questions based on common topics
        template_questions = self._get_template_questions(topic.lower(), difficulty.lower())
        
        # Select questions based on requested number and type
        selected_questions = []
        for i, template_q in enumerate(template_questions[:num_questions]):
            if quiz_type == "True/False" or (quiz_type == "Mixed" and i % 2 == 0):
                question = {
                    "question": template_q["question"],
                    "type": "true_false",
                    "options": ["True", "False"],
                    "correct_answer": template_q.get("tf_answer", "True"),
                    "explanation": template_q.get("explanation", "")
                }
            else:
                question = {
                    "question": template_q["question"],
                    "type": "multiple_choice",
                    "options": template_q.get("options", ["A", "B", "C", "D"]),
                    "correct_answer": template_q.get("correct_answer", "A"),
                    "explanation": template_q.get("explanation", "")
                }
            selected_questions.append(question)
        
        quiz = {
            'quiz_id': quiz_id,
            'topic': topic,
            'difficulty': difficulty,
            'num_questions': len(selected_questions),
            'quiz_type': quiz_type,
            'questions': selected_questions,
            'created_at': datetime.now().isoformat(),
            'generated_by': 'template'
        }
        
        # Save quiz
        self.quizzes[quiz_id] = quiz
        self._save_quizzes()
        
        return quiz
    
    def _get_template_questions(self, topic: str, difficulty: str) -> List[Dict[str, Any]]:
        """Get template questions for common topics"""
        templates = {
            "python": [
                {
                    "question": "What is Python primarily used for?",
                    "options": ["Web development", "Data science", "Automation", "All of the above"],
                    "correct_answer": "All of the above",
                    "tf_answer": "True",
                    "explanation": "Python is a versatile language used in many domains."
                },
                {
                    "question": "Which keyword is used to define a function in Python?",
                    "options": ["function", "def", "define", "func"],
                    "correct_answer": "def",
                    "explanation": "The 'def' keyword is used to define functions in Python."
                },
                {
                    "question": "Python is an interpreted language.",
                    "tf_answer": "True",
                    "explanation": "Python code is executed line by line by the Python interpreter."
                },
                {
                    "question": "Lists in Python are mutable.",
                    "tf_answer": "True",
                    "explanation": "Lists can be modified after creation, making them mutable."
                }
            ],
            "machine learning": [
                {
                    "question": "What is supervised learning?",
                    "options": ["Learning with labeled data", "Learning without labels", "Learning with rewards", "Learning by observation"],
                    "correct_answer": "Learning with labeled data",
                    "explanation": "Supervised learning uses labeled examples to train models."
                },
                {
                    "question": "Which algorithm is commonly used for classification?",
                    "options": ["Linear Regression", "K-Means", "Decision Tree", "PCA"],
                    "correct_answer": "Decision Tree",
                    "explanation": "Decision trees are popular classification algorithms."
                },
                {
                    "question": "Neural networks are inspired by the human brain.",
                    "tf_answer": "True",
                    "explanation": "Neural networks mimic the structure of biological neural networks."
                }
            ],
            "data science": [
                {
                    "question": "What does pandas library primarily handle?",
                    "options": ["Images", "Data manipulation", "Web scraping", "Machine learning"],
                    "correct_answer": "Data manipulation",
                    "explanation": "Pandas is mainly used for data manipulation and analysis."
                },
                {
                    "question": "Which visualization library is most popular in Python?",
                    "options": ["Seaborn", "Matplotlib", "Plotly", "Bokeh"],
                    "correct_answer": "Matplotlib",
                    "explanation": "Matplotlib is the most widely used plotting library in Python."
                }
            ],
            "marketing": [
                {
                    "question": "What does SEO stand for?",
                    "options": ["Search Engine Optimization", "Social Engagement Online", "Sales Enhancement Operation", "Site Efficiency Optimization"],
                    "correct_answer": "Search Engine Optimization",
                    "explanation": "SEO refers to optimizing content for search engines."
                },
                {
                    "question": "Content marketing focuses on creating valuable content.",
                    "tf_answer": "True",
                    "explanation": "Content marketing aims to provide value to attract and engage audiences."
                }
            ],
            "mathematics": [
                {
                    "question": "What is the derivative of x²?",
                    "options": ["x", "2x", "x²", "2"],
                    "correct_answer": "2x",
                    "explanation": "Using the power rule: d/dx(x²) = 2x."
                },
                {
                    "question": "The limit of a function always exists.",
                    "tf_answer": "False",
                    "explanation": "Limits may not exist if the function approaches different values from different directions."
                }
            ]
        }
        
        # Default questions if topic not found
        default_questions = [
            {
                "question": f"This is a {difficulty} level question about {topic}.",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "Option A",
                "tf_answer": "True",
                "explanation": "This is a template explanation."
            }
        ]
        
        # Find matching template questions
        for key in templates:
            if key in topic:
                return templates[key]
        
        return default_questions
    
    def calculate_score(self, quiz: Dict[str, Any], user_answers: Dict[int, str]) -> Dict[str, Any]:
        """Calculate quiz score"""
        try:
            questions = quiz['questions']
            correct_count = 0
            total_questions = len(questions)
            
            for i, question in enumerate(questions):
                user_answer = user_answers.get(i)
                correct_answer = question['correct_answer']
                
                if user_answer == correct_answer:
                    correct_count += 1
            
            percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
            
            return {
                'correct': correct_count,
                'total': total_questions,
                'percentage': round(percentage, 1)
            }
            
        except Exception as e:
            st.error(f"Error calculating score: {str(e)}")
            return {'correct': 0, 'total': 0, 'percentage': 0}
    
    def save_quiz_result(self, user_id: str, quiz: Dict[str, Any], user_answers: Dict[int, str], score: Dict[str, Any]):
        """Save quiz result for a user"""
        try:
            if user_id not in self.quiz_results:
                self.quiz_results[user_id] = []
            
            result = {
                'quiz_id': quiz['quiz_id'],
                'topic': quiz['topic'],
                'difficulty': quiz['difficulty'],
                'score': score['percentage'],
                'correct_answers': score['correct'],
                'total_questions': score['total'],
                'user_answers': user_answers,
                'date': datetime.now().isoformat(),
                'time_taken': 0  # This would be calculated in a real implementation
            }
            
            self.quiz_results[user_id].append(result)
            self._save_quiz_results()
            
            # Record in progress tracker
            from utils.progress_tracker import ProgressTracker
            progress_tracker = ProgressTracker()
            progress_tracker.record_quiz_result(user_id, quiz['topic'], score['percentage'])
            
        except Exception as e:
            st.error(f"Error saving quiz result: {str(e)}")
    
    def get_user_quiz_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Get quiz history for a user"""
        return self.quiz_results.get(user_id, [])
    
    def get_quiz_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get quiz analytics for a user"""
        try:
            user_results = self.quiz_results.get(user_id, [])
            
            if not user_results:
                return {}
            
            total_quizzes = len(user_results)
            total_score = sum(result['score'] for result in user_results)
            average_score = total_score / total_quizzes if total_quizzes > 0 else 0
            
            # Topic performance
            topic_performance = {}
            for result in user_results:
                topic = result['topic']
                if topic not in topic_performance:
                    topic_performance[topic] = {'scores': [], 'count': 0}
                topic_performance[topic]['scores'].append(result['score'])
                topic_performance[topic]['count'] += 1
            
            # Calculate average per topic
            for topic in topic_performance:
                scores = topic_performance[topic]['scores']
                topic_performance[topic]['average'] = sum(scores) / len(scores)
            
            analytics = {
                'total_quizzes_taken': total_quizzes,
                'average_score': round(average_score, 1),
                'best_score': max(result['score'] for result in user_results),
                'recent_performance': [result['score'] for result in user_results[-5:]],
                'topic_performance': topic_performance,
                'improvement_trend': self._calculate_improvement_trend(user_results)
            }
            
            return analytics
            
        except Exception as e:
            st.error(f"Error getting quiz analytics: {str(e)}")
            return {}
    
    def _calculate_improvement_trend(self, results: List[Dict[str, Any]]) -> str:
        """Calculate if user performance is improving"""
        if len(results) < 3:
            return "insufficient_data"
        
        recent_scores = [result['score'] for result in results[-3:]]
        early_scores = [result['score'] for result in results[:3]]
        
        recent_avg = sum(recent_scores) / len(recent_scores)
        early_avg = sum(early_scores) / len(early_scores)
        
        if recent_avg > early_avg + 5:
            return "improving"
        elif recent_avg < early_avg - 5:
            return "declining"
        else:
            return "stable"
    
    def generate_adaptive_quiz(self, user_id: str, topic: str) -> Optional[Dict[str, Any]]:
        """Generate adaptive quiz based on user's past performance"""
        try:
            user_results = self.quiz_results.get(user_id, [])
            
            # Determine difficulty based on past performance
            topic_results = [r for r in user_results if topic.lower() in r['topic'].lower()]
            
            if not topic_results:
                difficulty = "Beginner"
            else:
                avg_score = sum(r['score'] for r in topic_results) / len(topic_results)
                if avg_score >= 80:
                    difficulty = "Advanced"
                elif avg_score >= 60:
                    difficulty = "Intermediate"
                else:
                    difficulty = "Beginner"
            
            # Generate quiz with adaptive difficulty
            return self.generate_quiz(topic, difficulty, 10, "Mixed")
            
        except Exception as e:
            st.error(f"Error generating adaptive quiz: {str(e)}")
            return None