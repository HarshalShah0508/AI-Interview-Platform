import { useEffect, useState } from "react";
import { FaTrash } from "react-icons/fa";

import {
  getResumes,
  uploadResume,
  deleteResume,
} from "../../api/resumeApi";

import useAuth from "../../hooks/useAuth";

function ResumeUploadCard() {
  const { token } = useAuth();

  const [selectedFile, setSelectedFile] = useState(null);
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [fetchingResumes, setFetchingResumes] = useState(true);
  const [deletingResumeId, setDeletingResumeId] = useState(null);

  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  const loadResumes = async () => {
    try {
      setFetchingResumes(true);
      const data = await getResumes(token);
      setResumes(data);
    } catch {
      setError("Failed to load resumes");
    } finally {
      setFetchingResumes(false);
    }
  };

  useEffect(() => {
    if (token) {
      loadResumes();
    }
  }, [token]);

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    setSuccess("");
    setError("");

    if (!file) {
      setSelectedFile(null);
      return;
    }

    if (file.type !== "application/pdf") {
      setError("Only PDF files are allowed");
      setSelectedFile(null);
      return;
    }

    setSelectedFile(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select a PDF resume first");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setSuccess("");

      const response = await uploadResume(selectedFile, token);

      setSuccess(
        `Resume uploaded successfully: ${response.filename}`
      );

      setSelectedFile(null);

      await loadResumes();
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
          "Resume upload failed"
      );
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (resume) => {
    const confirmed = window.confirm(
      `Are you sure you want to permanently delete "${resume.original_filename}"?`
    );

    if (!confirmed) {
      return;
    }

    try {
      setDeletingResumeId(resume.id);

      setSuccess("");
      setError("");

      await deleteResume(resume.id, token);

      setSuccess("Resume deleted successfully.");

      await loadResumes();
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
          "Failed to delete resume."
      );
    } finally {
      setDeletingResumeId(null);
    }
  };

  return (
    <div className="content-card upload-card">
      <div>
        <h2>Upload your resume</h2>

        <p>
          Upload a PDF resume so interview questions can
          be tailored to your profile.
        </p>
      </div>

      <div className="file-dropzone">
        <label className="form-field">
          <span>Select PDF resume</span>

          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
          />
        </label>

        {selectedFile && (
          <div className="file-preview">
            Selected file:
            <strong> {selectedFile.name}</strong>
          </div>
        )}

        <button
          className="button button--primary"
          type="button"
          onClick={handleUpload}
          disabled={loading}
        >
          {loading
            ? "Uploading..."
            : "Upload Resume"}
        </button>
      </div>

      {success && (
        <p className="success-text">{success}</p>
      )}

      {error && (
        <p className="error-text">{error}</p>
      )}

      <div className="resume-list-section">
        <h3>Your uploaded resumes</h3>

        {fetchingResumes ? (
          <p>Loading resumes...</p>
        ) : resumes.length === 0 ? (
          <p>No resumes uploaded yet.</p>
        ) : (
          <div className="resume-list">
            {resumes.map((resume) => (
              <div
                className="resume-item"
                key={resume.id}
              >
                <div className="resume-item-header">
                  <p>
                    <strong>
                      {resume.original_filename}
                    </strong>
                  </p>

                  <p>
                    Uploaded on:{" "}
                    {new Date(
                      resume.created_at
                    ).toLocaleString()}
                  </p>
                </div>

                <button
                  type="button"
                  className="resume-delete-button"
                  title="Delete Resume"
                  disabled={
                    deletingResumeId === resume.id
                  }
                  onClick={() =>
                    handleDelete(resume)
                  }
                >
                  {deletingResumeId ===
                  resume.id ? (
                    "..."
                  ) : (
                    <FaTrash />
                  )}
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default ResumeUploadCard;