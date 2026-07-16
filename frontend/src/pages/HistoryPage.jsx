import HistoryList from "../components/history/HistoryList";

function HistoryPage() {
  return (
    <section className="page-shell">
      <div className="page-header">
        <p className="eyebrow">History</p>
        <h1>Interview History</h1>
        <p>
          Review previous interview sessions and continue unfinished ones.
        </p>
      </div>

      <HistoryList />
    </section>
  );
}

export default HistoryPage;