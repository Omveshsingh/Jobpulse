from app.deduplicator import deduplicate_jobs


jobs = [
    {
        "id": "123",
        "source": "remoteok",
        "title": "Software Engineer"
    },
    {
        "id": "123",
        "source": "remoteok",
        "title": "Software Engineer"
    },
    {
        "id": "456",
        "source": "arbeitnow",
        "title": "Data Engineer"
    },
    {
        "id": "123",
        "source": "arbeitnow",
        "title": "Backend Engineer"
    }
]


unique_jobs = deduplicate_jobs(jobs)

print("Original jobs:", len(jobs))
print("Unique jobs:", len(unique_jobs))

for job in unique_jobs:
    print(job)