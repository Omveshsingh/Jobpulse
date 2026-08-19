def deduplicate_jobs(jobs):
    unique_jobs = []
    seen = set()
    for job in jobs:
        key = f"{job.get('source')}:{job.get('id')}"
        if key in seen:
            continue

        seen.add(key)
        unique_jobs.append(job)
    return unique_jobs