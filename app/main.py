from fastapi import FastAPI
from app.routes import resume_routes, career_routes

app = FastAPI(title="AI Resume & Career Guidance API")

app.include_router(resume_routes.router)
app.include_router(career_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to AI Resume & Career Guidance API"}
