from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from roadmap_generator.analyzer import analyze_resume_route  # import your route

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the route
app.include_router(analyze_resume_route)
