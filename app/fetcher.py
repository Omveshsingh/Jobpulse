import os
import requests
from dotenv import load_dotenv

load_dotenv()

PRIMARY_API_URL = os.getenv("PRIMARY_API_URL")
FALLBACK_API_URL=os.getenv("FALLBACK_API_URL")
def fetch_jobs_from_api(url, source_name):
    try:
        response = requests.get(url,timeout=10)
        print(f"{source_name} status:", response.status_code)
        if response.status_code== 429: 
             print("Primary Api is rate limited.")
             return None
        if response.status_code==403:
            print("Primary api denied request")
            return None
        response.raise_for_status()
        jobs=response.json()
        if not jobs:
            print("Primary api returned empty data")
            return None
        return jobs
    except requests.Timeout :
        print("Primary api timed out")
        return None
    except requests.RequestException as error:
        print("Primary Api Failed: ",error)
        return None
def fetch_primary_jobs():
    return fetch_jobs_from_api(PRIMARY_API_URL,"RemoteOK")
def fetch_fallback_jobs():
    return fetch_jobs_from_api(FALLBACK_API_URL,"Arbeitnow")

def fetch_jobs():
    jobs=fetch_primary_jobs()
    if jobs is not None:
        print("Using primary source")
        return jobs
    print("Primary source unavailable. Trying fallback")
    jobs=fetch_fallback_jobs()
    if jobs is not None:
        print("Using Fallback source")
        return jobs
    print("Both api Failed")
    return None
if __name__=="__main__":
    jobs=fetch_jobs()
    if jobs:
        print("Total jobs: ",len(jobs))
    else:
        print("no jobs received")