import RequirementRow from "./RequirementRow";

export default function RequirementTable({
  matches,
  partialMatchGuidance,
}) {
  const guidanceByRequirement = new Map(
    (partialMatchGuidance || []).map((item) => [
      item.requirement,
      item,
    ])
  );

  if (!matches?.length) {
    return (
      <p className="empty-state">
        No requirements were extracted from this job description.
      </p>
    );
  }

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

          <p>
            Click a row to see the resume evidence behind it.
          </p>
        </div>
      </div>

      <div className="requirement-table">

        <div className="requirement-table-header">
          <span>Requirement</span>
          <span>Priority</span>
          <span>Status</span>
          <span>Evidence Found</span>
          <span>Recommended Action</span>
          <span aria-hidden="true" />
        </div>

        {matches.map((match) => (
          <RequirementRow
            key={match.requirement}
            match={match}
            guidance={guidanceByRequirement.get(
              match.requirement
            )}
          />
        ))}

      </div>

    </section>
  );
}
