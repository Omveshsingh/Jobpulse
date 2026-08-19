from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .storage import create_database, get_all_jobs, save_jobs
from .fetcher import fetch_jobs
from .normalizer import (
    normalize_remoteok_job,
    normalize_arbeitnow_job
)
from .cleaner import clean_job
from .validator import validate_job
from .deduplicator import deduplicate_jobs


app = FastAPI(title="JobPulse API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():

    create_database()

    existing_jobs = get_all_jobs()

    if existing_jobs:
        print(f"Database already contains {len(existing_jobs)} jobs")
        return

    print("Database is empty. Fetching jobs...")

    raw_data = fetch_jobs()

    if not raw_data:
        print("No jobs received from APIs")
        return

    # RemoteOK returns a list directly
    if isinstance(raw_data, list):

        jobs = [
            normalize_remoteok_job(job)
            for job in raw_data
            if isinstance(job, dict)
        ]

    # Arbeitnow returns {"data": [...]}
    elif isinstance(raw_data, dict) and "data" in raw_data:

        jobs = [
            normalize_arbeitnow_job(job)
            for job in raw_data.get("data", [])
            if isinstance(job, dict)
        ]

    else:
        print("Unknown API response format")
        return

    print(f"Normalized jobs: {len(jobs)}")

    # Clean
    jobs = [
        clean_job(job)
        for job in jobs
    ]

    print(f"Cleaned jobs: {len(jobs)}")

    # Validate
    jobs = [
        job
        for job in jobs
        if validate_job(job)
    ]

    print(f"Valid jobs: {len(jobs)}")

    # Deduplicate
    jobs = deduplicate_jobs(jobs)

    print(f"Unique jobs: {len(jobs)}")

    # Store
    save_jobs(jobs)

    print(f"Saved {len(jobs)} jobs to database")


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