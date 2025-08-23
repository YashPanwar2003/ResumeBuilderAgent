import json
import re
from fastapi import HTTPException
from typing import Union
from .gemini_client import model
from app.models.resume_models import ResumeData

def improve_resume_with_gemini(data: Union[ResumeData, dict]) -> ResumeData:
    resume_json_str = data.model_dump_json(indent=2) if isinstance(data, ResumeData) else json.dumps(data, indent=2)

    prompt = f"""
    You are a professional resume writer.
    The user will provide resume data in JSON format.
    - input Format would be like : {ResumeData}
      -output Format would be Like : {ResumeData}
    Your job:
    - Improve ONLY:
        - personalInfo.summary
        - experience[].description
        - skills[].name
    - Do NOT change:
        - Dates, numbers, boolean values, levels, or structure
    - Return the result in EXACTLY the same JSON format as received.
    - Keep the same keys, types, and nested array structure.
    - keep the format stricly as provided in output format.
    - Ensure the output is valid JSON.
    Here is the resume data to improve:
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
        raise HTTPException(status_code=500, detail=f"Failed to parse Gemini output: {e}")
