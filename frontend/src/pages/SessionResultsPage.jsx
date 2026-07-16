import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { getSessionResults } from "../api/answerApi";
import useAuth from "../hooks/useAuth";

function SessionResultsPage() {
  const { sessionId } = useParams();
  const { token } = useAuth();

  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const data = await getSessionResults(sessionId, token);
        setResults(data);
      } catch (err) {
        setError(
          err?.response?.data?.detail ||
            "Failed to load session results."
        );
      } finally {
        setLoading(false);
      }
    };

    if (token) {
      fetchResults();
    }
  }, [sessionId, token]);

  if (loading) {
    return (
      <section className="page-shell">
        <p>Loading results...</p>
      </section>
    );
  }

  if (error) {
    return (
      <section className="page-shell">
        <p className="error-text">{error}</p>
      </section>
    );
  }

  return (
    <section className="page-shell">
      <div className="page-header">
        <p className="eyebrow">Interview Results</p>
        <h1>Session Summary</h1>
      </div>

      <div className="content-card results-card">
        <h2>Overall Performance</h2>

        <p>
          <strong>Average Score:</strong> {results.average_score}/10
        </p>

        <p>
          <strong>Questions Attempted:</strong>{" "}
          {results.questions_attempted}
        </p>

        <h3>Strong Topics</h3>

        {results.strong_topics.length === 0 ? (
          <p>None</p>
        ) : (
          <ul>
            {results.strong_topics.map((topic, index) => (
              <li key={index}>{topic}</li>
            ))}
          </ul>
        )}

        <h3>Weak Topics</h3>

        {results.weak_topics.length === 0 ? (
          <p>None</p>
        ) : (
          <ul>
            {results.weak_topics.map((topic, index) => (
              <li key={index}>{topic}</li>
            ))}
          </ul>
        )}
      </div>

      <div className="page-actions">
        <Link className="button button--secondary" to="/dashboard">
          Dashboard
        </Link>

        <Link
          className="button button--primary"
          to="/generate-interview"
        >
          New Interview
        </Link>
      </div>
    </section>
  );
}

export default SessionResultsPage;