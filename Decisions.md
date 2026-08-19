# JobPulse — Engineering Decisions

## 1. Ingestion Strategy

I chose a public job-board API approach instead of directly scraping platforms such as
LinkedIn, Indeed, or Naukri.

The obvious alternative was browser-based scraping with a headless browser, session
management, request rotation, and increasingly complex anti-bot handling. I rejected
that approach for this challenge because the assessment explicitly provides a
low-risk public API/RSS or sandbox path. A public API also gives a more reliable and
repeatable demonstration without attempting to bypass a platform's anti-bot or
access controls.

JobPulse uses RemoteOK as the primary source and Arbeitnow as a fallback. The
fetcher uses a 10-second timeout and handles rate limiting (429), denied requests
(403), request failures, timeouts, and empty responses. If the primary source fails,
the fallback source is attempted.

The ingestion pipeline is:

    API
      ↓
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
    SQLite

This design means a temporary failure of one source does not immediately stop the
pipeline.

I deliberately stop at public, permitted sources rather than attempting to bypass
CAPTCHAs, fingerprinting, authentication barriers, or other anti-bot controls on
platforms that prohibit automated access.

---

## 2. Trade-off Under the Time Limit

The main trade-off was using SQLite and client-side filtering instead of building
a production-scale database and server-side search system.

SQLite made the project faster to develop and easier to run locally, while the
current dataset is small enough for the frontend to search and filter efficiently.

With a full week, I would migrate storage to PostgreSQL, add server-side
pagination and search, schedule ingestion, add monitoring, and make database
persistence explicit for the deployment environment.

I would also improve source adapters so that changes to an individual API's schema
can be isolated without affecting the rest of the pipeline.

---

## 3. Resilience and Data Quality

The pipeline does not assume that external data is clean or permanent.

Different sources are converted into a common internal schema before processing.
HTML descriptions are cleaned, required fields are validated, and jobs are
deduplicated using `(source, id)`.

The database also enforces the same uniqueness rule through a database constraint,
providing a second layer of protection against duplicates.

If a source returns an empty response, times out, is rate-limited, or rejects a
request, the fetcher attempts the fallback source rather than silently treating
the failure as successful ingestion.

---

## 4. AI Usage and Verification

AI tools were used during development for debugging, implementation guidance,
architecture discussion, and reviewing deployment issues.

I personally verified the generated suggestions by running the individual
components and the complete pipeline locally. This included testing validation,
cleaning, deduplication, storage, API fetching, FastAPI responses, and the
deployed frontend/backend connection.

I also corrected implementation details when the suggested code did not match the
actual project interfaces. For example, the normalizer uses separate
`normalize_remoteok_job()` and `normalize_arbeitnow_job()` functions rather than
a generic `normalize_jobs()` function.

The final implementation was therefore tested against the actual codebase rather
than being submitted without verification.