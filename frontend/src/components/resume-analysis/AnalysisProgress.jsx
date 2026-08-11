const stages = [
  {
    threshold: 10,
    label: "Reading job description",
  },
  {
    threshold: 20,
    label: "Understanding job requirements",
  },
  {
    threshold: 35,
    label: "Analyzing resume",
  },
  {
    threshold: 48,
    label: "Verifying resume evidence",
  },
  {
    threshold: 60,
    label: "Matching requirements",
  },
  {
    threshold: 72,
    label: "Finding improvement opportunities",
  },
  {
    threshold: 84,
    label: "Generating recommendations",
  },
  {
    threshold: 94,
    label: "Validating recommendations",
  },
  {
    threshold: 100,
    label: "Analysis complete",
  },
];

export default function AnalysisProgress({
  progress = 0,
  currentStage,
}) {
  return (
    <div className="analysis-progress">
      <div className="analysis-progress-header">
        <div>
          <span>
            Resume Intelligence
          </span>

          <h2>
            Analyzing your resume
          </h2>

          <p>
            We're checking your resume against
            the job description and validating
            every recommendation.
          </p>
        </div>

        <strong>
          {progress}%
        </strong>
      </div>

      <div className="progress-track">
        <div
          className="progress-value"
          style={{
            width: `${progress}%`,
          }}
        />
      </div>

      <div className="analysis-stages">
        {stages.map((stage) => {
          const completed =
            progress >= stage.threshold;

          const active =
            currentStage === stage.label;

          return (
            <div
              key={stage.label}
              className={
                completed
                  ? "analysis-stage completed"
                  : active
                    ? "analysis-stage active"
                    : "analysis-stage"
              }
            >
              <div className="stage-indicator">
                {completed ? "✓" : ""}
              </div>

              <span>
                {stage.label}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}