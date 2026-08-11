import { useEffect, useState } from "react";
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
      <div className="resume-analysis-section">
  <div className="resume-analysis-header">
    <div>
      <h3>
        Evaluate your resume against a Job Description
      </h3>

      <p>
        Select one of your resumes and compare it
        against a specific job description to see
        what matches, what is missing, and what
        you can improve.
      </p>
    </div>
  </div>

  <div className="resume-analysis-form">

    <label className="form-field">
      <span>
        Select resume to evaluate
      </span>

      <select
        value={analysisResumeId}
        onChange={(event) =>
          setAnalysisResumeId(
            event.target.value
          )
        }
        disabled={
          fetchingResumes ||
          resumes.length === 0 ||
          analysisLoading
        }
      >
        <option value="">
          Select a resume
        </option>

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


    <div className="form-field">
      <span>
        Job Description
      </span>

      <textarea
        value={jobDescription}
        onChange={(event) => {
          setJobDescription(
            event.target.value
          );

          if (event.target.value.trim()) {
            setJobDescriptionFile(null);
          }
        }}
        placeholder={
          "Paste the complete job description here..."
        }
        rows={10}
        disabled={analysisLoading}
      />
    </div>


    <div className="jd-file-option">
      <span>
        Or upload the Job Description
      </span>

      <input
        type="file"
        accept=".pdf,.png,.jpg,.jpeg,.webp"
        onChange={(event) => {
          const file =
            event.target.files?.[0];

          if (!file) {
            return;
          }

          const allowedTypes = [
            "application/pdf",
            "image/png",
            "image/jpeg",
            "image/webp",
          ];

          if (
            !allowedTypes.includes(
              file.type
            )
          ) {
            setAnalysisError(
              "Please upload a PDF, PNG, JPG or WEBP file."
            );

            event.target.value = "";

            return;
          }

          setAnalysisError("");

          setJobDescriptionFile(file);

          setJobDescription("");
        }}
        disabled={analysisLoading}
      />

      {jobDescriptionFile && (
        <p className="file-preview">
          Selected JD:
          <strong>
            {" "}
            {jobDescriptionFile.name}
          </strong>
        </p>
      )}
    </div>


    {analysisError && (
      <p className="error-text">
        {analysisError}
      </p>
    )}


    <button
      className="button button--primary"
      type="button"
      onClick={handleStartAnalysis}
      disabled={
        analysisLoading ||
        !analysisResumeId ||
        (
          !jobDescription.trim() &&
          !jobDescriptionFile
        )
      }
    >
      {analysisLoading
        ? "Starting analysis..."
        : "Analyze Resume Against JD"}
    </button>

  </div>


  {analysisStatus?.status ===
    "processing" && (
    <AnalysisProgress
      progress={
        analysisStatus.progress
      }
      currentStage={
        analysisStatus.current_stage
      }
    />
  )}

</div>
    </div>
  );
}

export default ResumeUploadCard;