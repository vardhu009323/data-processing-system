
import { useCallback, useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";
const PAGE_SIZE = 5;

function App() {
  const [numbers, setNumbers] = useState("12, 45, 7, 23");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const [jobs, setJobs] = useState([]);
  const [historyError, setHistoryError] = useState("");
  const [historyLoading, setHistoryLoading] = useState(true);
  const [skip, setSkip] = useState(0);

  const fetchJobs = useCallback(async (currentSkip = 0) => {
    setHistoryLoading(true);
    setHistoryError("");

    try {
      const response = await fetch(
        `${API_URL}/jobs?skip=${currentSkip}&limit=${PAGE_SIZE + 1}`
      );

      if (!response.ok) {
        throw new Error("Could not load job history.");
      }

      const data = await response.json();
      setJobs(data);
    } catch {
      setHistoryError(
        "Could not load job history. Check that FastAPI is running."
      );
    } finally {
      setHistoryLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchJobs(0);
  }, [fetchJobs]);

  async function handleSubmit(event) {
    event.preventDefault();

    const parsedNumbers = numbers.split(",").map((value) => value.trim());

    if (
      parsedNumbers.some(
        (value) => value === "" || !/^-?\d+$/.test(value)
      )
    ) {
      setError("Enter integers separated by commas.");
      setResult(null);
      return;
    }

    const values = parsedNumbers.map(Number);

    if (
      values.length > 10000 ||
      values.some((value) => !Number.isSafeInteger(value))
    ) {
      setError("Enter up to 10,000 safe integers.");
      setResult(null);
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/jobs`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ numbers: values }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to process the job.");
      }

      setResult(data);
      setSkip(0);
      await fetchJobs(0);
    } catch (err) {
      setError(
        err.message === "Failed to fetch"
          ? "Cannot reach the API. Check that FastAPI is running."
          : err.message
      );
    } finally {
      setLoading(false);
    }
  }

  async function changePage(newSkip) {
    setSkip(newSkip);
    await fetchJobs(newSkip);
  }

  const visibleJobs = jobs.slice(0, PAGE_SIZE);
  const hasNextPage = jobs.length > PAGE_SIZE;

  return (
    <main className="dashboard">
      <header className="header">
        <div className="brand-mark">DP</div>
        <div>
          <h1>Data Processing System</h1>
          <p>C++ processing · FastAPI · PostgreSQL</p>
        </div>
      </header>

      <section className="intro">
        <p className="eyebrow">PROCESSING WORKSPACE</p>
        <h2>Turn your data into results.</h2>
        <p>
          Submit a dataset, inspect the results, and track your
          previous processing jobs.
        </p>
      </section>

      <section className="panel">
        <h3>Submit a job</h3>
        <p className="muted">
          Enter integers separated by commas.
        </p>

        <form onSubmit={handleSubmit}>
          <label htmlFor="numbers">Dataset</label>
          <textarea
            id="numbers"
            value={numbers}
            onChange={(event) => setNumbers(event.target.value)}
            placeholder="12, 45, 7, 23"
            rows={4}
          />

          <button type="submit" disabled={loading}>
            {loading ? "Processing..." : "Process dataset"}
          </button>
        </form>
      </section>

      {error && (
        <div className="message error" role="alert">
          {error}
        </div>
      )}

      {result && (
        <section className="panel results" aria-live="polite">
          <div className="result-heading">
            <div>
              <p className="eyebrow">JOB COMPLETED</p>
              <h3>Processing results</h3>
            </div>
            <span className="status">{result.status}</span>
          </div>

          <p className="muted">
            Job ID: {result.job_id} · Input size: {result.input_size}
          </p>

          <div className="result-grid">
            <article className="result-card">
              <p>Maximum</p>
              <strong>{result.result.maximum}</strong>
            </article>
            <article className="result-card">
              <p>Minimum</p>
              <strong>{result.result.minimum}</strong>
            </article>
            <article className="result-card">
              <p>Sum</p>
              <strong>{result.result.sum}</strong>
            </article>
          </div>
        </section>
      )}

      <section className="panel history">
        <div className="history-heading">
          <div>
            <p className="eyebrow">YOUR ACTIVITY</p>
            <h3>Job history</h3>
            <p className="muted">
              Recently submitted datasets and their results.
            </p>
          </div>

          <button
            type="button"
            className="secondary-button"
            onClick={() => fetchJobs(skip)}
            disabled={historyLoading}
          >
            {historyLoading ? "Loading..." : "Refresh"}
          </button>
        </div>

        {historyError && (
          <div className="message error" role="alert">
            {historyError}
          </div>
        )}

        {historyLoading ? (
          <p className="muted">Loading jobs...</p>
        ) : visibleJobs.length === 0 ? (
          <p className="empty-state">
            No jobs on this page yet. Submit a dataset to get started.
          </p>
        ) : (
          <>
            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Job ID</th>
                    <th>Status</th>
                    <th>Input size</th>
                    <th>Maximum</th>
                    <th>Minimum</th>
                    <th>Sum</th>
                  </tr>
                </thead>
                <tbody>
                  {visibleJobs.map((job) => (
                    <tr key={job.job_id}>
                      <td>#{job.job_id}</td>
                      <td>
                        <span className="status">{job.status}</span>
                      </td>
                      <td>{job.input_size}</td>
                      <td>{job.result.maximum}</td>
                      <td>{job.result.minimum}</td>
                      <td>{job.result.sum}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="pagination">
              <span className="muted">
                Showing {skip + 1}–{skip + visibleJobs.length}
              </span>

              <div className="pagination-buttons">
                <button
                  type="button"
                  className="secondary-button"
                  onClick={() => changePage(Math.max(0, skip - PAGE_SIZE))}
                  disabled={skip === 0 || historyLoading}
                >
                  Previous
                </button>

                <button
                  type="button"
                  className="secondary-button"
                  onClick={() => changePage(skip + PAGE_SIZE)}
                  disabled={!hasNextPage || historyLoading}
                >
                  Next
                </button>
              </div>
            </div>
          </>
        )}
      </section>

      <footer>
        High-Performance Data Processing &amp; Job Scheduler
      </footer>
    </main>
  );
}

export default App;
