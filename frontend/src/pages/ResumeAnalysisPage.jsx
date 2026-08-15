import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import {
  getResumeAnalysisResult,
} from "../api/resumeAnalysisApi";
import useAuth from "../hooks/useAuth";

import AnalysisTabs from "../components/resume-analysis/AnalysisTabs";
import AnalysisSummary from "../components/resume-analysis/AnalysisSummary";
import RequirementTable from "../components/resume-analysis/RequirementTable";
import ImprovementTable from "../components/resume-analysis/ImprovementTable";
import ReviewAreasTable from "../components/resume-analysis/ReviewAreasTable";

const TABS = [
  { id: "overview", label: "Overview" },
  { id: "requirements", label: "Requirements" },
  { id: "improvements", label: "Improvements" },
  { id: "review", label: "Review Areas" },
];

export default function ResumeAnalysisPage() {
  const { analysisId } =
    useParams();

  const [analysis, setAnalysis] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const [activeTab, setActiveTab] =
    useState("overview");

  const { token } = useAuth();

  useEffect(() => {
    if (!token) {
      return;
    }

    const loadResult = async () => {
      try {
        const result =
          await getResumeAnalysisResult(
            analysisId,
            token
          );

        setAnalysis(result);

      } catch (err) {
        console.error(
          "Failed to load analysis:",
          err
        );

        setError(
          err?.response?.data?.detail ||
            "Unable to load analysis."
        );

      } finally {
        setLoading(false);
      }
    };

    loadResult();
  }, [analysisId, token]);

  if (loading) {
    return (
      <div className="analysis-loading">
        Loading analysis...
      </div>
    );
  }

  if (error) {
    return (
      <div className="analysis-error">
        {error}
      </div>
    );
  }

  if (!analysis) {
    return null;
  }

  const result =
    analysis.result;

  const matchingReport =
    result.matching_report;

  const recommendationReport =
    result.recommendation_report;

  const missingAndReviewCount =
    (matchingReport?.summary?.missing_matches ?? 0) +
    (matchingReport?.summary?.ambiguous_matches ?? 0);

  const tabs = TABS.map((tab) => {

    if (tab.id === "requirements") {
      return {
        ...tab,
        count: matchingReport?.matches?.length ?? 0,
      };
    }

    if (tab.id === "improvements") {
      return {
        ...tab,
        count: recommendationReport?.recommendations?.length ?? 0,
      };
    }

    if (tab.id === "review") {
      return {
        ...tab,
        count: missingAndReviewCount,
      };
    }

    return tab;
  });

  return (
    <main className="resume-analysis-page">

      <section className="analysis-header">
        <div>
          <span>
            Resume Intelligence
          </span>

          <h1>
            {analysis.job_title ||
              "Resume Analysis"}
          </h1>

          <p>
            Evidence-backed analysis of your
            resume against this job description.
          </p>
        </div>
      </section>

      <AnalysisTabs
        tabs={tabs}
        activeTab={activeTab}
        onChange={setActiveTab}
      />

      {activeTab === "overview" && (
        <AnalysisSummary
          score={analysis.overall_score}
          matchingReport={matchingReport}
        />
      )}

      {activeTab === "requirements" && (
        <RequirementTable
          matches={matchingReport?.matches}
          partialMatchGuidance={
            recommendationReport?.partial_match_guidance
          }
        />
      )}

      {activeTab === "improvements" && (
        <ImprovementTable
          recommendations={
            recommendationReport?.recommendations
          }
          keepAsIs={
            recommendationReport?.keep_as_is
          }
        />
      )}

      {activeTab === "review" && (
        <ReviewAreasTable
          matches={matchingReport?.matches}
          missingActions={
            recommendationReport?.missing_requirement_actions
          }
        />
      )}

    </main>
  );
}
