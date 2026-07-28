# 🧞 EduGenie AI – Intelligent AI Study Assistant

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36+-red.svg)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-green.svg)](https://python.langchain.com/)
[![FAISS](https://img.shields.io/badge/FAISS-VectorDB-orange.svg)](https://github.com/facebookresearch/faiss)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **EduGenie AI** is an AI-powered learning assistant that helps students interact with study materials through Retrieval-Augmented Generation (RAG). Built with LangChain, FAISS, HuggingFace Embeddings, Streamlit, and OpenRouter API, it delivers accurate, context-aware answers, quizzes, summaries, flashcards, and personalized learning support.

---

# Live Demo

**Streamlit App:**  
https://edugenie-study-assistant.streamlit.app/

---

#  Overview

EduGenie AI transforms traditional learning into an interactive AI-powered experience. Instead of manually searching through lengthy notes or PDFs, students can upload study material and instantly interact with it using natural language.

The application combines Retrieval-Augmented Generation (RAG) with Large Language Models to retrieve relevant information from uploaded documents before generating responses. This approach significantly improves factual accuracy while reducing hallucinations.

The platform also includes gamification features such as XP, Levels, Achievements, Learning Progress, Daily Streaks, and AI Personalities to make studying more engaging and enjoyable.

---

#  Key Features

##  AI Learning Features

-  Context-aware AI Chat
-  Intelligent PDF Question Answering
-  AI Generated Flashcards
-  Automatic Quiz Generation
-  Smart PDF Summarization
-  Semantic Search using FAISS
-  Retrieval-Augmented Generation (RAG)

---

##  Personalized Learning

-  Friendly Genie Personality
-  Teacher Mode
-  Professor Mode
-  Exam Expert Mode

### Difficulty Levels

- Easy
- Medium
- Hard

### Explanation Styles

- Beginner
- Normal
- College
- Professional

---

##  Gamification

-  XP Reward System
-  Level Progression
-  Achievement Badges
-  Daily Learning Streak
-  Progress Dashboard

---

## Modern User Interface

-  Dark Mode
-  Light Mode
-  ChatGPT-inspired Chat UI
-  Beautiful Analytics Cards
-  Smooth Animations
-  Responsive Layout
-  Clean Sidebar Navigation

---

#  Architecture

```
                PDF
                 │
        PDF Loader (PyPDF)
                 │
          Text Chunking
            (LangChain)
                 │
      HuggingFace sentence Embeddings
                 │
        FAISS Vector Database
                 │
        Semantic Retrieval
                 │
        OpenRouter API (LLM)
                 │
      Context-Aware Response
```

---

#  Tech Stack

| Category | Technology |
|----------|------------|
| Frontend | Streamlit |
| Backend | Python |
| LLM | OpenRouter API |
| RAG Framework | LangChain |
| Embeddings | HuggingFace Sentence Transformers |
| Vector Database | FAISS |
| PDF Processing | PyPDF |
| Data Analysis | Pandas, NumPy |
| Visualization | Plotly |

---

#  Project Structure

```
Celebal-AI-Study-Assistant-Pro/
│
├── assets/
│   └── genie.gif
│
├── backend/
│   ├── cache.py
│   ├── config.py
│   ├── llm.py
│   ├── logger.py
│   ├── pdf_loader.py
│   ├── prompts.py
│   ├── rag.py
│   ├── utils.py
│   └── vector_store.py
│
├── frontend/
│   ├── chat.py
│   ├── quiz.py
│   ├── sidebar.py
│   ├── styles.py
│   └── summary.py
│
├── data/
│   ├── raw/
│   │   └── study_material.pdf
│   └── processed/
│       └── faiss_index/
│
├── docs/
│   └── screenshots/
│       ├── 01_dashboard.png
│       ├── 02_chat.png
│       ├── 03_quiz.png
│       ├── 04_flashcards.png
│       ├── 05_progress.png
│       └── 06_achievements.png
│
├── logs/
│
├── app.py
├── streamlit_app.py
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

---

#  Installation

## 1. Clone Repository

```bash
git clone https://github.com/agarwalkishu789-commits/EduGenie-AI.git

cd EduGenie-AI
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file inside the project root.

```
OPENROUTER_API_KEY=your_openrouter_api_key
```

You can generate your API Key from:

https://openrouter.ai/

---

## 5. Add Study Material

Place your study PDF inside

```
data/raw/study_material.pdf
```

---

#  Running the Application

```bash
streamlit run app.py
```

The application will start at:

```
http://localhost:8501
```
---

#  How to Use

##  AI Chat

- Ask questions directly from your uploaded study material.
- Receive context-aware answers powered by RAG.
- Chat history is maintained during your session.
- Choose different AI personalities for different learning styles.

---

##  AI Quiz Generator

Generate practice quizzes directly from your uploaded PDF.

Features include:

- Multiple question generation
- Difficulty selection
- Instant answer checking
- Score calculation
- Explanation of answers
- XP rewards

---

##  Smart Flashcards

Automatically generate flashcards from study material.

Useful for:

- Quick revision
- Concept memorization
- Exam preparation

---

##  Smart Summary

Generate concise summaries of uploaded documents.

The summary highlights:

- Key concepts
- Important definitions
- Major topics
- Revision points

---

##  XP & Level System

Students earn XP by interacting with EduGenie AI.

### XP Rewards

| Activity | XP |
|-----------|----|
| Ask Question | +5 |
| Complete Quiz | +20 |
| Perfect Quiz Score | +50 |

Every 100 XP unlocks a new level.

---

##  Achievements

Unlock learning achievements by completing milestones.

Examples include:

-  Quiz Master
-  100 Questions
-  7-Day Learning Streak
-  Fast Learner
-  Dedicated Student

---

##  Learning Progress

Monitor your learning journey with interactive analytics.

Track:

- Questions Asked
- Quiz Scores
- Learning Streak
- XP Earned
- Current Level
- Overall Progress

---

#  AI Personalization

EduGenie AI provides multiple learning styles.

## AI Personalities

-  Friendly Genie
-  Teacher
-  Professor
-  Exam Expert

---

## Difficulty Levels

- Easy
- Medium
- Hard

---

## Explanation Styles

- Beginner
- Normal
- College
- Professional

---

## Theme Support

-  Light Mode
-  Dark Mode

---

#  What Makes EduGenie AI Unique?

Unlike a traditional chatbot, EduGenie AI combines Retrieval-Augmented Generation (RAG) with modern AI technologies to provide accurate and document-grounded responses.

Key highlights:

- Retrieval-Augmented Generation (RAG)
- FAISS Semantic Search
- HuggingFace Embeddings
- Multiple AI Personalities
- Adaptive Learning
- Quiz & Flashcard Generation
- Gamified Learning Experience
- Progress Tracking Dashboard
- Responsive Modern UI
- Modular Architecture

---

#  Learning Analytics

EduGenie AI allows students to visualize their learning progress.

Analytics include:

- Learning Progress
- Quiz Performance
- Average Score
- XP Progress
- Daily Learning Activity
- Total Questions Asked

---

#  Screenshots

##  Dashboard

![Dashboard](docs/screenshots/01_dashboard.png)

---

##  AI Chat

![Chat](docs/screenshots/02_chat.png)

---

##  Quiz Generator

![Quiz](docs/screenshots/03_quiz.png)

---

##  Flashcards

![Flashcards](docs/screenshots/04_flashcards.png)

---

##  Progress Dashboard

![Progress](docs/screenshots/05_progress.png)

---

##  Achievements

![Achievements](docs/screenshots/06_achievements.png)

---

#  Future Enhancements

Planned improvements include:

-  Voice Interaction (Speech-to-Text & Text-to-Speech)
-  Multi-language Support
-  Multiple PDF Upload Support
-  Export Notes as PDF
-  AI Study Planner
-  Mind Map Generation
-  Image-based Question Answering
-  Interview Preparation Mode

---

#  How RAG Works

EduGenie AI follows the Retrieval-Augmented Generation workflow:

1. Upload PDF
2. Extract Text
3. Split into Chunks
4. Generate Embeddings
5. Store in FAISS
6. Retrieve Relevant Chunks
7. Send Context + Question to OpenRouter API
8. Generate Accurate Response

This ensures responses remain grounded in the uploaded study material.

---

### PDF Not Found

Place your study material inside:

```
data/raw/study_material.pdf
```

---

### Quiz Not Generating

Possible reasons:

- Invalid API Key
- Empty PDF
- Internet Connection Issue

---

### Vector Database Error

Delete the existing FAISS index and upload the PDF again.

---

#  License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for more details.

---

#  Acknowledgements

Special thanks to the following open-source technologies:

- Streamlit
- LangChain
- FAISS
- HuggingFace
- OpenRouter
- PyPDF
- Plotly

---

#  Developer

**Kishu Agarwal**

PGDM (Business Analytics & AI)

AI | Data Analytics Enthusiast | Generative AI Enthusiast

Project developed as part of the **Celebal Technologies Internship Program**.

---

<div align="center">

# 🧞 EduGenie AI

### *Your AI-Powered Learning Companion*

Transform your study experience with intelligent AI assistance.

If you found this project useful, consider giving it a  on GitHub.

</div>
