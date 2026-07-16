import { Link } from "react-router-dom";

function HistoryItem({ session }) {
  const createdDate = new Date(session.created_at).toLocaleString();

  return (
    <article className="history-item">
      <div>
        <p className="eyebrow">Interview Session</p>

        <h2>{session.role}</h2>

        <p>
          <strong>Difficulty:</strong> {session.difficulty}
        </p>

        <p>
          <strong>Created:</strong> {createdDate}
        </p>
      </div>

      <div
        style={{
          display: "flex",
          gap: "10px",
          flexWrap: "wrap",
        }}
      >
        <Link
          className="button button--secondary"
          to={`/interview/${session.session_id}`}
        >
          Continue Interview
        </Link>

        <Link
          className="button button--primary"
          to={`/results/${session.session_id}`}
        >
          View Results
        </Link>
      </div>
    </article>
  );
}

export default HistoryItem;