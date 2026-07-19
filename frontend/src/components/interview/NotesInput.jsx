function NotesInput({
  value,
  onChange,
  disabled = false,
}) {
  return (
    <div className="content-card">
      <h3>⌨️ Additional Notes</h3>

      <textarea
        rows={6}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        placeholder="Add extra explanation, time complexity, edge cases, assumptions..."
      />
    </div>
  );
}

export default NotesInput;