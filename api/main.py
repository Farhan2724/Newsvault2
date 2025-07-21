from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
import uvicorn

# Import your existing modules
from user_profile import UserProfile, UserProfileManager
from questionnaire import InvestmentQuestionnaire
from crew import NewsAICrew
from api.models import *

load_dotenv()

app = FastAPI(title="AI Finance News Curator")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize managers
profile_manager = UserProfileManager()
questionnaire = InvestmentQuestionnaire()

@app.get("/")
async def root():
    return {"message": "AI Finance News Curator API"}

@app.get("/questionnaire")
async def get_questionnaire():
    return {"questions": questionnaire.get_all_questions()}

@app.post("/profile")
async def create_profile(profile_data: ProfileCreationRequest):
    try:
        profile = questionnaire.create_profile_from_responses(
            profile_data.user_id,
            profile_data.responses
        )
        return {"success": True, "profile": profile.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/profile/{user_id}")
async def get_profile(user_id: str):
    profile = profile_manager.get_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile.to_dict()

@app.post("/news/{user_id}")
async def get_personalized_news(user_id: str):
    profile = profile_manager.get_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")
