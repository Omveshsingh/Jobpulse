def normalize_remoteok_job(job):
    return {
        "id": job.get("id"),
        "title": job.get("position"),
        "company": job.get("company"),
        "location": job.get("location"),
        "url": job.get("apply_url"),
        "description": job.get("description"),
        "tags": job.get("tags", []),
        "remote": job.get("location", "").lower() in ["remote", "worldwide"],
        "source": "remoteok"
    }
def normalize_arbeitnow_job(job):
    return {
        "id": str(job.get("slug")),
        "title": job.get("title"),
        "company": job.get("company_name"),
        "location": job.get("location"),
        "url": job.get("url"),
        "description": job.get("description"),
        "tags": job.get("tags", []),
        "remote": job.get("remote", False),
        "source": "arbeitnow"
    }