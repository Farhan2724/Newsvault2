from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/test")
def test_endpoint():
    return {
        "status": "success",
        "message": "Test endpoint working",
        "data": ["item1", "item2", "item3"]
    }

# Handler for Vercel
handler = app
