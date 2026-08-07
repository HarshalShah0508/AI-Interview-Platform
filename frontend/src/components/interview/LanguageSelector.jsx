function LanguageSelector({
  languages,
  selectedLanguage,
  onLanguageChange,
}) {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "flex-end",
        marginBottom: "12px",
      }}
    >
      <select
        value={selectedLanguage.id}
        onChange={(e) => onLanguageChange(e.target.value)}
        style={{
          padding: "8px 12px",
          borderRadius: "6px",
          fontSize: "14px",
          cursor: "pointer",
        }}
      >
        {languages.map((language) => (
          <option
            key={language.id}
            value={language.id}
          >
            {language.name}
          </option>
        ))}
      </select>
    </div>
  );
}

export default LanguageSelector;