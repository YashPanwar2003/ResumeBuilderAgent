import json
import re
from fastapi import HTTPException
from typing import Union
from .gemini_client import model
from app.models.resume_models import ResumeData


def improve_resume_with_gemini(data: Union[ResumeData, dict]) -> ResumeData:
    resume_json_str = (
        data.model_dump_json(indent=2)
        if isinstance(data, ResumeData)
        else json.dumps(data, indent=2)
    )

    prompt = f"""
    You are a professional resume writer.

    The user will provide resume data in JSON format.

    Your task:
    - Input will be JSON in the following schema: {ResumeData}
    - Output must also be JSON in the exact same schema: {ResumeData}

    Rules:
    1. Improve ONLY:
       - personalInfo.summary
       - experience[].description
       - skills[].name
    2. Do NOT change:
       - Dates
       - Numbers
       - Boolean values
       - Levels
       - JSON structure
    3. Keep all keys, types, and nested arrays exactly the same.
    4. Always return **only valid JSON** — no explanations, no markdown, no text outside the JSON.
    5. The root of the response must be a JSON object (matching ResumeData).

    Here is the resume data to improve:

    {resume_json_str}
    """

    response = model.generate_content(prompt)
    if not response or not response.text:
        raise HTTPException(status_code=500, detail="Gemini API returned no content.")

    raw_output = response.text.strip()
    match = re.search(r"\{.*\}", raw_output, re.DOTALL)
    if match:
        raw_output = match.group(0)

    try:
        return ResumeData(**json.loads(raw_output))
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse Gemini output: {e}"
        )
