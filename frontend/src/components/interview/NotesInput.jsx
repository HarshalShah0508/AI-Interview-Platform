function NotesInput({
  value,
  onChange,
  disabled = false,
}) {
  return (
    <div className="mode-block">
      <div className="mode-block__header">
        <span className="mode-block__label">ADDITIONAL NOTES</span>
      </div>

      <textarea
        className="notes-textarea"
        rows={4}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        placeholder="Add extra explanation, time complexity, edge cases, assumptions..."
      />
    </div>
  );
}

export default NotesInput;
