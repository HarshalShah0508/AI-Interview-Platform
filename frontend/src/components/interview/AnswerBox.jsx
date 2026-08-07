import {
  useState,
  forwardRef,
  useImperativeHandle,
} from "react";

import { submitAnswer } from "../../api/answerApi";
import useAuth from "../../hooks/useAuth";
import { runCode } from "../../api/codeApi";
import VoiceInput from "./VoiceInput";
import NotesInput from "./NotesInput";
import CodeEditor from "./CodeEditor";
import CombinedPreview from "./CombinedPreview";
import LanguageSelector from "./LanguageSelector";
import ConsoleOutput from "./ConsoleOutput";
import CustomInput from "./CustomInput";

import {
  PROGRAMMING_LANGUAGES,
  DEFAULT_LANGUAGE,
} from "../../constants/programmingLanguages";

const AnswerBox = forwardRef(function AnswerBox(
  {
    questionId,
    onAnswerSubmitted,
    disabled = false,
  },
  ref
) {
  const { token } = useAuth();

  const [voiceText, setVoiceText] = useState("");
  const [typedText, setTypedText] = useState("");
  const [code, setCode] = useState("");

  const [customInput, setCustomInput] = useState("");

  const [consoleOutput, setConsoleOutput] =
    useState("");

  const [executionStatus, setExecutionStatus] =
    useState("idle");

  const [selectedLanguage, setSelectedLanguage] =
    useState(DEFAULT_LANGUAGE);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const hasContent =
    voiceText.trim() ||
    typedText.trim() ||
    code.trim();

  const handleRunCode = async () => {
    if (executionStatus === "running") {
      return;
    }
    setError("");
    if (!code.trim()) {
      setExecutionStatus("idle");
      setConsoleOutput("Please write some code first.");
      return;
  }

  try {
    setExecutionStatus("running");
    setConsoleOutput("");

    const response = await runCode(
      {
        language: selectedLanguage.id,
        code,
        stdin: customInput,
      },
      token
    );

    setExecutionStatus(response.status);

    let output = "";

    if (response.stdout) {
      output += response.stdout;
    }

    if (response.stderr) {
      if (output) {
        output += "\n\n";
      }

      output += response.stderr;
    }

    if (output.trim()==="") {
      output = "Program executed successfully.";
    }

    setConsoleOutput(output);

  } catch (error) {

    setExecutionStatus("internal_error");

    setConsoleOutput(
      error?.response?.data?.detail ||
      error.message ||
      "Failed to execute code."
    );

  }
};

  const handleSubmit = async (event) => {
    if (event) event.preventDefault();

    if (disabled) return;

    if (!hasContent) {
      setError(
        "Please provide a voice explanation, notes or code."
      );
      return;
    }

    try {
      setLoading(true);
      setError("");

      const response = await submitAnswer(
        {
          question_id: questionId,
          voice_text: voiceText.trim(),
          typed_text: typedText.trim(),
          code: code.trim(),
        },
        token
      );

      setVoiceText("");
      setTypedText("");
      setCode("");
      setCustomInput("");
      setConsoleOutput("");
      setExecutionStatus("idle");
      setSelectedLanguage(DEFAULT_LANGUAGE);

      onAnswerSubmitted(response);

    } catch (err) {

      setError(
        err?.response?.data?.detail ||
        "Failed to submit answer."
      );

    } finally {

      setLoading(false);

    }
  };

  useImperativeHandle(ref, () => ({
    submit: () => handleSubmit(),
  }));

  const handleLanguageChange = (languageId) => {
    const language =
      PROGRAMMING_LANGUAGES.find(
        (lang) => lang.id === languageId
      );

    if (language) {
      setSelectedLanguage(language);
    }
  };

  return (
    <form
      className="answer-box"
      onSubmit={handleSubmit}
    >
      <VoiceInput
        value={voiceText}
        onChange={setVoiceText}
        disabled={disabled}
      />

      <NotesInput
        value={typedText}
        onChange={setTypedText}
        disabled={disabled}
      />

      <LanguageSelector
        languages={PROGRAMMING_LANGUAGES}
        selectedLanguage={selectedLanguage}
        onLanguageChange={handleLanguageChange}
      />

      <CodeEditor
        value={code}
        onChange={setCode}
        language={selectedLanguage}
        disabled={disabled}
        onRunCode={handleRunCode}
        isRunning={executionStatus === "running"}
      />

      <CustomInput
        value={customInput}
        onChange={setCustomInput}
        disabled={disabled}
      />

      <ConsoleOutput
        output={consoleOutput}
        status={executionStatus}
      />

      <CombinedPreview
        voiceText={voiceText}
        typedText={typedText}
        code={code}
      />

      {error && (
        <p className="error-text">
          {error}
        </p>
      )}

      <div
        style={{
        display: "flex",
        justifyContent: "flex-end",
        marginTop: "16px",
      }}
>
      <button
        className="button button--primary"
        type="submit"
        disabled={
          loading ||
          disabled ||
          !hasContent
        }
  >
        {disabled
          ? "Already Submitted"
          : loading
          ? "Submitting..."
          : "Submit Answer"}
      </button>
</div>
    </form>
  );
});

export default AnswerBox;