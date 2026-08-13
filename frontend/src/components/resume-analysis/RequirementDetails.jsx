import {
  getEvidenceExplanation,
  getConfidenceLabel,
} from "../../utils/resumeAnalysisPresentation";

export default function RequirementDetails({
  match,
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

    </div>
  );
}
