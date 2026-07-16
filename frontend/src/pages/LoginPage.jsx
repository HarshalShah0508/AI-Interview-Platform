import LoginForm from '../components/auth/LoginForm.jsx'

function LoginPage() {
  return (
    <section className="auth-page">
      <div className="page-header page-header--centered">
        <p className="eyebrow">Welcome back</p>
        <h1>Login Page</h1>
        <p>Sign in to continue preparing for your next interview.</p>
      </div>
      <LoginForm />
    </section>
  )
}

export default LoginPage
