function getStatusLabel(type) {
  switch (type) {
    case "strong":
      return "Strong Match";

    case "partial":
      return "Partial Match";

    case "ambiguous":
      return "Needs Review";

    case "missing":
      return "Missing";

    default:
      return type;
  }
}

export default function RequirementMatches({
  matches,
}) {
  return (
    <section className="analysis-section">

      <div className="section-heading">
        <div>
          <span>
            Requirement Analysis
          </span>

          <h2>
            What matches the JD?
          </h2>
        </div>
      </div>

      <div className="requirement-list">

        {matches.map((match) => (
          <article
            key={match.requirement}
            className={
              `requirement-card ${match.match_type}`
            }
          >

            <div className="requirement-card-top">

              <div>
                <h3>
                  {match.requirement}
                </h3>

                <span>
                  {match.category}
                  {" · "}
                  {match.importance}
                </span>
              </div>

              <strong>
                {getStatusLabel(
                  match.match_type
                )}
              </strong>

            </div>

            <div className="requirement-score">
              <div>
                <span>
                  Match strength
                </span>

                <strong>
                  {Math.round(
                    match.score
                  )}
                  %
                </strong>
              </div>

              <div>
                <span>
                  Evidence confidence
                </span>

                <strong>
                  {Math.round(
                    match.evidence_confidence *
                      100
                  )}
                  %
                </strong>
              </div>
            </div>

            <p>
              {match.reason}
            </p>

            {match.matched_resume_evidence
              ?.length > 0 && (
              <div className="evidence-box">

                <span>
                  Resume evidence
                </span>

                {match.matched_resume_evidence.map(
                  (evidence, index) => (
                    <p key={index}>
                      “{evidence}”
                    </p>
                  )
                )}

              </div>
            )}

          </article>
        ))}

      </div>

    </section>
  );
}