import os
import requests
from dotenv import load_dotenv
load_dotenv()
primary_url=os.getenv("PRIMARY_API_URL")
response= requests.get(primary_url)
print("status: ",response.status_code)
jobs=response.json()
print("Total jobs: ",len(jobs))
for job in jobs[:5]:
    if not job.get("position"):
        continue
    print("Title:", job.get("position"))
    print("Company:", job.get("company"))
    print("Location:", job.get("location"))
    print("URL:", job.get("apply_url"))
    print("-" * 50)
