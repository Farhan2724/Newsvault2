from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(title="NewsVault API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ProfileCreationRequest(BaseModel):
    user_id: str
    responses: Dict[str, Any]

class NewsRequest(BaseModel):
    user_id: str
    limit: Optional[int] = 10

class QuestionnaireResponse(BaseModel):
    frequency: str
    industries: List[str]
    horizon: str
    period: str
    risk: str
    experience: str

# Basic routes
@app.get("/")
async def root():
    return {"message": "NewsVault API is running!", "status": "success"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/news")
async def get_news(query: str = "technology"):
    """
    Get news based on query - minimal implementation
    """
    try:
        return {
            "status": "success",
            "query": query,
            "data": [
                {
                    "title": f"Sample news about {query}",
                    "description": "This is a sample news article",
                    "url": "https://example.com"
                }
            ],
            "message": "API is working!"
        }
    except Exception as e:
        logger.error(f"Error in get_news: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/api/profile")
async def create_profile(request: ProfileCreationRequest):
    """
    Create user profile from questionnaire responses
    """
    try:
        # For now, return a mock response
        # You can implement the actual profile creation logic here
        return {
            "status": "success",
            "message": "Profile created successfully",
            "user_id": request.user_id,
            "profile": request.responses
        }
    except Exception as e:
        logger.error(f"Error in create_profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/questionnaire")
async def get_questionnaire():
    """
    Get questionnaire questions
    """
    try:
        # Return the questionnaire structure
        questions = [
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
        
        return {
            "status": "success",
            "questions": questions
        }
    except Exception as e:
        logger.error(f"Error in get_questionnaire: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Stock analysis endpoint (basic version without complex imports)
@app.get("/api/stock/{symbol}")
async def get_stock_analysis(symbol: str):
    """
    Get basic stock information
    """
    try:
        # Import yfinance only when needed
        import yfinance as yf
        
        stock = yf.Ticker(symbol)
        info = stock.info
        
        current_price = info.get("regularMarketPrice") or info.get("currentPrice")
        change = info.get("regularMarketChange")
        change_percent = info.get("regularMarketChangePercent")
        currency = info.get("currency", "USD")
        
        if current_price is None:
            raise HTTPException(status_code=404, detail=f"Stock symbol {symbol} not found")
        
        return {
            "status": "success",
            "symbol": symbol.upper(),
            "data": {
                "price": current_price,
                "change": change,
                "change_percent": round(change_percent, 2) if change_percent else None,
                "currency": currency
            }
        }
    except Exception as e:
        logger.error(f"Error in get_stock_analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching stock data: {str(e)}")

# This is important for Vercel
handler = app
