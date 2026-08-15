import { useContext } from "react";
import ResumeAnalysisContext from "../context/ResumeAnalysisContext";

const useResumeAnalysis = () => useContext(ResumeAnalysisContext);

export default useResumeAnalysis;
