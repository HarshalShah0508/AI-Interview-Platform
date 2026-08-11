export default function MissingRequirements({
  requirements,
}) {
  if (!requirements?.length) {
    return null;
  }

  return (
    <section className="analysis-section">

      <div className="section-heading">
        <span>
          Gaps
        </span>

        <h2>
          What is not currently supported?
        </h2>

        <p>
          Missing requirements should never be
          added to a resume unless they are true.
        </p>
      </div>

      <div className="missing-list">

        {requirements.map(
          (item, index) => (
            <article
              key={index}
              className="missing-card"
            >

              <div>
                <h3>
                  {item.requirement}
                </h3>

                <span>
                  {item.importance}
                </span>
              </div>

              <p>
                {item.reason}
              </p>

              <div className="missing-warning">
                <strong>
                  Recommended action:
                </strong>

                <p>
                  {item.candidate_action
                    .replaceAll(
                      "_",
                      " "
                    )}
                </p>

                <small>
                  {item.warning}
                </small>
              </div>

            </article>
          )
        )}

      </div>

    </section>
  );
}