import {
  getEvidenceExplanation,
  getConfidenceLabel,
} from "../../utils/resumeAnalysisPresentation";

function PartialMatchGuidancePanel({ guidance }) {
  if (!guidance) {
    return null;
  }

  return (
    <div className="partial-guidance">

      <div className="requirement-details-block">
        <span className="requirement-details-label">
          Why this is only a partial match
        </span>

        <p>{guidance.why_partial}</p>
      </div>

      <div className="requirement-details-block">
        <span className="requirement-details-label">
          How to strengthen it
        </span>

        <p>{guidance.how_to_strengthen}</p>
      </div>

      {guidance.example_wording?.length > 0 && (
        <div className="requirement-details-block">
          <span className="requirement-details-label">
            Example wording — if true
          </span>

          <div className="requirement-evidence-list">
            {guidance.example_wording.map((text, index) => (
              <p
                key={index}
                className="requirement-evidence-item partial-guidance-example"
              >
                “{text}”
              </p>
            ))}
          </div>
        </div>
      )}

      <p className="safety-notice partial-guidance-notice">
        {guidance.safety_note}
      </p>

    </div>
  );
}

export default function RequirementDetails({
  match,
  guidance,
}) {
  const evidence = match.matched_resume_evidence || [];

  return (
    <div className="requirement-details">

      <div className="requirement-details-block">
        <span className="requirement-details-label">
          Why
        </span>

        <p>
          {getEvidenceExplanation(match.evidence_type)}
        </p>
      </div>

      <div className="requirement-details-block">
        <span className="requirement-details-label">
          Evidence confidence
        </span>

        <p>
          {getConfidenceLabel(match.evidence_confidence)}
        </p>
      </div>

      {evidence.length > 0 && (
        <div className="requirement-details-block">
          <span className="requirement-details-label">
            Resume evidence
          </span>

          <div className="requirement-evidence-list">
            {evidence.map((item, index) => (
              <p
                key={index}
                className="requirement-evidence-item"
              >
                “{item}”
              </p>
            ))}
          </div>
        </div>
      )}

      {match.match_type === "partial" && (
        <PartialMatchGuidancePanel guidance={guidance} />
      )}

    </div>
  );
}
