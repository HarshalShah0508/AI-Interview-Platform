function CodeEditor({
  value,
  onChange,
  disabled = false,
}) {
  return (
    <div className="content-card">
      <h3>💻 Code</h3>

      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        rows={14}
        spellCheck={false}
        placeholder={`Write your code here...

Example:

void bfs(...) {

}`}
        style={{
          width: "100%",
          fontFamily:
            "SFMono-Regular, Consolas, Monaco, Menlo, monospace",
          fontSize: "14px",
          lineHeight: "1.5",
          resize: "vertical",
          whiteSpace: "pre",
          tabSize: 4,
        }}
      />
    </div>
  );
}

export default CodeEditor;