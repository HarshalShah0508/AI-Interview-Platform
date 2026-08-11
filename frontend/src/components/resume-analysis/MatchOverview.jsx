export default function MatchOverview({
  score,
  matchingReport,
}) {
  const summary =
    matchingReport?.summary;

  return (
    <section className="match-overview">

      <div className="score-card">
        <span>
          JD Match Score
        </span>

        <strong>
          {score ?? 0}
        </strong>

        <small>
          / 100
        </small>
      </div>

      <div className="match-stat">
        <strong>
          {summary?.strong_matches ?? 0}
        </strong>

        <span>
          Strong matches
        </span>
      </div>

      <div className="match-stat">
        <strong>
          {summary?.partial_matches ?? 0}
        </strong>

        <span>
          Partial matches
        </span>
      </div>

      <div className="match-stat">
        <strong>
          {summary?.missing_matches ?? 0}
        </strong>

        <span>
          Missing
        </span>
      </div>

      <div className="match-stat">
        <strong>
          {summary?.required_matched ?? 0}
          /
          {summary?.required_requirements ?? 0}
        </strong>

        <span>
          Required matched
        </span>
      </div>

    </section>
  );
}