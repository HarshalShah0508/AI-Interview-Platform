import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import {
  getResumeAnalysisResult,
} from "../api/resumeAnalysisApi";

import MatchOverview from "../components/resume-analysis/MatchOverview";
import RequirementMatches from "../components/resume-analysis/RequirementMatches";
import ResumeRecommendations from "../components/resume-analysis/ResumeRecommendations";
import KeepAsIs from "../components/resume-analysis/KeepAsIs";
import MissingRequirements from "../components/resume-analysis/MissingRequirements";

export default function ResumeAnalysisPage() {
  const { analysisId } =
    useParams();

  const [analysis, setAnalysis] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  useEffect(() => {
    const loadResult = async () => {
      try {
        const token =
          localStorage.getItem("token");

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
  }, [analysisId]);

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

      <MatchOverview
        score={analysis.overall_score}
        matchingReport={
          result.matching_report
        }
      />

      <RequirementMatches
        matches={
          result.matching_report.matches
        }
      />

      <ResumeRecommendations
        recommendations={
          result.recommendation_report
            .recommendations
        }
      />

      <MissingRequirements
        requirements={
          result.recommendation_report
            .missing_requirement_actions
        }
      />

      <KeepAsIs
        items={
          result.recommendation_report
            .keep_as_is
        }
      />

    </main>
  );
}