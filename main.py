from fastapi import FastAPI

app = FastAPI(title="NewsVault API", version="1.0.0")

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

# This is important for Vercel
handler = app
