# 🚀 Hot Seat – AI-Powered Interview Preparation Platform

<p align="center">
An AI-powered interview preparation platform that simulates real technical interviews using Generative AI. Candidates can upload their resume, generate personalized interview questions, solve coding problems, answer using voice, text, and code, and receive detailed AI-powered feedback with personalized improvement suggestions.
</p>

<p align="center">

![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![Google OAuth](https://img.shields.io/badge/Google-OAuth-4285F4?logo=google)
![JWT](https://img.shields.io/badge/JWT-Authentication-black)
![Gemini](https://img.shields.io/badge/Google-Gemini-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

</p>

---

### 🔗 Application

> https://hotseatai.vercel.app

### 📘 Backend API Documentation

> https://interview-backend-5u2z.onrender.com/docs

---

# 📖 Overview

Hot Seat is a production-ready AI-powered interview preparation platform designed to simulate real-world technical interviews.

Unlike traditional interview preparation websites that simply generate a list of questions, Hot Seat behaves like an intelligent interviewer capable of generating role-specific interviews, asking adaptive follow-up questions, evaluating responses using Generative AI, and providing personalized feedback.

Candidates can answer interview questions using:

- 🎤 Voice
- ⌨️ Text
- 💻 Code

making the interview experience closely resemble actual software engineering interviews.

The platform currently supports multiple interview domains including:

- Software Engineering
- Finance
- Consulting
- Sales
- Marketing

---

# ✨ Features

## 🔐 Authentication

Hot Seat provides a complete authentication system supporting both traditional and OAuth-based authentication.

- JWT Authentication
- Email & Password Login
- Google OAuth Login
- Smart Account Linking
- Email Verification
- Resend Verification Email
- Protected Routes
- Secure Password Hashing using Passlib & Bcrypt
- Verification Token Expiry
- Single-Use Email Verification Tokens

Local accounts must verify their email address before they can log in.

Google OAuth accounts are authenticated directly through Google and do not require the local email verification flow.

---

## 📄 Resume Management

- Upload Resume
- PDF Parsing
- Resume Storage
- Resume Deletion
- Extract Resume Content
- Resume-Based Question Generation

---

## 🤖 AI Interview Engine

- Resume-Based Questions
- Multi-Domain Interview Generation
- Difficulty Selection
- Software Engineering Interviews
- Finance Interviews
- Consulting Interviews
- Sales Interviews
- Marketing Interviews
- Prompt Optimization
- Structured AI Prompt Routing

---

## 🎯 Adaptive Interview Experience

Hot Seat no longer behaves like a static interview generator.

It dynamically adapts the interview based on candidate performance.

### Context-Aware Follow-up Questions

If a candidate's answer receives a score below a configurable threshold, the platform automatically generates an AI follow-up question before proceeding to the next topic.

This closely mimics how human interviewers probe deeper when a candidate provides an incomplete or weak answer.

---

## 💻 Coding Interview Environment

Hot Seat includes a complete LeetCode-style coding environment powered by the Monaco Editor.

### Features

- Monaco Editor with VS Code-like experience
- Multi-language Support
- Compile & Run
- Runtime Output
- Compilation Errors
- Sample Test Cases
- Hidden Test Cases
- AI Code Evaluation
- Language-specific execution environments

### Supported Languages

- C
- C++
- Java
- Python
- JavaScript
- Verilog

The coding environment supports both conventional programming languages and hardware description language workflows, allowing candidates to practice a wider range of technical interview problems.

---

## 🎙 Hybrid Interview Mode

Candidates can answer interview questions using:

- 🎤 Voice
- ⌨️ Text
- 💻 Code

These inputs can be combined into a single interview response.

For example, a candidate can:

1. Explain their approach using voice.
2. Add additional notes using text.
3. Implement the solution inside the coding environment.

The combined response is then evaluated by the AI interview engine.

---

## 📊 AI Evaluation

Every answer is evaluated using Google Gemini.

The platform provides:

- Overall Score
- Strengths
- Areas for Improvement
- Personalized Feedback
- AI Evaluation
- Coding Feedback
- Interview History
- Context-Aware Follow-up Questions

---

## 📚 Interview History

Candidates can revisit previous interviews and review:

- Questions
- Answers
- AI Feedback
- Scores
- Interview Details

---

# 🚀 Production Deployment

The application is fully deployed using a modern cloud architecture.

| Component | Platform |
|-----------|----------|
| Frontend | Vercel |
| Backend | Render |
| Database | Neon PostgreSQL |

---

# 🏗 System Architecture

```text
                              Browser
                                 │
                                 ▼
                     React + Vite Frontend
                                 │
                Google OAuth + JWT + Email Verification
                                 │
                                 ▼
                         FastAPI Backend
                                 │
      ┌───────────────┬───────────────┬───────────────┐
      ▼               ▼               ▼               ▼
 Resume Engine   Interview Engine  Coding Engine  Evaluation Engine
      │               │               │               │
      └───────────────┴───────────────┴───────────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
             Google Gemini AI          PostgreSQL
                                           │
                                      Neon + Alembic
```

---

# 🔄 Application Workflow

```text
User Registration / Google Login
            │
            ▼
     Email Verification
      (Local Accounts)
            │
            ▼
      Upload Resume
            │
            ▼
 Resume Parsing & Extraction
            │
            ▼
 Select Interview Domain
            │
            ▼
 Select Difficulty
            │
            ▼
 AI Interview Generation
            │
            ▼
 Answer Using
   • Voice
   • Text
   • Code
            │
            ▼
 AI Evaluation
            │
            ▼
 Context-Aware Follow-up Question
       (if required)
            │
            ▼
 Final Feedback
            │
            ▼
 Interview History
```

---

# 🛠 Tech Stack

## Frontend

- React
- Vite
- React Router
- React Context API
- Monaco Editor
- Google OAuth
- CSS

---

## Backend

- FastAPI
- SQLAlchemy
- Alembic
- JWT Authentication
- Google OAuth
- Passlib
- Bcrypt
- Python

---

## Artificial Intelligence

- Google Gemini
- `google-genai`

Used for:

- Interview Generation
- Answer Evaluation
- Coding Evaluation
- Adaptive Follow-up Questions

---

## Email

- Brevo
- Transactional Email API
- Email Verification
- Verification Email Resending

---

## Database

- PostgreSQL
- Neon
- Alembic

---

## DevOps

- Docker
- Docker Compose
- Render
- Vercel
- Nginx

---

# 🏆 Project Highlights

- ✅ Production Deployed
- ✅ Google OAuth Authentication
- ✅ Email Verification
- ✅ Resend Verification Emails
- ✅ Multi-Domain AI Interviews
- ✅ Context-Aware Follow-up Questions
- ✅ Monaco Coding Environment
- ✅ C / C++ / Java / Python / JavaScript / Verilog Support
- ✅ AI Answer Evaluation
- ✅ Hybrid Interview (Voice + Text + Code)
- ✅ Dockerized Full-Stack Application
- ✅ PostgreSQL + Alembic Migrations
- ✅ Public REST APIs

---

# ⚙️ Prerequisites

Before running the project locally, ensure the following software is installed on your system.

| Software | Version |
|----------|---------|
| Git | Latest |
| Docker Desktop | Latest |
| Node.js | 20+ |
| Python | 3.11+ |
| PostgreSQL *(optional if using Docker)* | 16+ |

---

# 📂 Project Structure

```text
Hot-Seat/
│
├── backend/
│   ├── alembic/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── utils/
│   ├── uploads/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic.ini
│   └── .env.example
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

# 🚀 Installation Guide

## Step 1 — Clone the Repository

```bash
git clone https://github.com/HarshalShah0508/AI-Interview-Platform.git

cd AI-Interview-Platform
```

---

## Step 2 — Create Backend Environment Variables

Navigate to the backend directory.

```bash
cd backend
```

Create a `.env` file.

```bash
touch .env
```

Add the required configuration.

```env
DATABASE_URL=postgresql://interview_user_official:YOUR_PASSWORD@postgres:5432/interview_db

SECRET_KEY=YOUR_SECRET_KEY

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

GEMINI_API_KEY=YOUR_GEMINI_API_KEY

GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID

FRONTEND_URL=http://localhost:3000

BREVO_API_KEY=YOUR_BREVO_API_KEY
```

> Never commit your `.env` file or expose API keys publicly.

---

# 🔑 Generate Secret Key

Generate a secure JWT secret.

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

Copy the generated value into:

```env
SECRET_KEY=YOUR_SECRET_KEY
```

---

# 🤖 Google Gemini API Setup

Hot Seat uses Google's Gemini API for:

- Interview Generation
- Answer Evaluation
- Coding Evaluation
- Follow-up Questions

## Step 1

Visit:

https://aistudio.google.com/

## Step 2

Sign in using your Google account.

## Step 3

Click:

```text
Get API Key
```

## Step 4

Create a new API key.

## Step 5

Copy the key into:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

# 🔐 Google OAuth Setup

Hot Seat supports authentication using Google OAuth.

## Step 1

Open:

https://console.cloud.google.com/

## Step 2

Create a new project.

## Step 3

Navigate to:

```text
APIs & Services
        ↓
Credentials
```

## Step 4

Create an:

```text
OAuth Client ID
```

## Step 5

Select:

```text
Web Application
```

## Step 6

Add Authorized JavaScript Origins.

For local development:

```text
http://localhost:3000
http://localhost:5173
```

## Step 7

Add the appropriate authorized origin/redirect configuration for the frontend.

> Update these values if your frontend runs on a different port.

## Step 8

Copy the Client ID.

Add it to the backend:

```env
GOOGLE_CLIENT_ID=YOUR_CLIENT_ID
```

And create:

```text
frontend/.env
```

with:

```env
VITE_GOOGLE_CLIENT_ID=YOUR_CLIENT_ID

VITE_API_URL=http://localhost:8000
```

---

# 📧 Email Verification Setup

Hot Seat uses Brevo for transactional verification emails.

## Step 1

Create a Brevo account.

## Step 2

Generate a Brevo API key.

## Step 3

Add the key to the backend environment:

```env
BREVO_API_KEY=YOUR_BREVO_API_KEY
```

## Step 4

Configure the frontend URL:

For local development:

```env
FRONTEND_URL=http://localhost:3000
```

For production:

```env
FRONTEND_URL=https://hotseatai.vercel.app
```

The verification email contains a secure verification link generated by the backend.

### Verification Flow

```text
Signup
   │
   ▼
Create Account
   │
   ▼
Generate Secure Token
   │
   ▼
Store Token Hash
   │
   ▼
Send Verification Email
   │
   ▼
User Clicks Link
   │
   ▼
Verify Token
   │
   ▼
Mark Email as Verified
   │
   ▼
User Can Login
```

Verification tokens:

- Expire after 24 hours.
- Are stored as SHA-256 hashes.
- Are single-use.
- Are replaced when a new verification email is requested.

---

# 🐳 Running with Docker (Recommended)

Return to the project root.

```bash
cd ..
```

Build and start the containers:

```bash
docker compose up --build
```

Docker starts:

- Frontend
- Backend
- PostgreSQL

and connects the services together.

---

# 🌐 Application URLs

Frontend:

```text
http://localhost:3000
```

Backend:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

---

# 🗄️ Database Migrations

Hot Seat uses Alembic for schema migrations.

Create a migration:

```bash
alembic revision --autogenerate -m "migration_name"
```

Apply migrations:

```bash
alembic upgrade head
```

Rollback:

```bash
alembic downgrade -1
```

---

# ▶️ Running Without Docker

## Backend

```bash
cd backend

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# ✅ Verify Installation

After everything starts successfully, visit:

```text
http://localhost:3000
```

Verify the following:

- ✅ Email Signup
- ✅ Email Verification
- ✅ Resend Verification Email
- ✅ Email Login
- ✅ Google Login
- ✅ Resume Upload
- ✅ Resume Parsing
- ✅ Interview Generation
- ✅ Voice Answers
- ✅ Text Answers
- ✅ Coding Environment
- ✅ C Code Execution
- ✅ C++ Code Execution
- ✅ Java Code Execution
- ✅ Python Code Execution
- ✅ JavaScript Code Execution
- ✅ Verilog Code Execution
- ✅ AI Evaluation
- ✅ Follow-up Questions
- ✅ Interview History

---

# 🚀 Deployment

Hot Seat is deployed using:

| Component | Platform |
|-----------|----------|
| Frontend | Vercel |
| Backend | Render |
| Database | Neon PostgreSQL |
| Email | Brevo |

---

# 🌍 Deploy Your Own Instance

## Backend (Render)

1. Fork this repository.

2. Create a new **Web Service** on Render.

3. Connect your GitHub repository.

4. Set the root directory to:

```text
backend
```

5. Build Command:

```bash
pip install -r requirements.txt
```

6. Start Command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

7. Configure the following environment variables:

```text
DATABASE_URL
SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES
ALGORITHM
GEMINI_API_KEY
GOOGLE_CLIENT_ID
FRONTEND_URL
BREVO_API_KEY
```

8. Deploy.

---

## Frontend (Vercel)

1. Import the repository into Vercel.

2. Set the root directory:

```text
frontend
```

3. Configure Environment Variables:

```env
VITE_API_URL=https://YOUR_RENDER_BACKEND_URL

VITE_GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID
```

4. Deploy.

---

# 🔌 API Overview

Hot Seat exposes REST APIs for all major functionality.

## Authentication

```text
POST /signup
POST /login
POST /auth/google
GET  /auth/verify-email
POST /auth/resend-verification
GET  /me
```

---

## Resume

```text
POST /resume/upload
GET /resume
DELETE /resume/{resume_id}
```

---

## Interview

```text
POST /interview/generate
GET /interview/history
GET /interview/{session_id}
```

---

## Answers

```text
POST /answer
GET /answer/session/{session_id}/results
```

---

## Coding

The coding environment provides APIs for:

```text
Code Execution
Compilation
Runtime Output
Compilation Errors
Test Case Evaluation
```

Supported languages include:

```text
C
C++
Java
Python
JavaScript
Verilog
```

---

## Documentation

Swagger UI:

```text
/docs
```

OpenAPI JSON:

```text
/openapi.json
```

---

# 🔒 Security

Hot Seat follows modern authentication and security practices.

Implemented:

- JWT Authentication
- Google OAuth
- Email Verification
- Verification Token Expiry
- Single-Use Verification Tokens
- Secure Password Hashing
- Protected API Endpoints
- Environment Variables for Secrets
- Ownership Validation for User Resources
- Google Token Verification
- Smart Account Linking
- Alembic Database Migrations
- Email Enumeration Protection for Verification Resends

---

# 📈 Current Features

### Authentication

- JWT Authentication
- Email & Password Login
- Google OAuth
- Smart Account Linking
- Email Verification
- Resend Verification Email
- Protected Routes

### Resume

- Resume Upload
- Resume Parsing
- Resume Deletion
- Resume-Based Question Generation

### AI Interviews

- AI Interview Generation
- Multi-Domain Interviews
- Difficulty Selection
- Prompt Optimization
- Context-Aware Follow-up Questions
- AI Answer Evaluation

### Coding

- Monaco Editor
- C
- C++
- Java
- Python
- JavaScript
- Verilog
- Compile & Run
- Sample Test Cases
- Hidden Test Cases
- Runtime Output
- Compilation Errors
- AI Code Evaluation

### Interview Experience

- Voice Answers
- Text Answers
- Code Answers
- Hybrid Voice + Text + Code Interviews
- Interview History

### Infrastructure

- PostgreSQL
- Neon
- Alembic
- Docker
- Docker Compose
- Render Deployment
- Vercel Deployment

---

# 🛣️ Product Roadmap

## ✅ Completed

- [x] JWT Authentication
- [x] Email & Password Authentication
- [x] Google OAuth Authentication
- [x] Smart Account Linking
- [x] Email Verification
- [x] Resend Verification Emails
- [x] Resume Upload
- [x] Resume Management
- [x] Resume Parsing
- [x] AI Interview Generation
- [x] Multi-Domain Interviews
- [x] Prompt Optimization
- [x] Context-Aware Follow-up Questions
- [x] Voice + Text + Code Interviews
- [x] Monaco Editor Integration
- [x] C Support
- [x] C++ Support
- [x] Java Support
- [x] Python Support
- [x] JavaScript Support
- [x] Verilog Support
- [x] Multi-Language Support
- [x] Compile & Run
- [x] Sample Test Cases
- [x] Hidden Test Cases
- [x] AI Answer Evaluation
- [x] Interview History
- [x] PostgreSQL Migration
- [x] Alembic Migrations
- [x] Dockerization
- [x] Render Deployment
- [x] Vercel Deployment

---

## 🚧 Planned Features

### AI Improvements

- [ ] AI Code Review
- [ ] Voice Recognition Improvements
- [ ] Resume AI Review
- [ ] Adaptive AI Interviewer
- [ ] Interview Personas

---

### Analytics

- [ ] Skill Dashboard
- [ ] Performance Trends
- [ ] Learning Roadmap
- [ ] Downloadable Interview Reports

---

### Interview Packs

- [ ] Google
- [ ] Amazon
- [ ] Microsoft
- [ ] Atlassian
- [ ] Uber
- [ ] Goldman Sachs
- [ ] McKinsey
- [ ] BCG

---

### Production

- [ ] Forgot Password
- [ ] Notification Emails
- [ ] Cloud Resume Storage
- [ ] Resume Versioning
- [ ] Rate Limiting
- [ ] Advanced Monitoring

---

### SaaS

- [ ] Institute Dashboard
- [ ] Recruiter Dashboard
- [ ] Subscription Plans
- [ ] API Platform
- [ ] White-Label Solution

---

# 🤝 Contributing

Contributions are welcome.

If you would like to improve Hot Seat:

1. Fork this repository.

2. Create a feature branch.

```bash
git checkout -b feature/your-feature-name
```

3. Commit your changes.

```bash
git commit -m "Add feature"
```

4. Push your branch.

```bash
git push origin feature/your-feature-name
```

5. Open a Pull Request.

---

# 💡 Future Vision

Hot Seat aims to evolve beyond an interview preparation platform into a complete AI-powered interview ecosystem.

Future versions will support:

- AI Interview Coach
- Recruiter Dashboard
- Institute Portal
- Interview-as-a-Service APIs
- Enterprise Hiring Solutions
- AI Resume Optimization
- Personalized Learning Paths
- Company-Specific Interview Simulations
- Hardware / Verilog Interview Preparation

---

# 👨‍💻 Author

**Harshal Shah**

B.E. Computer Science

BITS Pilani, Hyderabad Campus

GitHub

https://github.com/HarshalShah0508

LinkedIn

(Add your LinkedIn URL)

---

# ⭐ Support

If you found this project useful:

⭐ Star the repository

🐛 Report bugs

💡 Suggest improvements

🤝 Share your feedback

Your support helps improve Hot Seat and motivates future development.

---

## 📜 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

---

<p align="center">

Built with ❤️ using React, FastAPI, PostgreSQL, Docker, Google Gemini, Google OAuth and Brevo.

</p>