function QuestionCard({ questionNumber, questionText }) {
  return (
    <article className="content-card question-card">
      <p className="eyebrow">Question {questionNumber}</p>
      <h2>{questionText}</h2>
    </article>
  )
}

export default QuestionCard
