import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import useAuth from "../../hooks/useAuth";
import GoogleLoginButton from "./GoogleLoginButton";
function LoginForm() {
  const navigate = useNavigate();
  const {
    login,
    resendVerificationEmail,
} = useAuth();
  const [showResend, setShowResend] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");

  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [error, setError] = useState("");

  const handleChange = (event) => {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setSuccessMessage("");
    setShowResend(false);

    try {
      await login(formData);
      navigate("/dashboard");
    } catch (err) {

      const message =
        err.response?.data?.detail ||
        "Login failed.";

      setError(message);

      if (
        err.response?.status === 403 &&
        message ===
          "Please verify your email before logging in."
      ) {
          setShowResend(true);
      } else {
          setShowResend(false);
  }
}
  };
  const handleResendVerification = async () => {

  try {

    const response =
      await resendVerificationEmail(
        formData.email
      );

    setSuccessMessage(
      response.message
    );

  } catch {

    setError(
      "Unable to resend verification email."
    );
    setSuccessMessage("");
  }

};

  return (
    <form className="auth-card" onSubmit={handleSubmit}>
      <label className="form-field">
        <span>Email</span>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="you@example.com"
          required
        />
      </label>

      <label className="form-field">
        <span>Password</span>
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          placeholder="Enter your password"
          required
        />
      </label>

      {error && <p className="error-text">{error}</p>}
      {showResend && (
  <button
    type="button"
    className="button button--secondary"
    onClick={handleResendVerification}
  >
    Resend Verification Email
  </button>
)}

{successMessage && (
  <p className="success-text">
    {successMessage}
  </p>
)}

      <button className="button button--primary" type="submit">
        Login
      </button>
      <div className="auth-divider">
        <hr />
        <span>OR</span>
        <hr />
      </div>

      <GoogleLoginButton />

      <p className="form-footer">
        New to Hot Seat? <Link to="/signup">Create an account</Link>
      </p>
    </form>
  );
}

export default LoginForm;