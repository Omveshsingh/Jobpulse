import re
from bs4 import BeautifulSoup

def clean_html(text):
    if not text:
        return ""
    soup=BeautifulSoup(text,"html.parser")
    return soup.get_text(" ",strip=True)

def clean_whitespace(text):
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def clean_url(url):
    if not url:
        return ""
    url = url.strip()
    if url.startswith("[") and "](" in url:
        url = url[url.find("(") + 1:url.rfind(")")]
    return url

def clean_job(job):
    cleaned_job = job.copy()
    cleaned_job["title"] = clean_encoding(
        clean_whitespace(
            clean_html(cleaned_job.get("title", ""))
        )
    )
    cleaned_job["company"] = clean_encoding(
        clean_whitespace(
            clean_html(cleaned_job.get("company", ""))
        )
    )
    cleaned_job["location"] = clean_encoding(
        clean_whitespace(
            clean_html(cleaned_job.get("location", ""))
        )
    )
    cleaned_job["description"] = clean_encoding(
        clean_whitespace(
            clean_html(cleaned_job.get("description", ""))
        )
    )
    cleaned_job["url"] = clean_url(
        cleaned_job.get("url", "")
    )
    return cleaned_job

def clean_encoding(text):
    if not text:
        return ""
    
    try:
        return text.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text