const STORAGE_KEY = "hotseat.resumeJdAnalysis.v1";

export function loadResumeAnalysisState() {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function saveResumeAnalysisState(state) {
  try {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch {
    // sessionStorage unavailable (private mode / quota) - in-memory state still works
  }
}

export function clearResumeAnalysisState() {
  try {
    sessionStorage.removeItem(STORAGE_KEY);
  } catch {
    // ignore
  }
}
