import InterviewGeneratorForm from "../components/interview/InterviewGeneratorForm.jsx";

function GenerateInterviewPage() {
  return (
    <section className="page-shell">
      <div className="page-header">
        <p className="eyebrow">Question generation</p>
        <h1>Generate Interview</h1>
        <p>Choose a role and difficulty to shape your next practice session.</p>
      </div>

      <InterviewGeneratorForm />
    </section>
  );
}

export default GenerateInterviewPage;