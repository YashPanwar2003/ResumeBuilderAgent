import json
import re
from fastapi import HTTPException
from typing import List
from .gemini_client import model
from app.models.career_models import CareerGuidanceRequest, CareerRecommendation

def get_career_guidance_with_gemini(data: CareerGuidanceRequest) -> List[CareerRecommendation]:
    prompt = """
You are an expert Indian career guidance associate with deep knowledge of industries, roles, skill requirements, and educational pathways in India. Your job is to provide precise and actionable career guidance to individuals based on their profile and goals. 

You will receive input strictly in the following JSON-like format:

{CareerGudianceRequest}

Your response **must always be strictly in JSON format**, containing the following structure:

{
  CareerRecommendation[]          
}

Rules for your response:

1. Always follow the exact JSON structure above. Do **not** include any text outside the JSON object.
2. Suggest options and guidance specific to **India** and its job market.
3. Base recommendations on the user’s `age`, `interests`, `skills`, `relatedFields`, and `careerGoal`.
4. Provide realistic and actionable steps, including certifications, skills, or networking tips.
5. Avoid generic advice; tailor suggestions based on the `currentLevel` and `targetLevel`.
6. If any field in the input is missing or invalid, respond with an **error object** in JSON format:

{{
  "error": "Invalid input: <explanation>"
}}

Always ensure your JSON is valid and parseable.
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
