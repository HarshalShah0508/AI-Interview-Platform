import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import useAuth from "../../hooks/useAuth";

function LoginForm() {
  const navigate = useNavigate();
  const { login } = useAuth();

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

    try {
      await login(formData);
      navigate("/dashboard");
    } catch (err) {
      console.error(err);
      console.error(err.response);
      console.error(err.response?.data);

      setError(err.message);
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

      <button className="button button--primary" type="submit">
        Login
      </button>

      <p className="form-footer">
        New to InterviewAI? <Link to="/signup">Create an account</Link>
      </p>
    </form>
  );
}

export default LoginForm;