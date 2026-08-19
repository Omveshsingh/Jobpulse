from app.cleaner import clean_job


job = {
    "id": "123",
    "title": "<strong>Software Engineer</strong>",
    "company": "Example Company",
    "location": "  Delhi   ",
    "url": "[https://example.com/job/123](https://example.com/job/123)",
    "description": "<p>Build APIs</p><br><strong>Work with Python</strong>",
    "tags": ["python"],
    "remote": True,
    "source": "test"
}


cleaned = clean_job(job)

print(cleaned)