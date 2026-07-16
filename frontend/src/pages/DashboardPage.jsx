import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getDashboard } from "../api/dashboardApi";
import useAuth from "../hooks/useAuth";

const actionCards = [
  {
    title: "Upload Resume",
    description: "Add a PDF resume so future interview questions can match your background.",
    to: "/resume",
  },
  {
    title: "Generate Interview",
    description: "Choose a role and difficulty to prepare a focused practice session.",
    to: "/generate-interview",
  },
  {
    title: "Interview History",
    description: "Review previous practice sessions and revisit your progress.",
    to: "/history",
  },
];

function DashboardPage() {
  const { token } = useAuth();

  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const data = await getDashboard(token);
        setDashboard(data);
      } catch (err) {
        setError(
          err?.response?.data?.detail ||
            "Failed to load dashboard."
        );
      } finally {
        setLoading(false);
      }
    };

    if (token) {
      fetchDashboard();
    }
  }, [token]);

  if (loading) {
    return <p>Loading dashboard...</p>;
  }

  if (error) {
    return <p className="error-text">{error}</p>;
  }

  return (
    <section className="page-shell dashboard-page">
      <div className="page-header">
        <p className="eyebrow">Dashboard</p>

        <h1>Welcome, {dashboard.username} 👋</h1>

        <p>{dashboard.email}</p>
      </div>

      <div className="results-summary">
        <div>
          <p>Latest Resume</p>
          <strong style={{ fontSize: "18px" }}>
            {dashboard.latest_resume ?? "No Resume Uploaded"}
          </strong>
        </div>

        <div>
          <p>Total Interviews</p>
          <strong>{dashboard.total_interviews}</strong>
        </div>

        <div>
          <p>Completed</p>
          <strong>{dashboard.completed_interviews}</strong>
        </div>

        <div>
          <p>In Progress</p>
          <strong>{dashboard.in_progress_interviews}</strong>
        </div>

        <div style={{ gridColumn: "1 / -1" }}>
          <p>Latest Interview</p>

          {dashboard.latest_interview ? (
            <>
              <strong style={{ fontSize: "18px" }}>
                {dashboard.latest_interview.role}
              </strong>

              <br />

              <span>
                {dashboard.latest_interview.difficulty} •{" "}
                {new Date(
                  dashboard.latest_interview.created_at
                ).toLocaleString()}
              </span>
            </>
          ) : (
            <strong style={{ fontSize: "18px" }}>
              No interviews yet
            </strong>
          )}
        </div>
      </div>

      <div className="action-grid">
        {actionCards.map((card) => (
          <Link
            key={card.title}
            to={card.to}
            className="action-card"
          >
            <h2>{card.title}</h2>
            <p>{card.description}</p>
            <span>Open</span>
          </Link>
        ))}
      </div>
    </section>
  );
}

export default DashboardPage;