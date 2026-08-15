function CombinedPreview({
  voiceText,
  typedText,
  code,
}) {
  const sections = [];

  if (voiceText.trim()) {
    sections.push(
      `Explanation:\n${voiceText.trim()}`
    );
  }

  if (typedText.trim()) {
    sections.push(
      `Additional Notes:\n${typedText.trim()}`
    );
  }

  if (code.trim()) {
    sections.push(
      `Code:\n${code.trim()}`
    );
  }

  const preview = sections.length
    ? sections.join("\n\n")
    : "Your combined answer will appear here...";

  return (
    <div className="combined-preview">
      <div className="combined-preview__row">
        <span className="combined-preview__label">Combined answer preview</span>
        <span className="combined-preview__meta">
          Voice + Notes + Code will be submitted as one response
        </span>
      </div>

      <textarea
        className="combined-preview__box"
        value={preview}
        readOnly
        rows={6}
      />
    </div>
  );
}

export default CombinedPreview;
