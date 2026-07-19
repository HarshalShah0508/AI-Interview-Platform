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
    <div className="content-card">
      <h3>👀 Combined Answer Preview</h3>

      <textarea
        value={preview}
        readOnly
        rows={16}
        style={{
          width: "100%",
          fontFamily:
            "SFMono-Regular, Consolas, Monaco, Menlo, monospace",
          fontSize: "14px",
          lineHeight: "1.5",
          resize: "vertical",
          whiteSpace: "pre-wrap",
        }}
      />
    </div>
  );
}

export default CombinedPreview;