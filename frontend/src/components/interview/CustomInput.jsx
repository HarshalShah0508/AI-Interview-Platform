function CustomInput({
  value,
  onChange,
  disabled = false,
}) {
  return (
    <div className="content-card">
      <h3>⌨️ Custom Input (stdin)</h3>

      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        rows={6}
        spellCheck={false}
        placeholder={`Example

5
1 2 3 4 5`}
        style={{
          width: "100%",
          resize: "vertical",
          fontFamily:
            "SFMono-Regular, Consolas, Monaco, Menlo, monospace",
        }}
      />
    </div>
  );
}

export default CustomInput;