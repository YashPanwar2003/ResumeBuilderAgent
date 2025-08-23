from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import resume_routes, career_routes

app = FastAPI(title="AI Resume & Career Guidance API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(resume_routes.router)
app.include_router(career_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to AI Resume & Career Guidance API"}
