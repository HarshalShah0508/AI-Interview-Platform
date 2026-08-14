import HistoryList from "../components/history/HistoryList";
import Navbar from "../components/layout/Navbar.jsx";

function HistoryPage() {
  return (
    <div className="history-page">
      <Navbar />
      <main className="history-container">
        <div className="section-header">
          <div className="eyebrow">HISTORY</div>
          <h1>Interview history</h1>
          <p>Review previous sessions and continue anything unfinished.</p>
        </div>

        <HistoryList />
      </main>
    </div>
  );
}

export default HistoryPage;
