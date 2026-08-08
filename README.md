# 🚀 Hot Seat – AI-Powered Interview Preparation Platform

<p align="center">
  <img src="screenshots/logo.png" alt="Hot Seat Logo" width="180"/>
</p>

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

# 🌐 Live Demo

### 🔗 Application

> https://YOUR-VERCEL-URL.vercel.app

### 📘 Backend API Documentation

> https://YOUR-RENDER-URL.onrender.com/docs

---

# 📖 Overview

Hot Seat is a production-ready AI-powered interview preparation platform designed to simulate real-world technical interviews.

Unlike traditional interview preparation websites that simply generate a list of questions, Hot Seat behaves like an intelligent interviewer capable of generating role-specific interviews, asking adaptive follow-up questions, evaluating responses using Generative AI, and providing personalized feedback.

Candidates can answer interview questions using:

- 🎤 Voice
- ⌨️ Text
- 💻 Code

making the interview experience closely resemble actual software engineering interviews.

The platform currently supports multiple interview domains including Software Engineering, Finance, Consulting, Sales, and Marketing.

---

# ✨ Features

## 🔐 Authentication

- JWT Authentication
- Email & Password Login
- Google OAuth Login
- Smart Account Linking
- Protected Routes
- Secure Password Hashing using Passlib & Bcrypt

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
- Software Interviews
- Finance Interviews
- Consulting Interviews
- Sales Interviews
- Marketing Interviews
- Prompt Optimizations
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

Hot Seat includes a complete LeetCode-style coding environment.

Features include:

- Monaco Editor (VS Code Experience)
- Multi-language Support
- Compile & Run
- Runtime Output
- Compilation Errors
- Sample Test Cases
- Hidden Test Cases
- Code Submission
- AI Code Evaluation

Supported Languages

- C++
- Java
- Python
- JavaScript

---

## 🎙 Hybrid Interview Mode

Candidates can answer interview questions using

- Voice
- Text
- Code

allowing both conceptual explanations and coding solutions within the same interview.

---

## 📊 AI Evaluation

Every answer is evaluated using Google Gemini.

The platform provides

- Overall Score
- Strengths
- Areas for Improvement
- Personalized Feedback
- AI Evaluation
- Coding Feedback
- Interview History

---

## 📚 Interview History

Candidates can revisit previous interviews and review

- Questions
- Answers
- AI Feedback
- Scores
- Interview Details

---

## 🚀 Production Deployment

The application is fully deployed.

Frontend

- Vercel

Backend

- Render

Database

- Neon PostgreSQL

---

# 🏗 System Architecture

```text
                              Browser
                                 │
                                 ▼
                     React + Vite Frontend
                                 │
                 Google OAuth + JWT Authentication
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
                           Google Gemini AI
                                 │
                                 ▼
                    PostgreSQL (Neon + Alembic)
```

---

# 🔄 Application Workflow

```text
User Registration / Google Login
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
 Context-Aware Follow-up Question (if required)
            │
            ▼
 Final Feedback
            │
            ▼
 Interview History
```

---

# 🖼 Screenshots

> Replace the placeholder images below with actual screenshots from the application.

## Authentication

| Login | Signup |
|-------|--------|
| ![](screenshots/login.png) | ![](screenshots/signup.png) |

---

## Dashboard

![](screenshots/dashboard.png)

---

## Resume Upload

![](screenshots/upload_resume.png)

---

## Interview Generation

![](screenshots/interview_generation.png)

---

## Coding Environment

![](screenshots/coding_environment.png)

---

## AI Feedback

![](screenshots/feedback.png)

---

## Interview History

![](screenshots/history.png)

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

- Google Gemini (google-genai)

---

## Database

- PostgreSQL
- Neon

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
- ✅ Multi-Domain AI Interviews
- ✅ Context-Aware Follow-up Questions
- ✅ Monaco Coding Environment
- ✅ AI Answer Evaluation
- ✅ Hybrid Interview (Voice + Text + Code)
- ✅ Dockerized Full-Stack Application
- ✅ PostgreSQL + Alembic Migrations
- ✅ Public REST APIs

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

Add the following configuration.

```env
DATABASE_URL=postgresql://interview_user_official:YOUR_PASSWORD@postgres:5432/interview_db

SECRET_KEY=YOUR_SECRET_KEY

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

GEMINI_API_KEY=YOUR_GEMINI_API_KEY

GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID
```

---

# 🔑 Generate Secret Key

Generate a secure JWT secret.

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

Copy the generated value into

```
SECRET_KEY
```

---

# 🤖 Google Gemini API Setup

Hot Seat uses Google's Gemini API for

- Interview Generation
- Answer Evaluation
- Follow-up Questions

## Step 1

Visit

https://aistudio.google.com/

---

## Step 2

Sign in using your Google account.

---

## Step 3

Click

```
Get API Key
```

---

## Step 4

Create a new API key.

---

## Step 5

Copy the key into

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

# 🔐 Google OAuth Setup

Hot Seat supports authentication using Google OAuth.

## Step 1

Open

https://console.cloud.google.com/

---

## Step 2

Create a new project.

---

## Step 3

Navigate to

```
APIs & Services

↓

Credentials
```

---

## Step 4

Create an

```
OAuth Client ID
```

---

## Step 5

Application Type

```
Web Application
```

---

## Step 6

Add Authorized JavaScript Origins

For Local Development

```
http://localhost:3000

http://localhost:5173
```

---

## Step 7

Add Authorized Redirect URI

```
http://localhost:5173
```

*(Update this if your frontend runs on a different port.)*

---

## Step 8

Copy the Client ID.

Add it to

Backend

```env
GOOGLE_CLIENT_ID=YOUR_CLIENT_ID
```

Frontend

Create

```
frontend/.env
```

```env
VITE_GOOGLE_CLIENT_ID=YOUR_CLIENT_ID

VITE_API_URL=http://localhost:8000
```

---

# 🐳 Running with Docker (Recommended)

Return to the project root.

```bash
cd ..
```

Build the containers.

```bash
docker compose up --build
```

Docker automatically

- Builds the frontend
- Builds the backend
- Starts PostgreSQL
- Creates the database
- Runs Alembic migrations
- Connects all services

---

# 🌐 Application URLs

Frontend

```
http://localhost:3000
```

Backend

```
http://localhost:8000
```

Swagger Documentation

```
http://localhost:8000/docs
```

---

# 🗄️ Database Migrations

Hot Seat uses Alembic for schema migrations.

Create a migration

```bash
alembic revision --autogenerate -m "migration_name"
```

Apply migrations

```bash
alembic upgrade head
```

Rollback

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

After everything starts successfully

Visit

```
http://localhost:3000
```

Verify the following

- ✅ Email Signup
- ✅ Email Login
- ✅ Google Login
- ✅ Resume Upload
- ✅ Interview Generation
- ✅ Voice Answers
- ✅ Coding Environment
- ✅ AI Evaluation
- ✅ Follow-up Questions

---

# 🚀 Deployment

Hot Seat is fully deployed using a modern cloud-native architecture.

| Component | Platform |
|-----------|----------|
| Frontend | Vercel |
| Backend | Render |
| Database | Neon PostgreSQL |

---

# 🌍 Deploy Your Own Instance

## Backend (Render)

1. Fork this repository.

2. Create a new **Web Service** on Render.

3. Connect your GitHub repository.

4. Set the root directory to:

```
backend
```

5. Build Command

```bash
pip install -r requirements.txt
```

6. Start Command

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

7. Configure the following environment variables:

```
DATABASE_URL
SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES
ALGORITHM
GEMINI_API_KEY
GOOGLE_CLIENT_ID
```

8. Deploy.

---

## Frontend (Vercel)

1. Import the repository into Vercel.

2. Set the root directory:

```
frontend
```

3. Configure Environment Variables

```
VITE_API_URL=https://YOUR_RENDER_BACKEND_URL

VITE_GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID
```

4. Deploy.

---

# 🔌 API Overview

Hot Seat exposes REST APIs for all major functionality.

## Authentication

```
POST /signup
POST /login
POST /auth/google
```

---

## Resume

```
POST /resume/upload
GET /resume
DELETE /resume/{resume_id}
```

---

## Interview

```
POST /interview/generate
GET /interview/history
GET /interview/{session_id}
```

---

## Answers

```
POST /answer
GET /answer/session/{session_id}/results
```

---

## Documentation

Swagger UI

```
/docs
```

OpenAPI JSON

```
/openapi.json
```

---

# 🔒 Security

Hot Seat follows modern authentication and security practices.

Implemented

- JWT Authentication
- Google OAuth
- Secure Password Hashing
- Protected API Endpoints
- Environment Variables for Secrets
- Ownership Validation for User Resources
- Google Token Verification
- Smart Account Linking
- Alembic Database Migrations

---

# 📈 Current Features

- JWT Authentication
- Email & Password Login
- Google OAuth
- Resume Upload
- Resume Parsing
- Resume Deletion
- AI Interview Generation
- Multi-Domain Interviews
- Prompt Optimization
- Context-Aware Follow-up Questions
- Voice + Text + Code Interviews
- Monaco Editor
- Multi-Language Coding Environment
- Compile & Run
- Sample Test Cases
- Hidden Test Cases
- AI Answer Evaluation
- Interview History
- PostgreSQL
- Alembic
- Docker
- Render Deployment
- Vercel Deployment

---

# 🛣️ Product Roadmap

## ✅ Completed

- [x] JWT Authentication
- [x] Resume Upload
- [x] Resume Management
- [x] Resume Parsing
- [x] AI Interview Generation
- [x] Multi-Domain Interviews
- [x] Prompt Optimization
- [x] Context-Aware Follow-up Questions
- [x] Voice + Text + Code Interviews
- [x] Monaco Editor Integration
- [x] Multi-Language Support
- [x] Compile & Run
- [x] Sample Test Cases
- [x] Hidden Test Cases
- [x] Google OAuth Authentication
- [x] Smart Account Linking
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

- [ ] Email Verification
- [ ] Forgot Password
- [ ] Notification Emails
- [ ] Cloud Resume Storage
- [ ] Resume Versioning

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

1. Fork the repository.

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

If you found this project useful,

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

Built with ❤️ using React, FastAPI, PostgreSQL, Docker, Google Gemini and Google OAuth.

</p>