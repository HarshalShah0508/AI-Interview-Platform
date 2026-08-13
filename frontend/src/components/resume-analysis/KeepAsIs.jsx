export default function KeepAsIs({
  items,
}) {
  if (!items?.length) {
    return null;
  }

  return (
    <section className="analysis-section">

      <div className="section-heading">
        <span>
          Already Strong
        </span>

        <h2>
          What you should keep
        </h2>

        <p>
          Not every bullet needs an AI rewrite.
        </p>
      </div>

      <div className="keep-list">

        {items.map(
          (item, index) => (
            <article
              key={index}
              className="keep-card"
            >

              <span>
                {item.section}
              </span>

              <p>
                {item.original_text}
              </p>

              <div>
                <strong>
                  Keep as-is
                </strong>

                <p>
                  {item.reason}
                </p>
              </div>

            </article>
          )
        )}

      </div>

    </section>
  );
}