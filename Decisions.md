# JobPulse — Technical Decisions

## 1. Project Overview

JobPulse is a job aggregation system that collects job listings from multiple
public APIs, processes and validates them, removes duplicates, stores them in
SQLite, and exposes the processed data through a FastAPI backend to a React
frontend.

The overall architecture is:

External Job APIs
        ↓
     Fetcher
        ↓
    Normalizer
        ↓
     Cleaner
        ↓
    Validator
        ↓
   Deduplicator
        ↓
     Storage
        ↓
     SQLite
        ↓
     FastAPI
        ↓
     React Frontend


## 2. Primary and Fallback APIs

### Decision

RemoteOK is used as the primary job source and Arbeitnow is used as the
fallback source.

### Why

Using two independent sources makes the ingestion pipeline more resilient.

If the primary API becomes unavailable, rate-limited, rejects the request,
times out, or returns unusable data, JobPulse attempts to retrieve jobs from
the fallback API.

This prevents a temporary failure of one external service from stopping the
entire ingestion process.


## 3. API Failure Handling

### Decision

The fetcher handles common API failure conditions explicitly.

These include:

- HTTP 429 — rate limiting
- HTTP 403 — request denied
- Request timeout
- Other HTTP/request exceptions
- Empty API responses

### Why

External APIs cannot be assumed to always be available.

The application therefore fails gracefully instead of crashing and allows the
fallback source to be attempted.


## 4. Request Timeout

### Decision

External API requests use a 10-second timeout.

### Why

The application should not wait indefinitely for an external service.

A fixed timeout allows the system to detect an unresponsive API and continue
with the fallback strategy.


## 5. Data Normalization

### Decision

Jobs from different APIs are converted into a common internal job schema.

### Why

RemoteOK and Arbeitnow do not return identical data structures.

Without normalization, every later stage of the pipeline would need separate
logic for each API.

The normalized job contains fields such as:

- id
- source
- title
- company
- location
- url
- description
- tags
- remote


## 6. HTML Cleaning

### Decision

HTML markup is removed from job descriptions before storing processed data.

### Why

Job descriptions from external APIs can contain HTML elements such as:

- `<p>`
- `<br>`
- `<li>`
- `<strong>`

Cleaning the descriptions makes the stored data easier to display, search,
and process later.


## 7. Validation

### Decision

Jobs are validated before they are stored.

### Why

External APIs can return incomplete or malformed records.

Validation prevents invalid jobs from entering the database and ensures that
later pipeline stages receive records that satisfy the expected schema.


## 8. Deduplication

### Decision

Jobs are deduplicated using the combination of `source` and `id`.

### Why

A job ID may only be unique within a particular source.

For example:

    remoteok + 123
    arbeitnow + 123

may represent two completely different jobs.

Therefore the uniqueness key is:

    (source, id)


## 9. SQLite Storage

### Decision

SQLite is used for persistent local storage.

### Why

The current project is a lightweight job aggregation application and does not
require a separate database server during development.

SQLite provides:

- persistent storage
- SQL support
- simple configuration
- no external database service
- easy local development


## 10. Database-Level Uniqueness

### Decision

The database enforces uniqueness using the combination of `source` and `id`.

### Why

Application-level deduplication alone is not enough.

A database-level uniqueness constraint provides an additional layer of
protection against duplicate records being inserted.


## 11. FastAPI Backend

### Decision

FastAPI is used as the backend API layer.

### Why

FastAPI provides a clean interface between the Python processing pipeline,
SQLite database, and React frontend.

The frontend does not communicate directly with SQLite.

Instead:

    React
      ↓
    FastAPI
      ↓
    Storage
      ↓
    SQLite

This separation keeps the frontend independent of the database implementation.


## 12. API Response Format

### Decision

The FastAPI `/api/jobs` endpoint converts database rows into JSON objects.

### Why

SQLite returns rows that can behave like tuples.

Returning those raw rows would force the frontend to use positional access
such as:

    job[2]
    job[3]
    job[4]

Instead, the API returns meaningful fields:

    job.title
    job.company
    job.location
    job.url
    job.remote

This creates a cleaner and more maintainable API contract between the backend
and frontend.


## 13. React and Vite

### Decision

React with Vite is used for the frontend.

### Why

React provides component-based UI development, while Vite provides a fast
development server and build system.

This combination is appropriate for building the JobPulse dashboard.


## 14. CORS

### Decision

FastAPI is configured to allow requests from the React frontend.

### Why

During local development, the frontend and backend run on different origins.

Frontend:

    http://localhost:5173

Backend:

    http://127.0.0.1:8000

CORS allows the browser to permit communication between these origins.


## 15. Client-Side Search

### Decision

The frontend performs search filtering on the jobs already loaded from the
API.

### Why

The current dataset is small enough for client-side filtering.

This provides immediate search results without making an API request for
every character typed by the user.

Search currently checks:

- job title
- company
- location


## 16. Remote Job Filtering

### Decision

The frontend provides a remote-only filter.

### Why

Remote availability is an important property of job listings and gives users
a simple way to narrow the available opportunities.


## 17. Loading and Error States

### Decision

The frontend provides loading, error, and empty-result states.

### Why

A usable application should clearly communicate whether:

- jobs are being loaded
- the API failed
- no jobs match the current search


## 18. Separation of Responsibilities

### Decision

JobPulse separates data ingestion, processing, storage, API access, and
frontend presentation.

### Why

Each layer has a specific responsibility.

    Fetcher
    ↓
    Retrieves external data

    Normalizer
    ↓
    Converts different API formats

    Cleaner
    ↓
    Cleans job descriptions

    Validator
    ↓
    Rejects invalid jobs

    Deduplicator
    ↓
    Removes duplicate jobs

    Storage
    ↓
    Saves jobs in SQLite

    FastAPI
    ↓
    Provides jobs to the frontend

    React
    ↓
    Displays and filters jobs

This makes the system easier to test, maintain, debug, and extend.


## 19. Deployment Considerations

### Decision

The application will be deployed with the frontend and backend as separate
services.

### Why

The React frontend and FastAPI backend have different runtime requirements.

Keeping them separate allows each layer to be deployed and scaled
independently.

The SQLite deployment will require persistent storage because a temporary
deployment filesystem should not be relied upon for permanent database data.


