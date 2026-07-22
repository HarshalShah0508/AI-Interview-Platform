# 🎯 AI Interview Platform

An AI-powered interview preparation platform that simulates real technical interviews using Generative AI. Candidates can upload their resume, generate personalized interview questions, answer using text, voice, and code, and receive detailed AI-powered feedback with scores and improvement suggestions.

---

## 🚀 Features

- 🔐 User Authentication (JWT)
- 📄 Resume Upload & PDF Parsing
- 🤖 AI-Based Interview Question Generation
- 💼 Role-Based Interviews
- 📊 Difficulty Selection (Easy / Medium / Hard)
- 🎤 Voice Answer Support
- ⌨️ Text Answer Support
- 💻 Code Editor for Coding Questions
- 🧠 AI Answer Evaluation
- 📈 Detailed Feedback & Scores
- 📜 Interview History
- 🐳 Dockerized Full-Stack Application
- 📖 Interactive API Documentation (Swagger)

---

## 🛠️ Tech Stack

### Frontend
- React
- Vite
- React Router
- CSS

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication
- Passlib (Password Hashing)

### AI
- Google Gemini API

### DevOps
- Docker
- Docker Compose
- Nginx

---

# 📂 Project Structure

```text
InterviewAI/
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
           ┌────────────┴────────────┐
           │                         │
           ▼                         ▼
      PostgreSQL Database       Gemini API
```

---

# ⚙️ Prerequisites

Before running the project, ensure the following are installed:

- Docker Desktop
- Git

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/HarshalShah0508/AI-Interview-Platform.git
cd AI-Interview-Platform
```

---

## 2. Create Environment File

Inside the **backend** directory, create a `.env` file.

Example:

```env
DATABASE_URL=postgresql://interview_user_official:<password>@postgres:5432/interview_db

SECRET_KEY=<your_secret_key>

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

GEMINI_API_KEY=<your_gemini_api_key>
```

---

## 3. Run with Docker

```bash
docker compose up --build
```

Docker automatically:

- Builds the frontend
- Builds the backend
- Starts PostgreSQL
- Creates the database
- Connects all services

---

# 🌐 Application URLs

### Frontend

```
http://localhost:3000
```

### Backend API

```
http://localhost:8000/docs
```

---

# 📋 Application Workflow

1. Register/Login
2. Upload Resume
3. Select Interview Role
4. Choose Difficulty
5. Generate AI Interview Questions
6. Answer Using:
   - Voice
   - Text
   - Code
7. Submit Answers
8. Receive AI Evaluation
9. View Interview History

---

# 🐳 Docker Services

| Service | Port |
|----------|------|
| Frontend | 3000 |
| Backend | 8000 |
| PostgreSQL | 5432 |


# 🔒 Security

- JWT Authentication
- Password Hashing using Passlib & Bcrypt
- Protected API Endpoints
- Environment Variables for Secrets

---

# 📈 Future Enhancements

- Video Interview Support
- AI Follow-up Questions
- Real-Time Code Execution
- Multi-Language Interviews
- Admin Dashboard
- Company Interview Templates
- Leaderboards
- Email Performance Reports
- Cloud Deployment (AWS/GCP/Azure)

---

# 👨‍💻 Author

**Harshal Shah**

BITS Pilani Hyderabad Campus

---

# ⭐ If you found this project useful, consider giving it a Star on GitHub!
