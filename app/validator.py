REQUIRED_FIELDS = [
    "id",
    "title",
    "company",
    "url"
]

def validate_job(job):
    for field in REQUIRED_FIELDS:
        if not job.get(field):
            return False
        
    return True