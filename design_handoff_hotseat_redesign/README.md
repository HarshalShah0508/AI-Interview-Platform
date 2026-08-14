# Handoff: HotSeat Frontend Redesign

## Overview
A complete visual redesign of the HotSeat AI interview-prep platform (React + Vite + FastAPI). Covers the public landing page plus every authenticated screen: auth, dashboard, resume management, resume↔JD analysis, interview configuration, the live interview workspace, session results, and history.

## About the Design Files
The files in `designs/` are **design references built as standalone HTML/CSS/JS prototypes** (Design Components) — they show the intended look, layout, copy, and states pixel-precisely, but they are **not production code to paste in**. The task is to **recreate these designs inside the existing React/Vite codebase**, using its existing component structure, routing (`react-router-dom`), state (Context/hooks), and API layer — not to import or iframe the HTML files.

Each `.dc.html` file is self-contained (open directly in a browser to view). All styling is inline (React-style objects in spirit) — read the `<script>` block in each file for exact style values.

## Fidelity
**High-fidelity.** Every screen has final colors (as CSS `oklch()` values), typography (exact font families/weights/sizes), spacing, and copy. Recreate pixel-precisely using the values below and in each file, translated into the codebase's existing CSS approach (the app currently uses global classes in `src/index.css` — either extend that stylesheet with new rules, or introduce CSS modules/styled-components if the team prefers; just stay consistent with whatever the codebase already does).

## ABSOLUTE constraint: backend and contracts are untouched
- Do **not** modify anything under `backend/`.
- Do **not** rename, add, or change any API route, request shape, or response shape.
- Every field referenced below (e.g. `dashboard.total_interviews`, `results.average_score`) is a **real field already returned by an existing endpoint** — wire the new UI to the existing `src/api/*.js` calls exactly as they exist today (see `## API mapping`). The sample values shown in the designs (names, scores, filenames) are illustrative placeholders — replace with the real data returned at runtime, loading/empty states included.
- Preserve all existing functional logic: JWT auth, Google OAuth, email verification, resume upload/parsing, Monaco code editor + execution, Web Speech API voice input, adaptive follow-up handling, combined-answer submission.

## Design tokens

### Typography
- Display / headings: **Space Grotesk** (500/600/700)
- Body / UI text: **Inter** (400/500/600/700)
- Technical labels, eyebrows, code, numeric stats: **JetBrains Mono** (500/600)
- Load via Google Fonts: `Space+Grotesk:wght@500;600;700`, `Inter:wght@400;500;600;700`, `JetBrains+Mono:wght@500;600`

### Color — dark app surfaces (all authenticated screens: auth, dashboard, resume, generate-interview, interview workspace, results, history)
| Token | Value | Use |
|---|---|---|
| `char` | `oklch(0.16 0.011 45)` | page background |
| `char-raised` | `oklch(0.21 0.013 45)` | cards, panels |
| `char-deeper` | `oklch(0.135 0.009 45)` | code/terminal surfaces, left auth panel |
| `char-elevated` | `oklch(0.245 0.018 42)` | dashboard hero CTA card |
| `char-border` | `oklch(0.31 0.015 45)` | all hairline borders |
| `char-text` | `oklch(0.94 0.006 70)` | primary text on dark |
| `char-text-soft` | `oklch(0.66 0.011 60)` | secondary text on dark |

### Color — light marketing surface (landing page only)
| Token | Value | Use |
|---|---|---|
| `paper` | `oklch(0.975 0.007 70)` | page background |
| `paper-raised` | `oklch(0.995 0.004 70)` | cards |
| `border` | `oklch(0.89 0.012 60)` | hairlines |
| `ink` | `oklch(0.24 0.02 50)` | primary text |
| `ink-soft` | `oklch(0.48 0.02 55)` | secondary text |

### Accent + status
| Token | Value | Use |
|---|---|---|
| `accent` | `oklch(0.64–0.66 0.19 35)` | primary CTAs, active/selected states, recording indicator, scores |
| `accent-soft` | `accent` at 10–14% alpha | pill/badge backgrounds |
| `green` | `oklch(0.5–0.68 0.13–0.14 150)` | "completed" / positive badges |
| `red` | `oklch(0.55–0.62 0.17–0.19 25)` | error states |
| `amber` | `oklch(0.75 0.14 75)` | "in progress" badges |

Radii: 3–4px on controls/buttons, 6–8px on cards. No large rounded-everything look. Borders are 1px hairlines, no heavy shadows on dark surfaces.

## Screens / Views

1. **Landing Page** (`Landing Page.dc.html`) — public marketing page, light theme. Nav, hero with a dark "session preview" mockup (question + code + recording state), 5-feature editorial loop (resume-tailored questions, adaptive follow-ups, voice/text/code hybrid, progress history, resume↔JD match analysis), 5-step "how it works", final CTA, footer.
2. **Authentication** (`Authentication.dc.html`) — Login, Signup, and Verify Email (success + error) stacked as three full sections. Split layout: dark editorial left panel (brand story + a small live-data preview card — session progress on login, resume/JD match on signup) + form on the right. Includes the "email not verified / resend" state as a red inline alert under the login form.
3. **Dashboard** (`Dashboard.dc.html`) — greeting, a slim stats strip (total/completed/in-progress interviews + latest resume filename — all real `/dashboard` fields, no invented metrics), a large accent-bordered "start interview" CTA card, quick links to resume/history, and a "most recent session" card.
4. **Resume** (`Resume.dc.html`) — three sections: resume upload/manage (dropzone + list with delete), resume↔JD analysis (resume select, JD textarea or file upload, analyze CTA, an in-progress state example with stage list), and past-analysis history list.
5. **Generate Interview** (`Generate Interview.dc.html`) — focused single-column setup form: resume select, role text input, difficulty as a 3-way segmented control, "Enter the HotSeat" CTA.
6. **Interview Workspace** (`Interview Workspace.dc.html`) — **highest priority screen**. Sticky top bar with question-progress dots + exit link. Question card with a follow-up banner variant. One unified "Your Answer" card containing Voice (transcript box + record/stop + recording indicator), Notes (textarea), and Code (mock Monaco surface, language pill, run button, stdin, console output) as three labeled sub-sections graded together, plus a muted combined-preview strip. Dark "previous question feedback" card (score, strengths, improvements). Sticky bottom action bar (Previous / Next-Skip / Submit).
7. **Session Results** (`Session Results.dc.html`) — average score (large numeral, not a gauge) + questions attempted, strong/weak topic pills, a question-by-question list (including a follow-up example), and dashboard/new-interview actions.
8. **History** (`History.dc.html`) — list of past sessions with role, difficulty, date, status badge (completed/in progress), average score, and Continue/View-results actions.

Open any `.dc.html` file directly in a browser to inspect exact spacing/markup; the inline `style` objects in the `<script>` section are the source of truth for pixel values.

## Interactions & Behavior to preserve
- Login/Signup forms: same validation and error surfaces as current `LoginForm.jsx`/`SignupForm.jsx` (inline error text, resend-verification flow on 403).
- Google OAuth button: keep `@react-oauth/google`'s `GoogleLogin` behavior; only the button chrome is restyled (custom wrapper with the standard 4-color "G" mark — see SVG in `Authentication.dc.html`).
- Voice input: keep the Web Speech API logic in `VoiceInput.jsx`; only the surrounding chrome (labels, recording badge/pulse, transcript box) is restyled.
- Code editor: keep Monaco (`CodeEditor.jsx`) exactly as-is; only the header/controls around it are restyled. Do not reskin Monaco's internal theme unless you also switch it to a dark Monaco theme (`vs-dark`) to match the new workspace — recommended, since the mock in the design shows a dark editor surface.
- Follow-up questions: when `question.is_follow_up` is true, use the accent-outlined "FOLLOW-UP" tag + banner shown in the design instead of the primary question chrome.
- Difficulty segmented control on Generate Interview replaces the native `<select>` — keep it wired to the same `difficulty` form field (Easy/Medium/Hard).
- All buttons/links map 1:1 to existing handlers (submit, run code, delete resume, resend verification, continue/finish interview, etc.) — this is a visual restyle, not a behavior change.

## State Management
No new state is required beyond what already exists in each page/component (`LoginForm`, `SignupForm`, `AnswerBox`, `InterviewSessionPage`, `ResumeUploadCard`, etc.). The only new bit of UI state is the segmented-control selection on Generate Interview.

## API mapping (existing endpoints — do not change)
| Screen | Endpoint(s) already used |
|---|---|
| Auth | `POST /signup`, `POST /login`, `POST /auth/google`, `GET /auth/verify-email`, `POST /auth/resend-verification` |
| Dashboard | `GET /dashboard` → `username, email, latest_resume, total_interviews, completed_interviews, in_progress_interviews, latest_interview{role,difficulty,created_at}` |
| Resume | `POST /resume/upload`, `GET /resume`, `DELETE /resume/{id}`, resume↔JD analysis endpoints in `resumeAnalysisApi.js` |
| Generate Interview | `POST /interview/generate-questions` |
| Interview Workspace | `GET /interview/{sessionId}`, `POST /answer`, code execution via `codeApi.js` |
| Session Results | `GET /answer/session/{sessionId}/results` → `average_score, questions_attempted, strong_topics[], weak_topics[]` (per-question breakdown shown in the design comes from the same per-question `score/feedback/strengths/improvements` already tracked in `InterviewSessionPage.jsx`) |
| History | `GET /interview/history` |

## Assets
No external image assets — the hero/feature "mockups" on the landing page and the code-editor mock in the workspace are hand-built with divs/text (no icon libraries beyond the existing `react-icons` already in the project for things like the delete/trash icon). The Google "G" mark is inlined as SVG in `Authentication.dc.html`.

## Files
All design references are in `designs/`:
- `Landing Page.dc.html`
- `Authentication.dc.html`
- `Dashboard.dc.html`
- `Resume.dc.html`
- `Generate Interview.dc.html`
- `Interview Workspace.dc.html`
- `Session Results.dc.html`
- `History.dc.html`
