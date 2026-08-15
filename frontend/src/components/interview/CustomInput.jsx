function CustomInput({
  value,
  onChange,
  disabled = false,
}) {
  return (
    <div className="stdin-row">
      <span className="mode-block__label">STDIN</span>
      <textarea
        className="stdin-input"
        rows={2}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        spellCheck={false}
        placeholder={`Custom input for test run\n5\n1 2 3 4 5`}
      />
    </div>
  );
}

export default CustomInput;
