function QuestionCard({ questionNumber, questionText }) {
  return (
    <article className="content-card question-card">
      <p className="eyebrow">
        Question {questionNumber}
      </p>

      <div
        style={{
          whiteSpace: "pre-wrap",
          lineHeight: "1.8",
          fontSize: "18px",
          color: "#1f2937",
        }}
      >
        {questionText}
      </div>
    </article>
  );
}

export default QuestionCard;