from app.storage import create_database, save_jobs


test_jobs = [
    {
        "id": "123",
        "source": "remoteok",
        "title": "Software Engineer",
        "company": "Test Company",
        "location": "Remote",
        "url": "https://example.com/job/123",
        "description": "Build software",
        "tags": ["python", "backend"],
        "remote": True
    },
    {
        "id": "456",
        "source": "arbeitnow",
        "title": "Data Engineer",
        "company": "Data Company",
        "location": "Berlin",
        "url": "https://example.com/job/456",
        "description": "Work with data",
        "tags": ["sql", "python"],
        "remote": False
    }
]


create_database()
save_jobs(test_jobs)

print("Jobs saved successfully.")