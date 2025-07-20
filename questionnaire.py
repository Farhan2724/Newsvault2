# questionnaire.py
from typing import Dict, List, Any
from user_profile import (
    UserProfile, UserProfileManager, 
    InvestmentFrequency, RiskAppetite, 
    InvestmentHorizon, ExperienceLevel
)

class InvestmentQuestionnaire:
    def __init__(self):
        self.profile_manager = UserProfileManager()
        self.questions = self._setup_questions()
    
    def _setup_questions(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "frequency",
                "question": "How frequently do you plan to invest?",
                "type": "single_choice",
                "options": [
                    {"value": "daily", "label": "Daily - Active trading"},
                    {"value": "weekly", "label": "Weekly - Regular contributions"},
                    {"value": "monthly", "label": "Monthly - Steady investing"},
                    {"value": "quarterly", "label": "Quarterly - Periodic investments"},
                    {"value": "yearly", "label": "Yearly - Annual contributions"}
                ]
            },
            {
                "id": "industries",
                "question": "Which industries interest you most? (Select up to 4)",
                "type": "multiple_choice",
                "max_selections": 4,
                "options": [
                    {"value": "technology", "label": "Technology & Software"},
                    {"value": "healthcare", "label": "Healthcare & Biotech"},
                    {"value": "finance", "label": "Financial Services"},
                    {"value": "energy", "label": "Energy & Utilities"},
                    {"value": "consumer", "label": "Consumer Goods & Retail"},
                    {"value": "real_estate", "label": "Real Estate"},
                    {"value": "telecommunications", "label": "Telecommunications"},
                    {"value": "manufacturing", "label": "Manufacturing & Industrial"},
                    {"value": "aerospace", "label": "Aerospace & Defense"},
                    {"value": "media", "label": "Media & Entertainment"}
                ]
            },
            {
                "id": "horizon",
                "question": "What is your investment time horizon?",
                "type": "single_choice",
                "options": [
                    {"value": "short_term", "label": "Short-term (Less than 1 year)"},
                    {"value": "medium_term", "label": "Medium-term (1-5 years)"},
                    {"value": "long_term", "label": "Long-term (More than 5 years)"}
                ]
            },
            {
                "id": "period",
                "question": "How long do you plan to invest regularly?",
                "type": "text_input",
                "placeholder": "e.g., '2 years', '5-10 years', 'indefinitely'"
            },
            {
                "id": "risk",
                "question": "What is your risk tolerance?",
                "type": "single_choice",
                "options": [
                    {"value": "low", "label": "Low - Prefer stable, predictable returns"},
                    {"value": "medium", "label": "Medium - Balanced growth with some risk"},
                    {"value": "high", "label": "High - Aggressive growth, comfortable with volatility"},
                    {"value": "very_high", "label": "Very High - Maximum growth potential, high risk tolerance"}
                ]
            },
            {
                "id": "experience",
                "question": "What is your investment experience level?",
                "type": "single_choice",
                "options": [
                    {"value": "beginner", "label": "Beginner - New to investing"},
                    {"value": "intermediate", "label": "Intermediate - Some experience with basic investments"},
                    {"value": "advanced", "label": "Advanced - Experienced with various investment types"},
                    {"value": "expert", "label": "Expert - Sophisticated investor with deep market knowledge"}
                ]
            }
        ]
    
    def display_question(self, question_id: int) -> Dict[str, Any]:
        """Display a specific question"""
        if 0 <= question_id < len(self.questions):
            return self.questions[question_id]
        return None
    
    def get_all_questions(self) -> List[Dict[str, Any]]:
        """Get all questions for form rendering"""
        return self.questions
    
    def validate_responses(self, responses: Dict[str, Any]) -> List[str]:
        """Validate user responses and return list of errors"""
        errors = []
        
        # Check required fields
        required_fields = ["frequency", "industries", "horizon", "period", "risk", "experience"]
        for field in required_fields:
            if field not in responses or not responses[field]:
                errors.append(f"Please answer the {field} question")
        
        # Validate industry selections
        if "industries" in responses:
            if not isinstance(responses["industries"], list):
                errors.append("Industries must be a list")
            elif len(responses["industries"]) == 0:
                errors.append("Please select at least one industry")
            elif len(responses["industries"]) > 4:
                errors.append("Please select no more than 4 industries")
        
        # Validate enum values
        try:
            if "frequency" in responses:
                InvestmentFrequency(responses["frequency"])
        except ValueError:
            errors.append("Invalid investment frequency")
        
        try:
            if "horizon" in responses:
                InvestmentHorizon(responses["horizon"])
        except ValueError:
            errors.append("Invalid investment horizon")
        
        try:
            if "risk" in responses:
                RiskAppetite(responses["risk"])
        except ValueError:
            errors.append("Invalid risk appetite")
        
        try:
            if "experience" in responses:
                ExperienceLevel(responses["experience"])
        except ValueError:
            errors.append("Invalid experience level")
        
        return errors
    
    def create_profile_from_responses(self, user_id: str, responses: Dict[str, Any]) -> UserProfile:
        """Create user profile from questionnaire responses"""
        # Validate responses first
        errors = self.validate_responses(responses)
        if errors:
            raise ValueError(f"Invalid responses: {', '.join(errors)}")
        
        # Create profile
        profile = self.profile_manager.create_profile(user_id, responses)
        return profile
    
    def get_recommendation_preview(self, responses: Dict[str, Any]) -> str:
        """Generate a preview of what kind of news the user would receive"""
        if not responses:
            return "Complete the questionnaire to see your personalized news preview"
        
        preview = "Based on your responses, you'll receive:\n\n"
        
        # Investment frequency
        freq_map = {
            "daily": "Daily market updates and breaking news",
            "weekly": "Weekly market summaries and trend analysis",
            "monthly": "Monthly market reports and investment insights",
            "quarterly": "Quarterly portfolio reviews and market outlook",
            "yearly": "Annual market analysis and long-term projections"
        }
        
        if "frequency" in responses:
            preview += f"📅 {freq_map.get(responses['frequency'], 'Regular updates')}\n"
        
        # Industries
        if "industries" in responses and responses["industries"]:
            industry_labels = {
                "technology": "Tech & Software",
                "healthcare": "Healthcare & Biotech",
                "finance": "Financial Services",
                "energy": "Energy & Utilities",
                "consumer": "Consumer Goods",
                "real_estate": "Real Estate",
                "telecommunications": "Telecom",
                "manufacturing": "Manufacturing",
                "aerospace": "Aerospace & Defense",
                "media": "Media & Entertainment"
            }
            
            selected_industries = [industry_labels.get(ind, ind.title()) for ind in responses["industries"]]
            preview += f"🏭 Focus on: {', '.join(selected_industries)}\n"
        
        # Risk level
        risk_content = {
            "low": "Conservative investment opportunities and stable market news",
            "medium": "Balanced mix of growth opportunities and risk assessments",
            "high": "Growth-focused content with emerging market opportunities",
            "very_high": "High-growth investments, volatility analysis, and aggressive strategies"
        }
        
        if "risk" in responses:
            preview += f"📊 {risk_content.get(responses['risk'], 'Balanced content')}\n"
        
        # Experience level
        exp_content = {
            "beginner": "Educational content, basic concepts, and beginner-friendly analysis",
            "intermediate": "Intermediate strategies, market analysis, and portfolio tips",
            "advanced": "Advanced techniques, detailed analysis, and complex strategies",
            "expert": "Expert-level insights, sophisticated analysis, and cutting-edge strategies"
        }
        
        if "experience" in responses:
            preview += f"🎓 {exp_content.get(responses['experience'], 'Appropriate content')}\n"
        
        # Investment horizon
        horizon_content = {
            "short_term": "Short-term market movements and quick opportunities",
            "medium_term": "Medium-term trends and strategic positioning",
            "long_term": "Long-term investment themes and fundamental analysis"
        }
        
        if "horizon" in responses:
            preview += f"⏰ {horizon_content.get(responses['horizon'], 'Time-appropriate content')}\n"
        
        preview += "\n✨ All content will be personalized based on your preferences!"
        
        return preview
    
    def get_question_by_id(self, question_id: str) -> Dict[str, Any]:
        """Get a specific question by its ID"""
        for question in self.questions:
            if question["id"] == question_id:
                return question
        return None
    
    def get_progress_percentage(self, completed_questions: List[str]) -> float:
        """Calculate completion percentage"""
        if not self.questions:
            return 0.0
        
        total_questions = len(self.questions)
        completed_count = len(completed_questions)
        
        return min(100.0, (completed_count / total_questions) * 100.0)
    
    def get_next_question_id(self, completed_questions: List[str]) -> str:
        """Get the next question ID to display"""
        for question in self.questions:
            if question["id"] not in completed_questions:
                return question["id"]
        return None
    
    def export_responses(self, responses: Dict[str, Any]) -> Dict[str, Any]:
        """Export responses with question labels for better readability"""
        export_data = {}
        
        for question in self.questions:
            question_id = question["id"]
            if question_id in responses:
                export_data[question_id] = {
                    "question": question["question"],
                    "response": responses[question_id],
                    "type": question["type"]
                }
                
                # Add human-readable labels for single choice questions
                if question["type"] == "single_choice":
                    for option in question["options"]:
                        if option["value"] == responses[question_id]:
                            export_data[question_id]["response_label"] = option["label"]
                            break
                
                # Add human-readable labels for multiple choice questions
                elif question["type"] == "multiple_choice":
                    labels = []
                    for option in question["options"]:
                        if option["value"] in responses[question_id]:
                            labels.append(option["label"])
                    export_data[question_id]["response_labels"] = labels
        
        return export_data