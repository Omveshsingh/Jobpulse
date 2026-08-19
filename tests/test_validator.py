from app.validator import validate_job


valid_job = {
    "id": "123",
    "title": "Software Engineer",
    "company": "Example Company",
    "url": "https://example.com/job/123"
}


invalid_job = {
    "id": "456",
    "title": "",
    "company": "Example Company",
    "url": "https://example.com/job/456"
}


print("Valid job:", validate_job(valid_job))
print("Invalid job:", validate_job(invalid_job))