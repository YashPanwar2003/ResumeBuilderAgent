from fastapi import APIRouter
from app.models.resume_models import ResumeData
from app.services.resume_services import improve_resume_with_gemini

router = APIRouter()

@router.post("/improve_resume", response_model=ResumeData)
def improve_resume(data: ResumeData):
    return improve_resume_with_gemini(data)
