from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .storage import get_all_jobs
app = FastAPI(title="JobPulse API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {
        "message": "JobPulse API is running"
    }

@app.get("/api/jobs")
def get_jobs():
    rows = get_all_jobs()
    jobs = []
    for row in rows:
        job = {
            "id": row[0],
            "source": row[1],
            "title": row[2],
            "company": row[3],
            "location": row[4],
            "url": row[5],
            "remote": bool(row[6])
        }
        jobs.append(job)
    return {
        "total": len(jobs),
        "jobs": jobs
    }