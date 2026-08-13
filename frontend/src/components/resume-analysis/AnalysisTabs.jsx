export default function AnalysisTabs({
  tabs,
  activeTab,
  onChange,
}) {
  return (
    <div
      className="analysis-tabs"
      role="tablist"
    >

      {tabs.map((tab) => (
        <button
          key={tab.id}
          type="button"
          role="tab"
          aria-selected={activeTab === tab.id}
          className={`analysis-tab ${activeTab === tab.id ? "analysis-tab--active" : ""}`}
          onClick={() => onChange(tab.id)}
        >
          {tab.label}

          {typeof tab.count === "number" && (
            <span className="analysis-tab-count">
              {tab.count}
            </span>
          )}
        </button>
      ))}

    </div>
  );
}
