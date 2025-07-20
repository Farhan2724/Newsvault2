from pydantic import BaseModel
from typing import List, Dict, Any, Optional

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