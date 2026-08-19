from fetcher import fetch_primary_jobs, fetch_fallback_jobs
from normalizer import normalize_remoteok_job, normalize_arbeitnow_job
from validator import validate_job
from storage import create_database, save_jobs
from cleaner import clean_job
from deduplicator import deduplicate_jobs
def get_jobs():
    primary_jobs = fetch_primary_jobs()
    if primary_jobs is not None:
        normalized_jobs = []
        for job in primary_jobs:
            normalized_job = normalize_remoteok_job(job)
            cleaned_job = clean_job(normalized_job)
            if not validate_job(cleaned_job):
                continue
            normalized_jobs.append(cleaned_job)
        return deduplicate_jobs(normalized_jobs)
    
    fallback_data = fetch_fallback_jobs()

    if fallback_data is not None:
        normalized_jobs = []
        fallback_jobs = fallback_data.get("data", [])
        for job in fallback_jobs:
            normalized_job = normalize_arbeitnow_job(job)
            cleaned_job = clean_job(normalized_job)
            if not validate_job(cleaned_job):
                continue
            normalized_jobs.append(cleaned_job)
        return deduplicate_jobs(normalized_jobs)

if __name__ == "__main__":
    create_database()
    jobs = get_jobs()
    print("Jobs fetched:", len(jobs))
    save_jobs(jobs)
    print("Jobs saved to database.")