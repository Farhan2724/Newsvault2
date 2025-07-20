# user_profile.py
from dataclasses import dataclass
from typing import List, Dict, Any
from enum import Enum
import json

class InvestmentFrequency(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"

class RiskAppetite(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

class InvestmentHorizon(Enum):
    SHORT_TERM = "short_term"  # < 1 year
    MEDIUM_TERM = "medium_term"  # 1-5 years
    LONG_TERM = "long_term"  # > 5 years

class ExperienceLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

@dataclass
class UserProfile:
    user_id: str
    investment_frequency: InvestmentFrequency
    industry_preferences: List[str]  # max 4-5 industries
    investment_horizon: InvestmentHorizon
    investment_period: str  # flexible string
    risk_appetite: RiskAppetite
    experience_level: ExperienceLevel
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'investment_frequency': self.investment_frequency.value,
            'industry_preferences': self.industry_preferences,
            'investment_horizon': self.investment_horizon.value,
            'investment_period': self.investment_period,
            'risk_appetite': self.risk_appetite.value,
            'experience_level': self.experience_level.value
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfile':
        return cls(
            user_id=data['user_id'],
            investment_frequency=InvestmentFrequency(data['investment_frequency']),
            industry_preferences=data['industry_preferences'],
            investment_horizon=InvestmentHorizon(data['investment_horizon']),
            investment_period=data['investment_period'],
            risk_appetite=RiskAppetite(data['risk_appetite']),
            experience_level=ExperienceLevel(data['experience_level'])
        )

class UserProfileManager:
    def __init__(self, storage_path: str = "user_profiles.json"):
        self.storage_path = storage_path
        self.profiles = self._load_profiles()
    
    def _load_profiles(self) -> Dict[str, UserProfile]:
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                return {
                    user_id: UserProfile.from_dict(profile_data)
                    for user_id, profile_data in data.items()
                }
        except FileNotFoundError:
            return {}
    
    def _save_profiles(self):
        data = {
            user_id: profile.to_dict()
            for user_id, profile in self.profiles.items()
        }
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def create_profile(self, user_id: str, responses: Dict[str, Any]) -> UserProfile:
        """Create user profile from questionnaire responses"""
        profile = UserProfile(
            user_id=user_id,
            investment_frequency=InvestmentFrequency(responses['frequency']),
            industry_preferences=responses['industries'],
            investment_horizon=InvestmentHorizon(responses['horizon']),
            investment_period=responses['period'],
            risk_appetite=RiskAppetite(responses['risk']),
            experience_level=ExperienceLevel(responses['experience'])
        )
        
        self.profiles[user_id] = profile
        self._save_profiles()
        return profile
    
    def get_profile(self, user_id: str) -> UserProfile:
        return self.profiles.get(user_id)
    
    def update_profile(self, user_id: str, updates: Dict[str, Any]) -> UserProfile:
        if user_id not in self.profiles:
            raise ValueError(f"Profile for user {user_id} not found")
        
        profile = self.profiles[user_id]
        for key, value in updates.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        
        self._save_profiles()
        return profile

# Industry mapping for news filtering
INDUSTRY_KEYWORDS = {
    'technology': ['tech', 'software', 'AI', 'artificial intelligence', 'cloud', 'cybersecurity', 'semiconductor'],
    'healthcare': ['healthcare', 'pharma', 'biotech', 'medical', 'drug', 'vaccine', 'clinical'],
    'finance': ['bank', 'financial', 'fintech', 'insurance', 'credit', 'loan', 'payment'],
    'energy': ['oil', 'gas', 'renewable', 'solar', 'wind', 'energy', 'utilities'],
    'consumer': ['retail', 'consumer', 'e-commerce', 'brand', 'restaurant', 'automotive'],
    'real_estate': ['real estate', 'REIT', 'property', 'construction', 'housing'],
    'telecommunications': ['telecom', 'wireless', '5G', 'network', 'infrastructure']
}