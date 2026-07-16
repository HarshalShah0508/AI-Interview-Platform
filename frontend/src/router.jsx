import { createBrowserRouter } from "react-router-dom";
import App from "./App";
import ProtectedRoute from "./components/layout/ProtectedRoute";

import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import DashboardPage from "./pages/DashboardPage";
import ResumePage from "./pages/ResumePage";
import GenerateInterviewPage from "./pages/GenerateInterviewPage";
import InterviewSessionPage from "./pages/InterviewSessionPage";
import HistoryPage from "./pages/HistoryPage";
import SessionResultsPage from "./pages/SessionResultsPage";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { index: true, element: <LoginPage /> },
      { path: "login", element: <LoginPage /> },
      { path: "signup", element: <SignupPage /> },

      {
        path: "dashboard",
        element: (
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        ),
      },
      {
        path: "resume",
        element: (
          <ProtectedRoute>
            <ResumePage />
          </ProtectedRoute>
        ),
      },
      {
        path: "generate-interview",
        element: (
          <ProtectedRoute>
            <GenerateInterviewPage />
          </ProtectedRoute>
        ),
      },
      {
        path: "interview/:sessionId",
        element: (
          <ProtectedRoute>
            <InterviewSessionPage />
          </ProtectedRoute>
        ),
      },
      {
        path: "history",
        element: (
          <ProtectedRoute>
            <HistoryPage />
          </ProtectedRoute>
        ),
      },
      {
        path: "results/:sessionId",
        element: (
          <ProtectedRoute>
            <SessionResultsPage />
          </ProtectedRoute>
        ),
      },
    ],
  },
]);

export default router;