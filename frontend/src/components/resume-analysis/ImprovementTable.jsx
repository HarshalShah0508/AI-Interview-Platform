import { useState } from "react";

import KeepAsIs from "./KeepAsIs";
import {
  getResumeArea,
  getSafetyBadge,
} from "../../utils/resumeAnalysisPresentation";

function ImprovementRow({
  recommendation,
}) {
  const [expanded, setExpanded] = useState(false);

  const badge = getSafetyBadge(recommendation.safety_status);

  const currentEvidence =
    recommendation.evidence_used?.[0] ||
    recommendation.original_text;

  return (
    <div
      className={`requirement-row ${expanded ? "requirement-row--expanded" : ""}`}
    >

      <button
        type="button"
        className="requirement-row-summary improvement-row-summary"
        onClick={() => setExpanded((value) => !value)}
        aria-expanded={expanded}
      >

        <div
          className="requirement-cell requirement-cell--name"
          data-label="Resume Area"
        >
          {getResumeArea(recommendation)}
        </div>

        <div
          className="requirement-cell"
          data-label="Current Evidence"
        >
          <span className="truncated-text">
            {currentEvidence}
          </span>
        </div>

        <div
          className="requirement-cell"
          data-label="Suggested Improvement"
        >
          <span className="truncated-text">
            {recommendation.suggested_text}
          </span>
        </div>

        <div
          className="requirement-cell"
          data-label="Status"
        >
          <span className={`badge badge--${badge.tone}`}>
            {badge.label}
          </span>
        </div>

        <span
          className="requirement-row-chevron"
          aria-hidden="true"
        >
          {expanded ? "−" : "+"}
        </span>

      </button>

      {expanded && (
        <div className="requirement-details">

          <div className="requirement-details-block">
            <span className="requirement-details-label">
              Current
            </span>

            <p>
              {recommendation.original_text}
            </p>
          </div>

          <div className="requirement-details-block">
            <span className="requirement-details-label">
              Suggested
            </span>

            <p>
              {recommendation.suggested_text}
            </p>
          </div>

          <div className="requirement-details-block">
            <span className="requirement-details-label">
              Why it helps
            </span>

            <p>
              {recommendation.reason}
            </p>
          </div>

        </div>
      )}

    </div>
  );
}

export default function ImprovementTable({
  recommendations,
  keepAsIs,
}) {
  const hasRecommendations = recommendations?.length > 0;
  const hasKeepAsIs = keepAsIs?.length > 0;

  return (
    <section className="analysis-section">

      <div className="section-heading">
        <div>
          <span>
            Resume Improvements
          </span>

          <h2>
            What should you change?
          </h2>

          <p>
            These suggestions are based only on evidence
            already present in your resume.
          </p>
        </div>
      </div>

      {hasRecommendations ? (
        <div className="requirement-table">

          <div className="requirement-table-header improvement-table-header">
            <span>Resume Area</span>
            <span>Current Evidence</span>
            <span>Suggested Improvement</span>
            <span>Status</span>
            <span aria-hidden="true" />
          </div>

          {recommendations.map((recommendation, index) => (
            <ImprovementRow
              key={index}
              recommendation={recommendation}
            />
          ))}

        </div>
      ) : (
        <p className="empty-state">
          No evidence-backed changes were identified. Your
          current resume already presents the relevant
          supported experience clearly.
        </p>
      )}

      {hasKeepAsIs && (
        <KeepAsIs items={keepAsIs} />
      )}

    </section>
  );
}
