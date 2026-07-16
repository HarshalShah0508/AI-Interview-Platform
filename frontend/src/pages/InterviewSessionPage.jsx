import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { getInterviewSession } from "../api/interviewApi";
import useAuth from "../hooks/useAuth";

import QuestionCard from "../components/interview/QuestionCard";
import AnswerBox from "../components/interview/AnswerBox";
import FeedbackCard from "../components/interview/FeedbackCard";

function InterviewSessionPage() {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const { token } = useAuth();

  const [session, setSession] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [answeredQuestions, setAnsweredQuestions] = useState(new Set());
  const [feedbackMap, setFeedbackMap] = useState({});

  useEffect(() => {
    const fetchSession = async () => {
      try {
        setLoading(true);

        const data = await getInterviewSession(sessionId, token);

        setSession(data);

        const answered = new Set();
        const feedbacks = {};

        data.questions.forEach((question) => {
          if (question.answered) {
            answered.add(question.id);

            feedbacks[question.id] = {
              score: question.score,
              feedback: question.feedback,
              strengths: question.strengths,
              improvements: question.improvements,
            };
          }
        });

        setAnsweredQuestions(answered);
        setFeedbackMap(feedbacks);

        const firstUnanswered = data.questions.findIndex(
          (q) => !q.answered
        );

        if (firstUnanswered !== -1) {
          setCurrentQuestionIndex(firstUnanswered);
        }
      } catch (err) {
        setError(
          err?.response?.data?.detail ||
            "Failed to load interview session."
        );
      } finally {
        setLoading(false);
      }
    };

    if (token) {
      fetchSession();
    }
  }, [sessionId, token]);

  if (loading) {
    return (
      <section className="page-shell">
        <p>Loading interview...</p>
      </section>
    );
  }

  if (error) {
    return (
      <section className="page-shell">
        <p className="error-text">{error}</p>
      </section>
    );
  }

  const currentQuestion = session.questions[currentQuestionIndex];
  const currentFeedback = feedbackMap[currentQuestion.id];

  const handleAnswerSubmitted = (response) => {
    setFeedbackMap((prev) => ({
      ...prev,
      [currentQuestion.id]: response,
    }));

    setAnsweredQuestions((prev) => {
      const updated = new Set(prev);
      updated.add(currentQuestion.id);
      return updated;
    });
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex((prev) => prev - 1);
    }
  };

  const handleNext = () => {
    if (currentQuestionIndex < session.questions.length - 1) {
      setCurrentQuestionIndex((prev) => prev + 1);
    }
  };

  const handleFinishInterview = () => {
    const unanswered =
      session.questions.length - answeredQuestions.size;

    if (unanswered > 0) {
      const confirmFinish = window.confirm(
        `You still have ${unanswered} unanswered question(s).\n\nDo you want to finish the interview?`
      );

      if (!confirmFinish) return;
    }

    navigate(`/results/${sessionId}`);
  };

  return (
    <section className="page-shell">
      <div className="page-header">
        <p className="eyebrow">Practice Session</p>

        <h1>
          {session.role} • {session.difficulty}
        </h1>

        <p>
          Question {currentQuestionIndex + 1} of{" "}
          {session.questions.length}
        </p>
      </div>

      <div className="interview-workspace">
        <QuestionCard
          questionNumber={currentQuestionIndex + 1}
          questionText={currentQuestion.question_text}
        />

        <AnswerBox
          key={currentQuestion.id}
          questionId={currentQuestion.id}
          disabled={answeredQuestions.has(currentQuestion.id)}
          onAnswerSubmitted={handleAnswerSubmitted}
        />

        {currentFeedback && (
          <FeedbackCard {...currentFeedback} />
        )}

        <div className="page-actions">
          <button
            className="button button--secondary"
            onClick={handlePrevious}
            disabled={currentQuestionIndex === 0}
          >
            Previous
          </button>

          {currentQuestionIndex < session.questions.length - 1 ? (
            <button
              className="button button--secondary"
              onClick={handleNext}
            >
              Next / Skip
            </button>
          ) : (
            <button
              className="button button--primary"
              onClick={handleFinishInterview}
            >
              Finish Interview
            </button>
          )}
        </div>
      </div>
    </section>
  );
}

export default InterviewSessionPage;