import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import useAuth from "../../hooks/useAuth";
import GoogleLoginButton from "./GoogleLoginButton";
function SignupForm() {
  const navigate = useNavigate();
  const { signup } = useAuth();

  const [formData, setFormData] = useState({
    username: "",
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

    try {
      await signup(formData);

      alert(
        "Account created successfully! Please check your email and verify your account before logging in."
    );

      navigate("/login");

  } catch (err) {

      setError(
        err.response?.data?.detail ||
        "Signup failed."
    );
  }
};

  return (
    <form className="auth-card" onSubmit={handleSubmit}>
      <label className="form-field">
        <span>Username</span>
        <input
          type="text"
          name="username"
          value={formData.username}
          onChange={handleChange}
          placeholder="Your name"
          required
        />
      </label>

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
          placeholder="Create a password"
          required
        />
      </label>

      {error && <p className="error-text">{error}</p>}

      <button className="button button--primary" type="submit">
        Signup
      </button>
      <div className="auth-divider">
        <hr />
        <span>OR</span>
        <hr />
      </div>

      <GoogleLoginButton />

      <p className="form-footer">
        Already have an account? <Link to="/login">Login</Link>
      </p>
    </form>
  );
}

export default SignupForm;