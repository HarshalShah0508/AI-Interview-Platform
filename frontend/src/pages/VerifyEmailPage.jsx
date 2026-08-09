import { useEffect, useState } from "react";
import { useSearchParams, Link } from "react-router-dom";
import apiClient from "../api/client";

function VerifyEmailPage() {
  const [searchParams] = useSearchParams();

  const [status, setStatus] = useState("loading");

  const [message, setMessage] = useState("");

  useEffect(() => {
    const token = searchParams.get("token");

    if (!token) {
      setStatus("error");
      setMessage("Invalid verification link.");
      return;
    }

    async function verifyEmail() {
      try {
        const response = await apiClient.get(
          `/auth/verify-email?token=${token}`
        );

        setStatus("success");
        setMessage(response.data.message);
      } catch (error) {
        setStatus("error");

        setMessage(
          error.response?.data?.detail ||
          "Unable to verify email."
        );
      }
    }

    verifyEmail();

  }, [searchParams]);

  return (
    <div className="auth-page">

      <div className="auth-card">

        {status === "loading" && (
          <>
            <h2>Verifying Email...</h2>
            <p>Please wait.</p>
          </>
        )}

        {status === "success" && (
          <>
            <h2>✅ Email Verified</h2>

            <p>{message}</p>

            <Link
              to="/login"
              className="button button--primary"
            >
              Go to Login
            </Link>
          </>
        )}

        {status === "error" && (
          <>
            <h2>❌ Verification Failed</h2>

            <p>{message}</p>

            <Link
              to="/signup"
              className="button button--primary"
            >
              Back to Signup
            </Link>
          </>
        )}

      </div>

    </div>
  );
}

export default VerifyEmailPage;