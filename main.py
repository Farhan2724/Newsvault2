from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="NewsVault API", version="1.0.0")

# Pydantic models for request/response
class NewsRequest(BaseModel):
    query: str
    max_results: int = 10

class NewsResponse(BaseModel):
    status: str
    data: list
    message: str = ""

@app.get("/")
async def root():
    return {"message": "NewsVault API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/news", response_model=NewsResponse)
async def get_news(request: NewsRequest):
    """
    Get news based on query
    """
    try:
        # Example using a simple news API call
        # You can replace this with your preferred news source
        
        # For now, returning a mock response
        mock_news = [
            {
                "title": f"Sample news about {request.query}",
                "description": "This is a sample news article",
                "url": "https://example.com",
                "published_at": "2025-01-01T00:00:00Z"
            }
        ]
        
        return NewsResponse(
            status="success",
            data=mock_news[:request.max_results],
            message=f"Found {len(mock_news)} articles"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add CORS if needed for frontend
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
