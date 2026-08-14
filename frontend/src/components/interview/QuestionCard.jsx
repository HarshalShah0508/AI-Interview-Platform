function QuestionCard({ questionText, isFollowUp }) {
  return (
    <article className="question-card">
      {isFollowUp && (
        <div className="follow-up-banner">
          <span className="follow-up-banner__tag">FOLLOW-UP</span>
          <span className="follow-up-banner__text">
            The interviewer is digging deeper into your previous answer.
          </span>
        </div>
      )}

      <p className="question-card__text">{questionText}</p>
    </article>
  );
}

export default QuestionCard;
