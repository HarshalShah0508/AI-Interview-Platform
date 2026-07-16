import { useEffect, useState } from "react";

import { getInterviewHistory } from "../../api/interviewApi";
import useAuth from "../../hooks/useAuth";

import HistoryItem from "./HistoryItem";

function HistoryList() {
  const { token } = useAuth();

  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await getInterviewHistory(token);
        setSessions(data);
      } catch (err) {
        setError(
          err?.response?.data?.detail ||
            "Failed to load interview history."
        );
      } finally {
        setLoading(false);
      }
    };

    if (token) {
      fetchHistory();
    }
  }, [token]);

  if (loading) {
    return <p>Loading interview history...</p>;
  }

  if (error) {
    return <p className="error-text">{error}</p>;
  }

  if (sessions.length === 0) {
    return (
      <div className="content-card">
        <p>No interview sessions found.</p>
      </div>
    );
  }

  return (
    <div className="history-list">
      {sessions.map((session) => (
        <HistoryItem
          key={session.session_id}
          session={session}
        />
      ))}
    </div>
  );
}

export default HistoryList;