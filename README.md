# JobPulse

JobPulse is a full-stack job aggregation platform that collects job listings
from multiple public job APIs, processes and validates the data, removes
duplicates, stores the results in SQLite, and exposes them through a FastAPI
backend and React frontend.

---

## Features

- Fetch jobs from multiple public APIs
- Primary and fallback API strategy
- API timeout and error handling
- Job data normalization
- HTML description cleaning
- Job validation
- Duplicate detection
- SQLite persistence
- FastAPI REST API
- React + Vite frontend
- Job search
- Remote-only filtering
- Job source identification
- Direct job links
- Loading and error states
- Refresh functionality

---

## Architecture

```text
                 ┌─────────────────┐
                 │   RemoteOK API  │
                 └────────┬────────┘
                          │
                          ↓
                    ┌───────────┐
                    │  Fetcher  │
                    └─────┬─────┘
                          │
                    API unavailable?
                          │
                          ↓
                 ┌─────────────────┐
                 │ Arbeitnow API   │
                 └────────┬────────┘
                          │
                          ↓
                  ┌──────────────┐
                  │  Normalizer  │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │   Cleaner    │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │  Validator   │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │ Deduplicator │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │   Storage    │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │    SQLite    │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │   FastAPI    │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │ React + Vite │
                  └──────────────┘
```

---

## Tech Stack

### Backend

- Python
- Requests
- FastAPI
- SQLite
- python-dotenv
- Uvicorn

### Frontend

- React
- Vite
- JavaScript
- CSS
- Lucide React

---

## Project Structure

```text
jobpulse/
│
├── app/
│   ├── __init__.py
│   ├── api.py
│   ├── cleaner.py
│   ├── deduplicator.py
│   ├── fetcher.py
│   ├── normalizer.py
│   ├── pipeline.py
│   ├── storage.py
│   └── validator.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── tests/
│   ├── test_api.py
│   ├── test_cleaner.py
│   ├── test_deduplicator.py
│   ├── test_normalizer.py
│   ├── test_storage.py
│   └── test_validator.py
│
├── decisions.md
├── requirements.txt
├── .gitignore
├── .env
└── jobs.db
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
PRIMARY_API_URL=https://remoteok.com/api
FALLBACK_API_URL=https://www.arbeitnow.com/api/job-board-api
```

The `.env` file contains configuration and should **not** be committed to
GitHub.

---

## Backend Installation

From the project root:

```powershell
python -m pip install -r requirements.txt
```

---

## Run the Job Pipeline

The pipeline fetches jobs, processes them, removes duplicates, and stores
them in SQLite.

```powershell
python app/pipeline.py
```

Expected flow:

```text
Fetch
  ↓
Normalize
  ↓
Clean
  ↓
Validate
  ↓
Deduplicate
  ↓
Store
```

---

## Run the FastAPI Backend

From the project root:

```powershell
uvicorn app.api:app --reload
```

The backend runs at:

```text
http://127.0.0.1:8000
```

API endpoint:

```text
http://127.0.0.1:8000/api/jobs
```

---

## API Response

The `/api/jobs` endpoint returns normalized JSON objects.

Example:

```json
{
  "total": 275,
  "jobs": [
    {
      "id": "1136966",
      "source": "remoteok",
      "title": "Team Member Special Assignment",
      "company": "Reliance Industries Limited",
      "location": "Jamnagar",
      "url": "https://example.com/job",
      "remote": false
    }
  ]
}
```

Returning named JSON fields allows the frontend to use:

```javascript
job.title
job.company
job.location
job.url
job.remote
```

instead of depending on database column positions.

---

## Frontend Installation

Move into the frontend directory:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

The frontend normally runs at:

```text
http://localhost:5173
```

---

## Frontend Functionality

The JobPulse dashboard provides:

### Search

Search jobs by:

- title
- company
- location

### Remote Filter

Users can enable **Remote only** to display remote positions.

### Job Information

Each job card displays:

- Job title
- Company
- Location
- Source
- Remote/on-site status
- Link to the original job posting

### Refresh

The refresh button requests the latest data from the FastAPI backend.

### Application States

The frontend handles:

- Loading
- Successful results
- Empty search results
- API errors

---

## Data Processing

### 1. Fetching

RemoteOK is used as the primary source.

If the primary API fails, JobPulse attempts to use Arbeitnow.

The fetcher handles:

- HTTP 429 rate limiting
- HTTP 403 request denial
- Request timeout
- Other request exceptions
- Empty responses

External requests use a 10-second timeout.

---

### 2. Normalization

Different APIs return different structures.

The normalizer converts these different structures into a common JobPulse
schema.

The normalized job contains fields including:

```text
id
source
title
company
location
url
description
tags
remote
```

---

### 3. Cleaning

Job descriptions can contain HTML such as:

```html
<p>
<strong>
<li>
<br>
```

The cleaner removes unnecessary HTML markup so that descriptions can be
stored and displayed as readable text.

---

### 4. Validation

Jobs are validated before entering the storage layer.

This prevents incomplete or malformed records from being stored.

---

### 5. Deduplication

Jobs are deduplicated using:

```text
(source, id)
```

This is important because the same numeric ID could theoretically occur in
different data sources.

For example:

```text
remoteok + 123
arbeitnow + 123
```

are treated as different records.

---

### 6. Storage

Validated and deduplicated jobs are stored in SQLite.

SQLite was selected because the current project is lightweight and does not
require a separate database server during development.

---

## Testing

Individual components can be tested independently.

### Validator

```powershell
python test_validator.py
```

### Cleaner

```powershell
python test_cleaner.py
```

### Deduplicator

```powershell
python test_deduplicator.py
```

### Storage

```powershell
python test_storage.py
```

### Pipeline

```powershell
python app/pipeline.py
```

The tests verify individual pipeline components before the complete system
is executed.

---

## Error Handling

The system is designed to avoid complete pipeline failure when an external
API becomes unavailable.

The fallback sequence is:

```text
RemoteOK
   │
   ├── Success ──────────────→ Continue
   │
   └── Failure
          ↓
       Arbeitnow
          │
          ├── Success ───────→ Continue
          │
          └── Failure
                    ↓
              No jobs received
```

---

## Technical Decisions

Important architectural decisions are documented in:

```text
decisions.md
```

The decisions document explains the reasoning behind:

- API selection
- Primary/fallback architecture
- Timeout handling
- Normalization
- Cleaning
- Validation
- Deduplication
- SQLite
- FastAPI
- React/Vite
- CORS
- API response design
- Frontend filtering
- Deployment considerations

---

## Current Limitations

### SQLite

SQLite is suitable for the current project scale and local development.

For a larger production system, PostgreSQL or another managed database would
be more appropriate.

### Client-Side Search

The current frontend filters the jobs already loaded into the browser.

For a much larger dataset, server-side search and pagination would be more
appropriate.

### External API Dependency

Job availability depends on the external APIs used by the application.
Changes to their response formats or availability may require changes to the
normalization layer.

---

## Future Improvements

Potential future improvements include:

- PostgreSQL migration
- Scheduled job ingestion
- Pagination
- Advanced filtering
- Salary filtering
- Job category filtering
- User authentication
- Saved jobs
- Personalized job recommendations
- Job ranking
- Email notifications
- Monitoring
- Logging
- CI/CD automation
- Production observability

---

## Deployment

The intended deployment architecture separates the frontend and backend:

```text
React Frontend
      │
      ↓
   FastAPI
      │
      ↓
   SQLite
```

The frontend and backend should be deployed as separate services.

---