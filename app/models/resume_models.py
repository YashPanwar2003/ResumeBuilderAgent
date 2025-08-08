from typing import List, Literal, Optional
from pydantic import BaseModel

class PersonalInfo(BaseModel):
    fullName: str
    email: str
    phone: str
    location: str
    website: str
    linkedin: str
    summary: str

class Experience(BaseModel):
    id: str
    company: str
    position: str
    location: str
    startDate: str
    endDate: str
    current: bool
    description: str

class Education(BaseModel):
    id: str
    institution: str
    degree: str
    field: str
    startDate: str
    endDate: str
    gpa: Optional[str] = None

class Skill(BaseModel):
    name: str
    level: Literal['beginner', 'intermediate', 'advanced', 'expert']

class ResumeData(BaseModel):
    personalInfo: PersonalInfo
    experience: List[Experience]
    education: List[Education]
    skills: List[Skill]
