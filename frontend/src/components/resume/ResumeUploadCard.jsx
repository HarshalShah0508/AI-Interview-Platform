import { useEffect, useRef, useState } from "react";
import { FaTrash } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import {
  getResumes,
  uploadResume,
  deleteResume,
} from "../../api/resumeApi";

import useAuth from "../../hooks/useAuth";
import {
  startResumeAnalysis,
  getResumeAnalysisStatus,
} from "../../api/resumeAnalysisApi";

import AnalysisProgress from "../resume-analysis/AnalysisProgress";
function ResumeUploadCard() {
  const { token } = useAuth();
  const fileInputRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [fetchingResumes, setFetchingResumes] = useState(true);
  const [deletingResumeId, setDeletingResumeId] = useState(null);
  const navigate = useNavigate();
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  //Jd Analysis
  const [analysisResumeId, setAnalysisResumeId] =
  useState("");
  const [jobDescription, setJobDescription] =
  useState("");

  const [jobDescriptionFile, setJobDescriptionFile] =
  useState(null);

  const [analysisId, setAnalysisId] =
  useState(null);

  const [analysisStatus, setAnalysisStatus] =
  useState(null);

  const [analysisLoading, setAnalysisLoading] =
  useState(false);

  const [analysisError, setAnalysisError] =
  useState("");
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
  useEffect(() => {
  if (!analysisId) {
    return;
  }

  let cancelled = false;
  let timeoutId;

  const pollAnalysis = async () => {
    try {
      const status =
        await getResumeAnalysisStatus(
          analysisId,
          token
        );

      if (cancelled) {
        return;
      }

      setAnalysisStatus(status);

      if (
  status.status === "completed"
) {
  navigate(
    `/resume-analysis/${analysisId}`
  );

  return;
}

      if (
        status.status === "failed"
      ) {
        setAnalysisError(
          status.error_message ||
            "Resume analysis failed."
        );

        return;
      }

      timeoutId = setTimeout(
        pollAnalysis,
        1500
      );

    } catch (err) {
      if (!cancelled) {
        console.error(
          "Failed to fetch analysis status:",
          err
        );

        setAnalysisError(
          "Unable to check analysis progress."
        );
      }
    }
  };

  pollAnalysis();

  return () => {
    cancelled = true;

    if (timeoutId) {
      clearTimeout(timeoutId);
    }
  };
}, [analysisId, token]);

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
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }

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
  const handleStartAnalysis = async () => {
    setAnalysisError("");

    if (!analysisResumeId) {
      setAnalysisError(
        "Please select a resume to evaluate."
      );
      return;
    }

    if (
      !jobDescription.trim() &&
      !jobDescriptionFile
    ) {
      setAnalysisError(
        "Please provide a job description."
      );
      return;
    }

    try {
      setAnalysisLoading(true);

      const result = await startResumeAnalysis({
        resumeId: analysisResumeId,
        jobDescription,
        jobDescriptionFile,
        token,
      });

      setAnalysisId(result.analysis_id);

      setAnalysisStatus(result);

    } catch (err) {
      console.error(
        "Failed to start resume analysis:",
        err
      );

      setAnalysisError(
        err?.response?.data?.detail ||
          "Failed to start resume analysis."
      );
    } finally {
      setAnalysisLoading(false);
    }
  };

  const latestResumeId = resumes.length
    ? resumes.reduce((latest, resume) =>
        new Date(resume.created_at) > new Date(latest.created_at) ? resume : latest
      ).id
    : null;

  return (
    <>
      <section className="resume-section">
        <div className="section-header">
          <div className="eyebrow">YOUR RESUME</div>
          <h1>This is what grounds your interview</h1>
          <p>Every question HotSeat generates is built from the resume you upload here.</p>
        </div>

        <div className="dropzone">
          <div className="dropzone__text">
            <div className="dropzone__label">DROP A PDF OR BROWSE</div>
            <div className="dropzone__hint">PDF only, up to 10MB</div>
            {selectedFile && (
              <div className="file-preview">
                Selected file: <strong>{selectedFile.name}</strong>
              </div>
            )}
          </div>
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            hidden
          />
          <button
            type="button"
            className="button button--secondary"
            onClick={() => fileInputRef.current?.click()}
          >
            Choose file
          </button>
          <button
            type="button"
            className="button button--primary"
            onClick={handleUpload}
            disabled={loading || !selectedFile}
          >
            {loading ? "Uploading..." : "Upload resume"}
          </button>
        </div>

        {success && <p className="success-text">{success}</p>}
        {error && <p className="error-text">{error}</p>}

        <div className="resume-list">
          {fetchingResumes ? (
            <p className="form-hint">Loading resumes...</p>
          ) : resumes.length === 0 ? (
            <p className="empty-state">No resumes uploaded yet.</p>
          ) : (
            resumes.map((resume) => (
              <div className="resume-list__item" key={resume.id}>
                <div className="resume-list__info">
                  <div className="resume-list__name">{resume.original_filename}</div>
                  <div className="resume-list__date">
                    Uploaded {new Date(resume.created_at).toLocaleString()}
                  </div>
                </div>
                {resume.id === latestResumeId && (
                  <span className="difficulty-pill">Active</span>
                )}
                <button
                  type="button"
                  className="resume-list__delete"
                  title="Delete resume"
                  disabled={deletingResumeId === resume.id}
                  onClick={() => handleDelete(resume)}
                >
                  {deletingResumeId === resume.id ? "…" : <FaTrash />}
                </button>
              </div>
            ))
          )}
        </div>
      </section>

      <section className="resume-section">
        <div className="section-header">
          <div className="eyebrow">RESUME INTELLIGENCE</div>
          <h2>Check your resume against a job description</h2>
          <p>See what you already cover, what's missing, and what to fix before you apply.</p>
        </div>

        <div className="analysis-form-card">
          <label className="form-field">
            <span>Resume to evaluate</span>
            <select
              value={analysisResumeId}
              onChange={(event) => setAnalysisResumeId(event.target.value)}
              disabled={fetchingResumes || resumes.length === 0 || analysisLoading}
            >
              <option value="">Select a resume</option>
              {resumes.map((resume) => (
                <option key={resume.id} value={resume.id}>
                  {resume.original_filename}
                </option>
              ))}
            </select>
          </label>

          <label className="form-field">
            <span>Job description</span>
            <textarea
              value={jobDescription}
              onChange={(event) => {
                setJobDescription(event.target.value);
                if (event.target.value.trim()) {
                  setJobDescriptionFile(null);
                }
              }}
              placeholder="Paste the complete job description here..."
              rows={6}
              disabled={analysisLoading}
            />
          </label>

          <div className="jd-file-row">
            <span className="form-hint">or upload the job description as PDF / image</span>
            <label className="button button--ghost jd-file-row__button">
              Choose file
              <input
                type="file"
                accept=".pdf,.png,.jpg,.jpeg,.webp"
                hidden
                onChange={(event) => {
                  const file = event.target.files?.[0];

                  if (!file) {
                    return;
                  }

                  const allowedTypes = [
                    "application/pdf",
                    "image/png",
                    "image/jpeg",
                    "image/webp",
                  ];

                  if (!allowedTypes.includes(file.type)) {
                    setAnalysisError("Please upload a PDF, PNG, JPG or WEBP file.");
                    event.target.value = "";
                    return;
                  }

                  setAnalysisError("");
                  setJobDescriptionFile(file);
                  setJobDescription("");
                }}
                disabled={analysisLoading}
              />
            </label>
          </div>

          {jobDescriptionFile && (
            <p className="file-preview">
              Selected JD: <strong>{jobDescriptionFile.name}</strong>
            </p>
          )}

          {analysisError && <p className="error-text">{analysisError}</p>}

          <button
            type="button"
            className="button button--primary button--lg button--wide"
            onClick={handleStartAnalysis}
            disabled={
              analysisLoading ||
              !analysisResumeId ||
              (!jobDescription.trim() && !jobDescriptionFile)
            }
          >
            {analysisLoading ? "Starting analysis..." : "Analyze resume against JD"}
          </button>
        </div>

        {analysisStatus?.status === "processing" && (
          <AnalysisProgress
            progress={analysisStatus.progress}
            currentStage={analysisStatus.current_stage}
          />
        )}
      </section>
    </>
  );
}

export default ResumeUploadCard;
