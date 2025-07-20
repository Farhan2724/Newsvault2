# crew.py
from crewai import Crew
from user_profile import UserProfile
from tasks.news_curation_task import (
    create_news_curation_task,
    create_summarization_task,
    create_relevance_scoring_task
)
from agents.news_curator_agent import (
    create_news_curator_agent,
    summarizer_agent,
    relevance_scorer_agent
)

class NewsAICrew:
    def __init__(self, user_profile: UserProfile):
        self.user_profile = user_profile
        self.curator_agent = create_news_curator_agent(user_profile)
        
        # Create tasks
        self.curation_task = create_news_curation_task(user_profile)
        self.summarization_task = create_summarization_task(user_profile)
        self.relevance_task = create_relevance_scoring_task(user_profile)
        
        # Create crew
        self.crew = Crew(
            agents=[self.curator_agent, summarizer_agent, relevance_scorer_agent],
            tasks=[self.curation_task, self.summarization_task, self.relevance_task],
            verbose=True
        )
    
    def generate_news_digest(self) -> str:
        """Generate personalized news digest for the user"""
        result = self.crew.kickoff()
        return result
    
    def update_user_profile(self, new_profile: UserProfile):
        """Update user profile and recreate agents/tasks"""
        self.user_profile = new_profile
        self.curator_agent = create_news_curator_agent(new_profile)
        self.curation_task = create_news_curation_task(new_profile)
        self.summarization_task = create_summarization_task(new_profile)
        self.relevance_task = create_relevance_scoring_task(new_profile)
        
        # Recreate crew with updated components
        self.crew = Crew(
            agents=[self.curator_agent, summarizer_agent, relevance_scorer_agent],
            tasks=[self.curation_task, self.summarization_task, self.relevance_task],
            verbose=True
        )

# Legacy crew for backward compatibility with existing stock analysis
from agents.analyst_agent import analyst_agent
from agents.trader_agent import trader_agent
from tasks.analyse_task import get_stock_analysis
from tasks.trade_task import trade_decision

stock_crew = Crew(
    agents=[analyst_agent, trader_agent],
    tasks=[get_stock_analysis, trade_decision],
    verbose=True
)