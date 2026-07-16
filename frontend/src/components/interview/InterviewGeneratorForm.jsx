import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { generateInterview } from "../../api/interviewApi";
import { getResumes } from "../../api/resumeApi";
import useAuth from "../../hooks/useAuth";

function InterviewGeneratorForm() {
  const navigate = useNavigate();
  const { token } = useAuth();

  const [formData, setFormData] = useState({
    role: "",
    difficulty: "Medium",
    resume_id: "",
  });

  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingResumes, setLoadingResumes] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchResumes = async () => {
      try {
        const data = await getResumes(token);

        setResumes(data);

        if (data.length > 0) {
          setFormData((prev) => ({
            ...prev,
            resume_id: data[0].id,
          }));
        }
      } catch (err) {
        setError("Failed to load resumes.");
      } finally {
        setLoadingResumes(false);
      }
    };

    fetchResumes();
  }, [token]);

  const handleChange = (event) => {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");

    if (!formData.role.trim()) {
      setError("Please enter a role.");
      return;
    }

    if (!formData.resume_id) {
      setError("Please select a resume.");
      return;
    }

    try {
      setLoading(true);

      const response = await generateInterview(
        {
          role: formData.role.trim(),
          difficulty: formData.difficulty,
          resume_id: Number(formData.resume_id),
        },
        token
      );

      navigate(`/interview/${response.session_id}`);
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
          "Failed to generate interview."
      );
    } finally {
      setLoading(false);
    }
  };

  if (loadingResumes) {
    return <p>Loading resumes...</p>;
  }

  return (
    <form
      className="content-card generator-form"
      onSubmit={handleSubmit}
    >
      <div>
        <h2>Generate Interview</h2>
        <p>Select a resume, role and difficulty.</p>
      </div>

      <label className="form-field">
        <span>Resume</span>

        <select
          name="resume_id"
          value={formData.resume_id}
          onChange={handleChange}
        >
          {resumes.map((resume) => (
            <option
              key={resume.id}
              value={resume.id}
            >
              {resume.original_filename}
            </option>
          ))}
        </select>
      </label>

      <label className="form-field">
        <span>Role</span>

        <input
          type="text"
          name="role"
          placeholder="e.g. Backend Engineer"
          value={formData.role}
          onChange={handleChange}
        />
      </label>

      <label className="form-field">
        <span>Difficulty</span>

        <select
          name="difficulty"
          value={formData.difficulty}
          onChange={handleChange}
        >
          <option value="Easy">Easy</option>
          <option value="Medium">Medium</option>
          <option value="Hard">Hard</option>
        </select>
      </label>

      {error && (
        <p className="error-text">{error}</p>
      )}

      <button
        className="button button--primary"
        type="submit"
        disabled={loading}
      >
        {loading
          ? "Generating..."
          : "Generate Interview"}
      </button>
    </form>
  );
}

export default InterviewGeneratorForm;