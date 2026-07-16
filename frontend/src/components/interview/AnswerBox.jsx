import { useState } from "react";
import { submitAnswer } from "../../api/answerApi";
import useAuth from "../../hooks/useAuth";

function AnswerBox({
  questionId,
  onAnswerSubmitted,
  disabled = false,
}) {
  const { token } = useAuth();

  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (disabled) return;

    if (!answer.trim()) {
      setError("Please enter an answer.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const response = await submitAnswer(
        {
          question_id: questionId,
          answer: answer.trim(),
        },
        token
      );

      onAnswerSubmitted(response);

      // Clear textbox after successful submission
      setAnswer("");
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
    <form className="content-card answer-box" onSubmit={handleSubmit}>
      <label className="form-field">
        <span>Your Answer</span>

        <textarea
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          rows={8}
          disabled={disabled}
          placeholder={
            disabled
              ? "This question has already been answered."
              : "Write your answer..."
          }
        />
      </label>

      {error && <p className="error-text">{error}</p>}

      <button
        className="button button--primary"
        type="submit"
        disabled={loading || disabled}
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