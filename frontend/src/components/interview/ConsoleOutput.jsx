function ConsoleOutput({
  output = "",
  status = "idle",
}) {
  let displayText = "Waiting for execution...";

  if (status === "running") {
    displayText = "Running...";
  } else if (output.trim()) {
    displayText = output;
  }

  return (
    <div className="content-card">
      <h3>🖥 Console Output</h3>

      <pre
        style={{
          minHeight: "120px",
          margin: 0,
          padding: "12px",
          background: "#111827",
          color: "#f3f4f6",
          borderRadius: "8px",
          overflowX: "auto",
          whiteSpace: "pre-wrap",
          fontFamily:
            "SFMono-Regular, Consolas, Monaco, Menlo, monospace",
        }}
      >
        {displayText}
      </pre>
    </div>
  );
}

export default ConsoleOutput;