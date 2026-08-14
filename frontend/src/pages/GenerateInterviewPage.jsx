import InterviewGeneratorForm from "../components/interview/InterviewGeneratorForm.jsx";
import Navbar from "../components/layout/Navbar.jsx";

function GenerateInterviewPage() {
  return (
    <div className="generate-page">
      <Navbar />
      <main className="generate-container">
        <div className="generate-card">
          <div className="eyebrow">INTERVIEW SETUP</div>
          <h1 className="generate-card__headline">Configure your session</h1>
          <p className="generate-card__sub">
            HotSeat will generate a resume-tailored interview for the role and
            difficulty you choose below.
          </p>

          <InterviewGeneratorForm />
        </div>
      </main>
    </div>
  );
}

export default GenerateInterviewPage;
