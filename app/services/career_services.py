import json
import re
from fastapi import HTTPException
from typing import List
from .gemini_client import model
from app.models.career_models import CareerGuidanceRequest, CareerRecommendation

def get_career_guidance_with_gemini(data: CareerGuidanceRequest) -> List[CareerRecommendation]:
    prompt = """
You are an expert Indian career counselor...
    """  # Keep the same prompt as before

    response = model.generate_content(prompt)
    if not response or not response.text:
        raise HTTPException(status_code=500, detail="Gemini API returned no content.")

    raw_output = response.text.strip()
    match = re.search(r"\[.*\]", raw_output, re.DOTALL)
    if match:
        raw_output = match.group(0)

    try:
        parsed = json.loads(raw_output)
        return [CareerRecommendation(**item) for item in parsed]
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse Gemini output: {e}")
