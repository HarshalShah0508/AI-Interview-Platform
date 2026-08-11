export default function ResumeRecommendations({
  recommendations,
}) {
  return (
    <section className="analysis-section">

      <div className="section-heading">
        <span>
          Resume Improvements
        </span>

        <h2>
          What should you change?
        </h2>

        <p>
          These recommendations are based on
          evidence already present in your resume.
        </p>
      </div>

      <div className="recommendation-list">

        {recommendations.map(
          (recommendation, index) => (
            <article
              key={index}
              className="recommendation-card"
            >

              <div className="recommendation-meta">

                <span>
                  {recommendation.change_type}
                </span>

                {recommendation.jd_requirement && (
                  <span>
                    JD:{" "}
                    {recommendation.jd_requirement}
                  </span>
                )}

                <span>
                  {recommendation.safety_status}
                </span>

              </div>

              <div className="recommendation-before">

                <span>
                  Current
                </span>

                <p>
                  {recommendation.original_text}
                </p>

              </div>

              <div className="recommendation-after">

                <span>
                  Suggested
                </span>

                <p>
                  {recommendation.suggested_text}
                </p>

              </div>

              <div className="recommendation-why">

                <strong>
                  Why?
                </strong>

                <p>
                  {recommendation.reason}
                </p>

              </div>

              {recommendation
                .verified_facts_used
                ?.length > 0 && (
                <div>
                  <strong>
                    Evidence used
                  </strong>

                  <ul>
                    {recommendation
                      .verified_facts_used
                      .map(
                        (fact, factIndex) => (
                          <li
                            key={factIndex}
                          >
                            {fact}
                          </li>
                        )
                      )}
                  </ul>
                </div>
              )}

            </article>
          )
        )}

      </div>

    </section>
  );
}