const sampleQuestions = [
  {
    question: 'Explain a backend API you built and how the frontend consumed it.',
    score: 84,
    note: 'Good end-to-end explanation with solid ownership.',
  },
  {
    question: 'Describe a time you improved performance in an application.',
    score: 78,
    note: 'Clear approach, but the result needs stronger metrics.',
  },
  {
    question: 'How do you handle validation across client and server?',
    score: 88,
    note: 'Strong coverage of UX, security, and data consistency.',
  },
]

function SessionResultsCard() {
  return (
    <article className="content-card results-card">
      <div className="results-summary">
        <div>
          <p className="eyebrow">Overall score</p>
          <strong>83</strong>
          <span>/100</span>
        </div>
        <div>
          <p>Questions answered</p>
          <strong>3</strong>
        </div>
        <div>
          <p>Average score</p>
          <strong>83%</strong>
        </div>
      </div>

      <p className="results-note">
        Mock summary: your answers show solid practical experience. Add sharper
        metrics and more concise tradeoff explanations to strengthen the final
        interview delivery.
      </p>

      <div className="question-results">
        {sampleQuestions.map((item, index) => (
          <div className="question-result" key={item.question}>
            <div>
              <p className="eyebrow">Question {index + 1}</p>
              <h3>{item.question}</h3>
              <p>{item.note}</p>
            </div>
            <span className="score-badge">{item.score}</span>
          </div>
        ))}
      </div>
    </article>
  )
}

export default SessionResultsCard
