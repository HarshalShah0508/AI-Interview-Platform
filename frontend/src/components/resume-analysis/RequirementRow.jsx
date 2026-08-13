import { useState } from "react";

import RequirementDetails from "./RequirementDetails";
import {
  getStatusLabel,
  getStatusTone,
  getPriorityLabel,
  getPriorityTone,
  getEvidenceFoundSummary,
  getRecommendedAction,
} from "../../utils/resumeAnalysisPresentation";

export default function RequirementRow({
  match,
}) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div
      className={`requirement-row ${expanded ? "requirement-row--expanded" : ""}`}
    >

      <button
        type="button"
        className="requirement-row-summary"
        onClick={() => setExpanded((value) => !value)}
        aria-expanded={expanded}
      >

        <div
          className="requirement-cell requirement-cell--name"
          data-label="Requirement"
        >
          {match.requirement}
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
          data-label="Status"
        >
          <span
            className={`badge badge--${getStatusTone(match.match_type)}`}
          >
            {getStatusLabel(match.match_type)}
          </span>
        </div>

        <div
          className="requirement-cell"
          data-label="Evidence Found"
        >
          {getEvidenceFoundSummary(match)}
        </div>

        <div
          className="requirement-cell"
          data-label="Recommended Action"
        >
          {getRecommendedAction(match)}
        </div>

        <span
          className="requirement-row-chevron"
          aria-hidden="true"
        >
          {expanded ? "−" : "+"}
        </span>

      </button>

      {expanded && (
        <RequirementDetails match={match} />
      )}

    </div>
  );
}
