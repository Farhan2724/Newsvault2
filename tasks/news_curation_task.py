# tasks/news_curation_task.py
from crewai import Task
from agents.news_curator_agent import create_news_curator_agent, relevance_scorer_agent
from user_profile import UserProfile

def create_news_curation_task(user_profile: UserProfile) -> Task:
    """Create a personalized news curation task based on user profile"""
    
    # Build sector keywords from user preferences
    sector_keywords = " OR ".join(user_profile.industry_preferences)
    
    # Adjust task description based on investment frequency
    frequency_context = {
        "daily": "today's market movements and breaking news",
        "weekly": "this week's significant market developments",
        "monthly": "major market trends and developments this month",
        "quarterly": "significant quarterly developments and earnings",
        "yearly": "major annual trends and long-term market shifts"
    }
    
    time_context = frequency_context.get(
        user_profile.investment_frequency.value, 
        "recent market developments"
    )
    
    curator_agent = create_news_curator_agent(user_profile)
    
    return Task(
        description=(
            f"Fetch and curate financial news articles focusing on {sector_keywords} sectors. "
            f"Prioritize {time_context} that align with {user_profile.investment_horizon.value} "
            f"investment strategy and {user_profile.risk_appetite.value} risk tolerance. "
            f"Consider the user's {user_profile.experience_level.value} experience level when "
            f"selecting and presenting information. Find 8-12 relevant articles."
        ),
        expected_output=(
            "A curated list of 8-12 financial news articles with:\n"
            "- Article title and source\n"
            "- Brief description\n"
            "- Relevance score (1-10)\n"
            "- Key tags (sector, risk level, time relevance)"
        ),
        agent=curator_agent
    )

# tasks/news_summarization_task.py
from agents.news_curator_agent import summarizer_agent

def create_summarization_task(user_profile: UserProfile) -> Task:
    """Create a news summarization task tailored to user profile"""
    
    # Adjust summary style based on experience level
    if user_profile.experience_level.value == "beginner":
        summary_style = (
            "Use simple language, explain technical terms, and provide context "
            "for market concepts. Focus on what this means for a new investor."
        )
    elif user_profile.experience_level.value == "expert":
        summary_style = (
            "Use precise financial terminology, focus on technical analysis, "
            "market implications, and advanced insights. Assume deep market knowledge."
        )
    else:
        summary_style = (
            "Balance technical accuracy with accessibility, explain key terms "
            "when necessary, and focus on actionable insights."
        )
    
    return Task(
        description=(
            f"Transform the curated news articles into 60-80 word summaries. "
            f"{summary_style} "
            f"Highlight information most relevant to {user_profile.investment_horizon.value} "
            f"investors with {user_profile.risk_appetite.value} risk tolerance. "
            f"Ensure each summary is standalone and actionable."
        ),
        expected_output=(
            "For each article, provide:\n"
            "- 60-80 word summary\n"
            "- Key takeaway for the user's investment profile\n"
            "- Action items (if any)\n"
            "- Risk/opportunity indicators"
        ),
        agent=summarizer_agent
    )

# tasks/relevance_scoring_task.py
def create_relevance_scoring_task(user_profile: UserProfile) -> Task:
    """Create a task to score article relevance based on user profile"""
    
    return Task(
        description=(
            f"Score the relevance of each news article based on the user's profile:\n"
            f"- Industries: {', '.join(user_profile.industry_preferences)}\n"
            f"- Investment horizon: {user_profile.investment_horizon.value}\n"
            f"- Risk appetite: {user_profile.risk_appetite.value}\n"
            f"- Experience level: {user_profile.experience_level.value}\n"
            f"- Investment frequency: {user_profile.investment_frequency.value}\n"
            f"Prioritize articles that best match these criteria."
        ),
        expected_output=(
            "A ranked list of articles with:\n"
            "- Relevance score (1-10)\n"
            "- Relevance reasoning\n"
            "- Priority level (High/Medium/Low)\n"
            "- Recommended action for this user type"
        ),
        agent=relevance_scorer_agent
    )