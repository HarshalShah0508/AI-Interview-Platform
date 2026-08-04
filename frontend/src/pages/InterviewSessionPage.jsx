import { useEffect, useState , useRef } from "react";
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
  const answerBoxRef = useRef(null);

  const [session, setSession] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [answeredQuestions, setAnsweredQuestions] = useState(new Set());
  const [feedbackMap, setFeedbackMap] = useState({});
  const [readyForNext, setReadyForNext] = useState(false);
  const [nextIsFollowUp, setNextIsFollowUp] =
  useState(false);

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
          (question) => !question.answered
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

  const currentQuestion =
    session.questions[currentQuestionIndex];

  const currentFeedback =
    feedbackMap[currentQuestion.id];

  const totalMainQuestions =
    session.questions.filter(
      (question) => !question.is_follow_up
    ).length;

  const currentMainQuestionNumber =
    session.questions
      .slice(0, currentQuestionIndex + 1)
      .filter(
        (question) => !question.is_follow_up
      ).length;
      const handleAnswerSubmitted = (response) => {
  setFeedbackMap((prev) => ({
    ...prev,
    [currentQuestion.id]: {
      score: response.score,
      feedback: response.feedback,
      strengths: response.strengths,
      improvements: response.improvements,
    },
  }));

  setAnsweredQuestions((prev) => {
    const updated = new Set(prev);
    updated.add(currentQuestion.id);
    return updated;
  });

  if (response.has_follow_up && response.follow_up) {
    setSession((prevSession) => {
      const updatedQuestions = [...prevSession.questions];

      updatedQuestions.splice(
        currentQuestionIndex + 1,
        0,
        {
          id: response.follow_up.question_id,
          question_text:
            response.follow_up.question_text,
          follow_up_depth:
            response.follow_up.follow_up_depth,
          is_follow_up: true,
          answered: false,
        }
      );

      return {
        ...prevSession,
        questions: updatedQuestions,
      };
    });
    setNextIsFollowUp(true);
  }else{
    setNextIsFollowUp(false);
  }

  setReadyForNext(true);
};

const handlePrevious = () => {
  if (currentQuestionIndex > 0) {

    setCurrentQuestionIndex((prev) => prev - 1);

    setReadyForNext(false);
    setNextIsFollowUp(false);

  }
};

const handleNext = () => {
  if (currentQuestionIndex < session.questions.length - 1) {

    setCurrentQuestionIndex((prev) => prev + 1);

    setReadyForNext(false);
    setNextIsFollowUp(false);

  }
};

const handleFinishInterview = () => {
  const unanswered =
    session.questions.length -
    answeredQuestions.size;

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

      <div className="question-progress">
        <p>
          Question {currentMainQuestionNumber} of{" "}
          {totalMainQuestions}
        </p>

        {currentQuestion.is_follow_up && (
          <div className="follow-up-banner">
            <strong>🔍 Follow-up Question</strong>

            <p>
              The interviewer wants to explore this topic
              in more depth based on your previous answer.
            </p>
          </div>
        )}
      </div>
      <div className="page-actions page-actions--top">

  <button
    className="button button--secondary"
    onClick={handlePrevious}
    disabled={currentQuestionIndex === 0}
  >
    ← Previous
  </button>

  <button
    className="button button--primary"
    onClick={() => answerBoxRef.current?.submit()}
    disabled={answeredQuestions.has(currentQuestion.id)}
  >
    Submit Answer
  </button>

  {currentQuestionIndex <
session.questions.length - 1 ? (

  readyForNext ? (

    <button
      className="button button--primary"
      onClick={handleNext}
    >
      {nextIsFollowUp
        ? "Continue to Follow-up →"
        : "Next Question →"}
    </button>

  ) : (

    <button
      className="button button--secondary"
      onClick={handleNext}
    >
      Next / Skip →
    </button>

  )

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

    <div className="interview-workspace">
      <QuestionCard
        questionNumber={currentMainQuestionNumber}
        questionText={currentQuestion.question_text}
        isFollowUp={currentQuestion.is_follow_up}
      />

      <AnswerBox
        ref={answerBoxRef}
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

  {currentQuestionIndex <
  session.questions.length - 1 ? (

    readyForNext ? (

      <button
        className="button button--primary"
        onClick={handleNext}
      >
        {session.questions[currentQuestionIndex + 1]
          ?.is_follow_up
          ? "Continue to Follow-up →"
          : "Next Question →"}
      </button>

    ) : (

      <button
        className="button button--secondary"
        onClick={handleNext}
      >
        Next / Skip
      </button>

    )

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