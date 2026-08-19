from app.storage import get_all_jobs


jobs = get_all_jobs()

print("Total jobs in database:", len(jobs))

for job in jobs:
    print(job)