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

{CareerGuidanceRequest}

Your response must always be a valid JSON array of CareerRecommendation objects, like this:

[
  {
    "jobName": "...",
    "description": "...",
    "averageSalary": "...",
    "skillsToDevelop": ["...", "..."],
    "sourcesToStudy": [
      {
        "name": "...",
        "url": "...",
        "description": "..."
      }
    ]
  }
]

Rules for your response:

1. Always return a valid JSON array at the root. Do not include any text before or after the array.
2. Tailor all suggestions to the Indian job market.
3. Use the user's `age`, `interests`, `skills`, `relatedFields`, and `careerGoal` to create realistic recommendations.
4. Provide actionable steps (certifications, skills, networking tips).
5. Avoid generic advice — match to `currentLevel` and `targetLevel`.
6. If input is invalid, return an array with a single error object:

[
  { "error": "Invalid input: <explanation>" }
]
"""


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
