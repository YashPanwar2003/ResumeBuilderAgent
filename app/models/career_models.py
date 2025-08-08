from typing import List, Literal
from pydantic import BaseModel

class CareerGoal(BaseModel):
    targetRole: str
    targetIndustry: str
    timeframe: str
    currentLevel: Literal['entry', 'mid', 'senior', 'executive']
    targetLevel: Literal['entry', 'mid', 'senior', 'executive']

class CareerGuidanceRequest(BaseModel):
    age: int
    interests: List[str]
    careerGoal: CareerGoal
    skills: List[str]
    relatedFields: List[str]

class StudySource(BaseModel):
    name: str
    url: str
    description: str

class CareerRecommendation(BaseModel):
    jobName: str
    description: str
    averageSalary: str
    skillsToDevelop: List[str]
    sourcesToStudy: List[StudySource]
