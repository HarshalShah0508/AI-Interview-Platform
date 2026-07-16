import ResumeUploadCard from '../components/resume/ResumeUploadCard.jsx'

function ResumePage() {
  return (
    <section className="page-shell">
      <div className="page-header">
        <p className="eyebrow">Resume</p>
        <h1>Resume Page</h1>
        <p>Upload a PDF resume that future interview sessions can use for context.</p>
      </div>
      <ResumeUploadCard />
    </section>
  )
}

export default ResumePage
