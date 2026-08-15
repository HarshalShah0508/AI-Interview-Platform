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

  const isError = ["runtime_error", "compilation_error", "internal_error"].includes(status);

  return (
    <div className="console-shell">
      <div className="console-shell__header">
        <span className="console-shell__title">CONSOLE OUTPUT</span>
        <span className={`console-shell__status ${isError ? "console-shell__status--error" : ""}`}>
          {statusLabel[status] || status}
        </span>
      </div>

      <pre className="console-shell__body">{displayText}</pre>
    </div>
  );
}

export default ConsoleOutput;
