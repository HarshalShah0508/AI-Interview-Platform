import {
  getStatusLabel,
  getStatusTone,
  getPriorityLabel,
  getPriorityTone,
  getEvidenceExplanation,
} from "../../utils/resumeAnalysisPresentation";

const FALLBACK_REVIEW_HINT =
  "Review your resume for stronger, more explicit evidence " +
  "of this requirement. Only add it if it is genuinely true.";

export default function ReviewAreasTable({
  matches,
  missingActions,
}) {
  const actionsByRequirement = new Map(
    (missingActions || []).map((action) => [
      action.requirement,
      action,
    ])
  );

  const reviewMatches = (matches || []).filter(
    (match) =>
      match.match_type === "missing" ||
      match.match_type === "ambiguous"
  );

  if (!reviewMatches.length) {
    return (
      <section className="analysis-section">

        <div className="section-heading">
          <span>
            Review Areas
          </span>

          <h2>
            What is not currently supported?
          </h2>
        </div>

        <p className="empty-state">
          No gaps found — your resume shows evidence for every
          extracted requirement.
        </p>

      </section>
    );
  }

  return (
    <section className="analysis-section">

      <div className="section-heading">
        <span>
          Review Areas
        </span>

        <h2>
          What is not currently supported?
        </h2>

        <p>
          These requirements either have no evidence in your
          resume, or the evidence is not explicit enough to
          confirm a match.
        </p>
      </div>

      <div className="requirement-table">

        <div className="requirement-table-header review-table-header">
          <span>Requirement</span>
          <span>Priority</span>
          <span>Why It Is Not Currently Matched</span>
          <span>What To Review In Your Experience</span>
        </div>

        {reviewMatches.map((match) => {
          const action = actionsByRequirement.get(
            match.requirement
          );

          return (
            <div
              key={match.requirement}
              className="requirement-row review-row"
            >

              <div
                className="requirement-cell requirement-cell--name"
                data-label="Requirement"
              >
                {match.requirement}

                <span
                  className={`badge badge--${getStatusTone(match.match_type)} review-status-badge`}
                >
                  {getStatusLabel(match.match_type)}
                </span>
              </div>

              <div
                className="requirement-cell"
                data-label="Priority"
              >
                <span
                  className={`badge badge--${getPriorityTone(match.importance)}`}
                >
                  {getPriorityLabel(match.importance)}
                </span>
              </div>

              <div
                className="requirement-cell"
                data-label="Why It Is Not Currently Matched"
              >
                {getEvidenceExplanation(match.evidence_type)}
              </div>

              <div
                className="requirement-cell"
                data-label="What To Review In Your Experience"
              >
                {action?.warning || FALLBACK_REVIEW_HINT}
              </div>

            </div>
          );
        })}

      </div>

      <p className="safety-notice">
        Only add a skill, achievement, responsibility, or
        experience if it is true and you can support it.
      </p>

    </section>
  );
}
