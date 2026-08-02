# 🚀 Hot Seat – Product Roadmap

This document outlines the planned roadmap for transforming **Hot Seat** from a portfolio project into a production-ready AI Interview Platform suitable for real users, coaching institutes, placement cells, and enterprise customers.

---

# Current Status

## Completed Features

- ✅ JWT Authentication
- ✅ Resume Upload & Parsing
- ✅ Resume Management (Upload & Delete)
- ✅ AI Interview Generation
- ✅ Multi-Domain Interviews
- ✅ AI Answer Evaluation
- ✅ Voice + Text + Code Hybrid Interview
- ✅ PostgreSQL Migration
- ✅ Dockerization
- ✅ Modular Prompt Architecture
- ✅ Public Deployment

---

# Sprint 1 – Core Experience

The objective of Sprint 1 is to improve the quality and reliability of the interview experience.

---

## 1. Prompt Optimization ⭐⭐⭐⭐⭐

### Why?

The quality of every interview depends on the AI prompt.

Current Issues

- Multiple questions generated together.
- Inconsistent formatting.
- Uneven difficulty.
- Generic questions.
- Limited control over interview flow.

### Goals

- Generate exactly one question at a time.
- Maintain consistent formatting.
- Improve question quality.
- Separate Resume, Technical, Coding, Behavioral, and System Design prompts.
- Store interview context for future adaptive interviews.
- Improve evaluation consistency.

Expected Impact

High

---

## 2. Voice Pipeline Improvements ⭐⭐⭐⭐⭐

### Why?

Incorrect speech recognition negatively affects AI evaluation.

Current Issues

- Incorrect words.
- Grammar-related feedback caused by transcription errors.
- Poor punctuation.
- User cannot verify transcript.

### Goals

- Improve speech recognition.
- Normalize transcript before evaluation.
- Restore punctuation.
- Improve capitalization.
- Allow transcript editing before submission.
- Send cleaned transcript to Gemini.

Expected Impact

Very High

---

## 3. Code Execution Environment ⭐⭐⭐⭐⭐

### Why?

Coding interviews should behave like real technical interviews.

Current Limitations

- Code editor only.
- No execution.
- No test cases.
- Single language.

### Goals

- Monaco Editor.
- Multiple programming languages.
- Compile & Run.
- Custom test cases.
- Hidden test cases.
- Runtime output.
- Error messages.
- AI code review.

Expected Impact

Very High

---

## 4. UI/UX Improvements ⭐⭐⭐⭐☆

### Why?

A polished interface improves usability and user retention.

Goals

- Better dashboard.
- Cleaner interview interface.
- Progress indicator.
- Timer.
- Better feedback cards.
- Responsive design.
- Dark mode.
- Improved loading states.
- Better animations.

Expected Impact

High

---

# Sprint 2 – Intelligent Interviews

The objective is to make interviews feel like conversations with a real interviewer.

---

## 5. Context-Aware Follow-Up Questions ⭐⭐⭐⭐⭐

### Why?

Real interviewers ask follow-up questions based on candidate responses.

Goals

- Generate one follow-up question.
- Maintain interview context.
- Avoid repeated questions.
- Probe deeper into weak answers.
- Ask advanced questions for strong candidates.

Expected Impact

Extremely High

---

## 6. Adaptive AI Interviewer ⭐⭐⭐⭐⭐

### Why?

Move from static interview generation to a dynamic AI interviewer.

Current

Generate all questions upfront.

Future

Generate questions dynamically based on interview progress.

Goals

- AI controls interview flow.
- Dynamic topic switching.
- Adaptive difficulty.
- Multiple follow-up levels.
- Interview memory.
- Human-like conversation.

Expected Impact

Game-Changing

---

# Sprint 3 – Product Differentiators

---

## 7. Company-Specific Interview Packs

Examples

- Google
- Amazon
- Microsoft
- Atlassian
- Uber
- Goldman Sachs
- JPMorgan
- McKinsey
- BCG

Goals

Generate company-specific interviews based on known interview styles.

Expected Impact

Very High

---

## 8. Resume AI Review

Goals

- Resume score.
- ATS score.
- Grammar suggestions.
- Content improvements.
- Missing keywords.
- Project recommendations.

Expected Impact

High

---

## 9. Analytics Dashboard

Goals

Track

- Overall score
- Coding score
- Communication score
- Technical score
- Behavioral score
- Improvement over time

Expected Impact

High

---

## 10. Interview Report

Generate downloadable reports containing

- Questions
- Answers
- Scores
- Feedback
- Learning roadmap
- Improvement areas

Expected Impact

High

---

# Sprint 4 – Authentication & Security

---

## 11. Google OAuth

Goals

- Sign in with Google.
- Account linking.
- Secure authentication.

---

## 12. Email Verification

Goals

- Verify user email.
- Prevent fake registrations.

---

## 13. Forgot Password

Goals

- Password reset email.
- Secure reset token.

---

# Sprint 5 – Production Readiness

---

## 14. Notifications

Examples

- Interview reminders
- Weekly reports
- Practice streaks

---

## 15. Performance Optimization

Goals

- Faster APIs.
- Better caching.
- Optimized prompts.
- Reduced Gemini latency.

---

## 16. Logging & Monitoring

Goals

- Centralized logs.
- Error tracking.
- API monitoring.
- Usage analytics.

---

# Sprint 6 – Cloud Infrastructure

This sprint should be completed **last**, after the product is stable.

---

## 17. Cloud Storage Migration ⭐⭐⭐⭐⭐

### Why?

Currently, resumes are stored on the backend server.

This is not suitable for production because:

- Files may be lost during redeployment.
- Scaling becomes difficult.
- Local storage is not shared across instances.

### Goals

Store uploaded resumes using cloud object storage.

Possible Providers

- AWS S3
- Google Cloud Storage
- Azure Blob Storage
- Cloudinary (documents)
- Supabase Storage

Features

- Secure uploads.
- Secure downloads.
- Resume deletion.
- Signed URLs.
- Scalable storage.
- Backup support.

Expected Impact

Production Ready

---

# Long-Term Vision

Hot Seat should evolve into an AI-powered interview platform capable of serving:

- Students
- Universities
- Placement Cells
- Coaching Institutes
- EdTech Companies
- Enterprise Recruiters

Future Business Models

- B2C Subscription
- B2B SaaS
- Interview-as-a-Service API
- White-label Platform