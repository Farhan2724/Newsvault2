# agents/news_curator_agent.py
from crewai import Agent, LLM
from tools.news_research_tool import get_financial_news, get_sector_news, get_stock_specific_news
from user_profile import UserProfile, ExperienceLevel, RiskAppetite

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.3
)

def create_news_curator_agent(user_profile: UserProfile) -> Agent:
    """Create a personalized news curator agent based on user profile"""
    
    # Customize agent based on experience level
    if user_profile.experience_level == ExperienceLevel.BEGINNER:
        role = "Beginner-Friendly Financial News Curator"
        backstory = (
            "You are a patient financial educator who specializes in making complex financial news "
            "accessible to new investors. You explain technical terms, provide context, and focus on "
            "educational value while keeping summaries concise and understandable."
        )
    elif user_profile.experience_level == ExperienceLevel.EXPERT:
        role = "Expert Financial News Analyst"
        backstory = (
            "You are a seasoned financial analyst who provides sophisticated insights to expert investors. "
            "You focus on technical analysis, market implications, and advanced financial concepts, "
            "assuming deep knowledge of financial markets and investment strategies."
        )
    else:
        role = "Personalized Financial News Curator"
        backstory = (
            "You are an experienced financial journalist who tailors news summaries to match "
            "individual investor needs. You balance technical accuracy with accessibility, "
            "providing relevant insights based on investment goals and risk tolerance."
        )
    
    # Create goal based on user preferences
    goal = (
        f"Curate and summarize financial news that aligns with {user_profile.investment_horizon.value} "
        f"investment strategy, focusing on {', '.join(user_profile.industry_preferences)} sectors, "
        f"with {user_profile.risk_appetite.value} risk tolerance. Provide 60-80 word summaries that "
        f"are relevant to {user_profile.experience_level.value} level investors."
    )
    
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        llm=llm,
        tools=[get_financial_news, get_sector_news, get_stock_specific_news],
        verbose=True
    )

# agents/news_summarizer_agent.py
summarizer_agent = Agent(
    role="Financial News Summarizer",
    goal=(
        "Transform complex financial news articles into concise, actionable 60-80 word summaries "
        "that highlight key information relevant to individual investor profiles and goals."
    ),
    backstory=(
        "You are a skilled financial writer who excels at distilling complex market information "
        "into bite-sized, digestible summaries. You understand what different types of investors "
        "need to know and can adjust your communication style accordingly."
    ),
    llm=llm,
    tools=[],
    verbose=True
)

# agents/relevance_scorer_agent.py
relevance_scorer_agent = Agent(
    role="Investment Relevance Analyst",
    goal=(
        "Evaluate and score the relevance of financial news articles based on user investment "
        "profiles, preferences, and goals to ensure the most pertinent information is prioritized."
    ),
    backstory=(
        "You are a quantitative analyst who specializes in matching financial information to "
        "investor needs. You understand how different news impacts various investment strategies "
        "and can accurately assess relevance based on user profiles."
    ),
    llm=llm,
    tools=[],
    verbose=True
)