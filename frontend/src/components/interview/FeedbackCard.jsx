function FeedbackCard({
  score,
  feedback,
  strengths = [],
  improvements = [],
}) {
  return (
    <article className="content-card feedback-card">
      <div className="feedback-card__header">
        <div>
          <p className="eyebrow">AI Evaluation</p>
          <h2>Answer Feedback</h2>
        </div>

        <span className="score-badge">{score}/10</span>
      </div>

      <p>{feedback}</p>

      <div className="feedback-grid">
        <div>
          <h3>Strengths</h3>
          <ul>
            {strengths.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>

        <div>
          <h3>Improvements</h3>
          <ul>
            {improvements.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      </div>
    </article>
  );
}

export default FeedbackCard;