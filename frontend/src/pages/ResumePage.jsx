import ResumeUploadCard from '../components/resume/ResumeUploadCard.jsx'
import AnalysisHistoryList from '../components/resume-analysis/AnalysisHistoryList.jsx'

function ResumePage() {
  return (
    <section className="page-shell">
      <div className="page-header">
        <p className="eyebrow">Resume</p>
        <h1>Resume Page</h1>
        <p>Upload a PDF resume that future interview sessions can use for context.</p>
      </div>
      <ResumeUploadCard />

      <div className="page-header">
        <p className="eyebrow">History</p>
        <h1>Past Resume ↔ JD Analyses</h1>
        <p>Revisit the results of job descriptions you've already analyzed your resume against.</p>
      </div>
      <AnalysisHistoryList />
    </section>
  )
}

export default ResumePage
