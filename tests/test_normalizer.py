import os
import requests
from dotenv import load_dotenv

from app.normalizer import (
    normalize_remoteok_job,
    normalize_arbeitnow_job
)

load_dotenv()

# ---------- RemoteOK ----------

primary_url = os.getenv("PRIMARY_API_URL")

response = requests.get(primary_url)

remoteok_jobs = response.json()

for job in remoteok_jobs:
    if not job.get("position"):
        continue

    normalized = normalize_remoteok_job(job)

    print("REMOTEOK")
    print(normalized)
    print("-" * 50)

    break


# ---------- Arbeitnow ----------

fallback_url = os.getenv("FALLBACK_API_URL")

response = requests.get(fallback_url)

arbeitnow_data = response.json()

arbeitnow_jobs = arbeitnow_data.get("data", [])

for job in arbeitnow_jobs:
    normalized = normalize_arbeitnow_job(job)

    print("ARBEITNOW")
    print(normalized)
    print("-" * 50)

    break