function LanguageSelector({
  languages,
  selectedLanguage,
  onLanguageChange,
}) {
  return (
    <select
      className="lang-pill-select"
      value={selectedLanguage.id}
      onChange={(e) => onLanguageChange(e.target.value)}
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
  );
}

export default LanguageSelector;
