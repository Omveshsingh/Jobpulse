import { useEffect, useState } from "react";
import {
  Search,
  MapPin,
  Building2,
  ExternalLink,
  RefreshCw,
  BriefcaseBusiness,
} from "lucide-react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000/api/jobs";

function App() {
  const [jobs, setJobs] = useState([]);
  const [search, setSearch] = useState("");
  const [remoteOnly, setRemoteOnly] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function fetchJobs() {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(API_URL);

      if (!response.ok) {
        throw new Error("Failed to fetch jobs");
      }

      const data = await response.json();
      console.log("API DATA:", data);
      console.log("FIRST JOB:", data.jobs[0]);
      setJobs(data.jobs);
      
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchJobs();
  }, []);

  const filteredJobs = jobs.filter((job) => {
  const searchText = search.toLowerCase();

  const matchesSearch =
    job.title?.toLowerCase().includes(searchText) ||
    job.company?.toLowerCase().includes(searchText) ||
    job.location?.toLowerCase().includes(searchText);

  const matchesRemote = remoteOnly ? job.remote === true : true;

  return matchesSearch && matchesRemote;
});

  return (
    <div className="app">
      <header className="navbar">
        <div className="brand">
          <div className="brand-icon">
            <BriefcaseBusiness size={20} />
          </div>

          <div>
            <h1>JobPulse</h1>
            <span>Job intelligence dashboard</span>
          </div>
        </div>

        <button className="refresh-button" onClick={fetchJobs}>
          <RefreshCw size={17} />
          Refresh
        </button>
      </header>

      <main className="container">
        <section className="hero">
          <div>
            <p className="eyebrow">LIVE JOB INGESTION</p>

            <h2>
              Find your next
              <span> opportunity.</span>
            </h2>

            <p className="hero-text">
              Browse job listings collected from multiple public sources,
              cleaned, validated, and deduplicated by JobPulse.
            </p>
          </div>
        </section>

        <section className="controls">
          <div className="search-box">
            <Search size={19} />

            <input
              type="text"
              placeholder="Search jobs, companies, or locations..."
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
          </div>

          <button
            className={`filter-button ${remoteOnly ? "active" : ""}`}
            onClick={() => setRemoteOnly(!remoteOnly)}
          >
            Remote only
          </button>
        </section>

        <section className="stats">
          <div className="stat-card">
            <span>Total Jobs</span>
            <strong>{jobs.length}</strong>
          </div>

          <div className="stat-card">
            <span>Showing</span>
            <strong>{filteredJobs.length}</strong>
          </div>

          <div className="stat-card">
            <span>Sources</span>
            <strong>2</strong>
          </div>
        </section>

        {loading && (
          <div className="state">
            <RefreshCw className="spin" size={24} />
            <p>Loading jobs...</p>
          </div>
        )}

        {error && !loading && (
          <div className="state error-state">
            <p>{error}</p>

            <button onClick={fetchJobs}>
              Try again
            </button>
          </div>
        )}

        {!loading && !error && filteredJobs.length === 0 && (
          <div className="state">
            <Search size={30} />
            <p>No jobs match your search.</p>
          </div>
        )}

        {!loading && !error && filteredJobs.length > 0 && (
          <section className="jobs-grid">
            {filteredJobs.map((job) => (
              <article className="job-card" key={`${job.source}-${job.id}`}>
                <div className="job-top">
                  <div className="company-icon">
                    <Building2 size={20} />
                  </div>

                  <span className="source-badge">
                    {job.source}
                  </span>
                </div>

                <h3>{job.title}</h3>
                <p className="company">
                  {job.company}
                </p>
                <div className="location">
                  <MapPin size={15} />
                  <span>{job.location || "Location not specified"}</span>
                </div>

                <div className="job-footer">
                  <span className={job.remote ? "remote-badge" : "onsite-badge"}>
                    {job.remote ? "Remote" : "On-site"}
                  </span>

                  <a
                    href={job.url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    View job
                    <ExternalLink size={15} />
                  </a>
                </div>
              </article>
            ))}
          </section>
        )}
      </main>
    </div>
  );
}

export default App;