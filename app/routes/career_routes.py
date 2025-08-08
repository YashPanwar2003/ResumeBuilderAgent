from fastapi import APIRouter
from typing import List
from app.models.career_models import CareerGuidanceRequest, CareerRecommendation
from app.services.career_services import get_career_guidance_with_gemini

router = APIRouter()

@router.post("/career_guidance", response_model=List[CareerRecommendation])
def career_guidance(data: CareerGuidanceRequest):
    return get_career_guidance_with_gemini(data)
