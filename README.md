
# 🎯 AI Interview Platform

An **AI-powered multi-domain interview preparation platform** that simulates realistic interviews using Generative AI. Candidates can upload their resume, generate personalized interview questions, answer using **voice, text, and code**, and receive detailed AI-powered feedback with scores and improvement suggestions.

---

# 🚀 Features

- 🔐 JWT Authentication
- 📄 Resume Upload & PDF Parsing
- 🤖 AI-Powered Interview Generation
- 💼 Multi-Domain Interviews (Software, Finance, Consulting, Sales, Marketing)
- 📊 Difficulty Selection (Easy / Medium / Hard)
- 🎤 Voice Answer Support
- ⌨️ Text Answer Support
- 💻 Built-in Code Editor
- 🧠 AI-Based Answer Evaluation
- 📈 Personalized Feedback & Scores
- 📜 Interview History
- 🐳 Dockerized Full-Stack Deployment
- 📖 Swagger API Documentation

---

# 🛠️ Tech Stack

## Frontend
- React
- Vite
- React Router
- CSS

## Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication
- Passlib + Bcrypt

## AI
- Google Gemini API

## DevOps
- Docker
- Docker Compose
- Nginx
- Git

---

# 📂 Project Structure

```text
Hot Seat/
│
├── backend/
│   ├── app/
│   ├── uploads/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   └── nginx.conf
│
├── docker/
│   └── postgres/
│       └── init.sql
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

# 🏗️ System Architecture

```text
Browser
   │
   ▼
React Frontend (Nginx)
   │
   ▼
FastAPI Backend
   │
   ├───────────────┐
   ▼               ▼
PostgreSQL     Gemini API
```

---

# ⚙️ Prerequisites

## 1. Install Git

### Windows
Download: https://git-scm.com/downloads

### macOS

```bash
brew install git
```

### Ubuntu

```bash
sudo apt update
sudo apt install git
```

Verify:

```bash
git --version
```

---

## 2. Install Docker Desktop

Download Docker Desktop:

https://www.docker.com/products/docker-desktop/

Verify installation:

```bash
docker --version
docker compose version
```

---

# 🚀 Getting Started

## Step 1. Clone Repository

```bash
git clone https://github.com/HarshalShah0508/AI-Interview-Platform.git
cd AI-Interview-Platform
```

---

## Step 2. Get a Gemini API Key

1. Visit https://aistudio.google.com/
2. Sign in with your Google account.
3. Click **Get API Key**.
4. Create a new API key.
5. Copy the generated key.

---

## Step 3. Generate a Secret Key

macOS / Linux

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

Windows

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

Copy the generated string.

---

## Step 4. Configure Environment Variables

Create:

```text
backend/.env
```

Example:

```env
DATABASE_URL=postgresql://interview_user_official:Harshal0508@postgres:5432/interview_db

SECRET_KEY=YOUR_GENERATED_SECRET_KEY

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

---

## Step 5. Start the Application

```bash
docker compose up --build
```

Docker will automatically:

- Build frontend
- Build backend
- Create PostgreSQL
- Connect all services

---

## Step 6. Verify Containers

```bash
docker ps
```

Expected containers:

- frontend
- backend
- postgres

---

# 🌐 Application URLs

Frontend

```text
http://localhost:3000
```

Backend Swagger

```text
http://localhost:8000/docs
```

---

# 📋 Application Workflow

1. Register an account
2. Login
3. Upload a PDF resume
4. Select interview role
5. Select difficulty
6. Generate AI interview questions
7. Answer using voice, text, or code
8. Submit answers
9. Review AI feedback
10. View interview history

---

# 🐳 Docker Services

| Service | Port |
|----------|------|
| Frontend | 3000 |
| Backend | 8000 |
| PostgreSQL | 5432 |

---

# 🔒 Security

- JWT Authentication
- Password Hashing (Passlib + Bcrypt)
- Protected REST APIs
- Environment Variables for Secrets

---

# 📷 Screenshots

Add screenshots here:

- Login Page
- Dashboard
- Resume Upload
- Interview Generation
- Interview Session
- AI Feedback
- Interview History

---

# ❗ Troubleshooting

## Docker daemon not running

Start Docker Desktop and retry.

---

## Invalid Gemini API Key

Verify `GEMINI_API_KEY` inside `backend/.env`.

---

## Port already in use

Stop the conflicting service or modify the exposed port in `docker-compose.yml`.

---

## Containers fail to start

```bash
docker compose down
docker compose up --build
```

---

## Database connection error

Ensure the password in `DATABASE_URL` matches the PostgreSQL credentials configured in `docker-compose.yml`.

---

# 📈 Future Enhancements

- Video Interview Support
- AI Follow-up Questions
- Real-Time Code Execution
- Company Interview Templates
- Leaderboards
- Email Reports
- Cloud Deployment
- Analytics Dashboard

---

# 🤝 Contributing

```bash
git checkout -b feature/my-feature

git add .

git commit -m "Add new feature"

git push origin feature/my-feature
```

Create a Pull Request for review.

---

# 👨‍💻 Author

**Harshal Shah**

BITS Pilani Hyderabad Campus

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub!
