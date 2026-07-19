import { useState } from "react";

import { submitAnswer } from "../../api/answerApi";
import useAuth from "../../hooks/useAuth";

import VoiceInput from "./VoiceInput";
import NotesInput from "./NotesInput";
import CodeEditor from "./CodeEditor";
import CombinedPreview from "./CombinedPreview";

function AnswerBox({
  questionId,
  onAnswerSubmitted,
  disabled = false,
}) {
  const { token } = useAuth();

  const [voiceText, setVoiceText] = useState("");
  const [typedText, setTypedText] = useState("");
  const [code, setCode] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const hasContent =
    voiceText.trim() ||
    typedText.trim() ||
    code.trim();

  const handleSubmit = async (event) => {
    event.preventDefault();

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

      onAnswerSubmitted(response);

      setVoiceText("");
      setTypedText("");
      setCode("");
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
          "Failed to submit answer."
      );
    } finally {
      setLoading(false);
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

      <CodeEditor
        value={code}
        onChange={setCode}
        disabled={disabled}
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
    </form>
  );
}

export default AnswerBox;