import SignupForm from '../components/auth/SignupForm.jsx'

function SignupPage() {
  return (
    <section className="auth-page">
      <div className="page-header page-header--centered">
        <p className="eyebrow">Create account</p>
        <h1>Signup Page</h1>
        <p>Set up your workspace for resume-based interview practice.</p>
      </div>
      <SignupForm />
    </section>
  )
}

export default SignupPage
