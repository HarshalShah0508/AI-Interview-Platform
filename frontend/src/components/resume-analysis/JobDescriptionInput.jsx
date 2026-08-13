import { useRef, useState } from "react";

export default function JobDescriptionInput({
  value,
  onChange,
  file,
  onFileChange,
}) {
  const fileInputRef = useRef(null);

  const [mode, setMode] = useState("text");

  const handleFileChange = (event) => {
    const selectedFile =
      event.target.files?.[0];

    if (!selectedFile) {
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
        selectedFile.type
      )
    ) {
      alert(
        "Please upload a PDF, PNG, JPG or WEBP file."
      );

      event.target.value = "";
      return;
    }

    onFileChange(selectedFile);
  };

  const clearFile = () => {
    onFileChange(null);

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="jd-input">
      <div className="jd-input-header">
        <div>
          <h3>Job Description</h3>

          <p>
            Paste the JD or upload it as a PDF/image.
          </p>
        </div>

        <div className="jd-mode-switch">
          <button
            type="button"
            className={
              mode === "text"
                ? "active"
                : ""
            }
            onClick={() => {
              setMode("text");
              clearFile();
            }}
          >
            Paste Text
          </button>

          <button
            type="button"
            className={
              mode === "file"
                ? "active"
                : ""
            }
            onClick={() => {
              setMode("file");
              onChange("");
            }}
          >
            Upload
          </button>
        </div>
      </div>

      {mode === "text" ? (
        <textarea
          value={value}
          onChange={(event) =>
            onChange(event.target.value)
          }
          placeholder={
            "Paste the complete job description here..."
          }
          rows={14}
        />
      ) : (
        <div className="jd-file-upload">
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.png,.jpg,.jpeg,.webp"
            onChange={handleFileChange}
            hidden
          />

          {!file ? (
            <button
              type="button"
              onClick={() =>
                fileInputRef.current?.click()
              }
            >
              Upload Job Description
            </button>
          ) : (
            <div className="selected-jd-file">
              <div>
                <strong>
                  {file.name}
                </strong>

                <span>
                  {(file.size / 1024 / 1024).toFixed(
                    2
                  )}{" "}
                  MB
                </span>
              </div>

              <button
                type="button"
                onClick={clearFile}
              >
                Remove
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}