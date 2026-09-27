# CareerForge-AI
# 🤖 AI Resume Analyser & MockTest Portal

An AI-powered career preparation platform built with **Python and Streamlit** that helps students and job seekers analyze their resumes, identify suitable job roles, find skill gaps, follow personalized study plans, take mock tests, and improve interview confidence.

---

## 📌 Project Overview

The **AI Resume Analyser & MockTest Portal** is designed as an all-in-one career preparation application.

Users can upload their resume in PDF format and receive insights about suitable job roles, matching skills, and missing skills. The platform also provides a structured 30-day study plan, subject-wise study materials, timed mock tests, performance analytics, and an AI-powered interview confidence coach.

The application has a simple and interactive **Streamlit** interface.

---

## ✨ Features

### 📄 1. AI Resume Analyser & Job Match

- Upload your resume in **PDF format**
- Automatically parse resume content
- Analyze skills and experience
- Match resume skills with different job roles
- Display job-role match percentage
- Identify relevant skills
- Highlight missing or recommended skills
- Provide career-oriented insights

Example:

> **Role: Web Developer — Match: 60%**

---

### 📅 2. 30-Day Action Plan & Study Routine

Provides a structured study plan based on selected subjects.

Features include:

- 30-day learning roadmap
- Daily study schedule
- Subject-wise topics
- Detailed syllabus overview
- Comprehensive study materials
- Recommended learning routine

Example subjects:

- Database Management Systems
- Data Structures
- Operating Systems
- Computer Networks
- Programming
- Web Development

---

### 📝 3. MockTest Portal

Practice technical questions through an interactive mock-test system.

Features:

- Timed mock tests
- Randomized questions
- Multiple-choice questions
- Automatic scoring
- Subject-based tests
- Performance evaluation

This helps users simulate technical assessments before interviews or placement exams.

---

### 📊 4. Performance Analytics

Track your mock-test performance using analytics.

The dashboard can provide:

- Test scores
- Accuracy
- Attempt history
- Subject-wise performance
- Weak areas
- Progress tracking
- Performance radar chart

This helps users understand which topics require more preparation.

---

### 🎤 5. AI Interview & Confidence Coach

An interview preparation section designed to help users prepare for technical and HR interviews.

Possible functionality includes:

- Interview questions
- Technical interview preparation
- HR interview preparation
- Confidence-building exercises
- Answer improvement suggestions
- Interview practice

---

### 🔐 6. Login Portal

The application includes a login interface for user access.

Features:

- Username authentication
- Password authentication
- Password visibility toggle
- Protected application pages
- Logout functionality

---

## 🖥️ Application Screenshots

### 🔐 Login Portal

![Login Portal](Screenshot%202026-09-27%20205810.png)

---

### 📄 Resume Analyser & Job Match

![Resume Analyser](Screenshot%202026-09-27%20205754.png)

---

### 📚 30-Day Action Plan & Study Materials

![Study Plan](Screenshot%202026-09-27%20205724.png)

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| 🐍 Python | Core programming language |
| 🎈 Streamlit | Web application framework |
| 📄 PDF Parser | Resume text extraction |
| 🤖 AI/ML | Resume and career analysis |
| 📊 Plotly / Charts | Performance visualization |
| 💻 VS Code | Development environment |
| 🔀 Git & GitHub | Version control |

---

## 📂 Project Structure

```text
AI-Resume-Analyser/
│
├── app.py
├── requirements.txt
├── README.md
│
├── assets/
│   └── screenshots/
│
├── data/
│   ├── questions/
│   └── study_material/
│
├── models/
│
├── utils/
│   ├── resume_parser.py
│   ├── job_matcher.py
│   ├── mocktest.py
│   └── analytics.py
│
└── .gitignore
