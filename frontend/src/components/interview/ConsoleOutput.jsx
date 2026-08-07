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

  const statusLabel = {
    idle: "Idle",
    running: "Running",
    accepted: "Accepted",
    runtime_error: "Runtime Error",
    compilation_error: "Compilation Error",
    time_limit_exceeded: "Time Limit Exceeded",
    internal_error: "Internal Error",
    not_implemented: "Not Implemented",
  };

  return (
    <div className="content-card">
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "12px",
        }}
      >
        <h3 style={{ margin: 0 }}>
          🖥 Console Output
        </h3>

        <span
          style={{
            fontWeight: "600",
            fontSize: "14px",
          }}
        >
          Status: {statusLabel[status] || status}
        </span>
      </div>

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