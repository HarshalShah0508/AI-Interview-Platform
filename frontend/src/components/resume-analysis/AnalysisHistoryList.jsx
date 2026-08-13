import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getResumeAnalysisHistory } from "../../api/resumeAnalysisApi";
import useAuth from "../../hooks/useAuth";

function getStatusBadge(status) {
  switch (status) {
    case "completed":
      return { label: "Completed", tone: "positive" };
    case "failed":
      return { label: "Failed", tone: "critical" };
    default:
      return { label: "Processing", tone: "info" };
  }
}

function AnalysisHistoryItem({ analysis }) {
  const badge = getStatusBadge(analysis.status);

  const createdDate = new Date(
    analysis.created_at
  ).toLocaleString();

  return (
    <article className="history-item">
      <div>
        <p className="eyebrow">
          Resume ↔ JD Analysis
        </p>

        <h2>
          {analysis.job_title || "Untitled role"}
        </h2>

        <p>
          <strong>Resume:</strong>{" "}
          {analysis.resume_filename || "Unknown resume"}
        </p>

        <p>
          <strong>Analyzed:</strong> {createdDate}
        </p>

        <p>
          <span className={`badge badge--${badge.tone}`}>
            {badge.label}
          </span>

          {analysis.status === "completed" && (
            <>
              {" "}
              <strong>Score:</strong>{" "}
              {analysis.overall_score ?? "—"}/100
            </>
          )}
        </p>
      </div>

      {analysis.status === "completed" && (
        <Link
          className="button button--primary"
          to={`/resume-analysis/${analysis.analysis_id}`}
        >
          View Results
        </Link>
      )}
    </article>
  );
}

export default function AnalysisHistoryList() {
  const { token } = useAuth();

  const [analyses, setAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!token) {
      return;
    }

    const fetchHistory = async () => {
      try {
        const data = await getResumeAnalysisHistory(token);
        setAnalyses(data);
      } catch (err) {
        setError(
          err?.response?.data?.detail ||
            "Failed to load your past analyses."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, [token]);

  if (loading) {
    return <p>Loading your past analyses...</p>;
  }

  if (error) {
    return <p className="error-text">{error}</p>;
  }

  if (analyses.length === 0) {
    return (
      <div className="content-card">
        <p>
          You haven't analyzed a resume against a job
          description yet.
        </p>
      </div>
    );
  }

  return (
    <div className="history-list">
      {analyses.map((analysis) => (
        <AnalysisHistoryItem
          key={analysis.analysis_id}
          analysis={analysis}
        />
      ))}
    </div>
  );
}
