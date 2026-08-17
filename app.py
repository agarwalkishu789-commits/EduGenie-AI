import streamlit as st
from pathlib import Path
import os
import json
import time
import tempfile
import re
from datetime import datetime
from dotenv import load_dotenv
import hashlib

from backend.pdf_loader import PDFLoader
from backend.vector_store import VectorStore
from backend.rag import RAGEngine

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(
    page_title="EduGenie AI",
    page_icon="🧞",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============= THEME CSS =============
LIGHT_THEME_CSS = """
<style>
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --bg-color: #ffffff;
        --text-color: #1a1a1e;
        --card-bg: #f5f7fa;
        --shadow: rgba(102, 126, 234, 0.3);
    }

    body {
        background-color: var(--bg-color) !important;
        color: var(--text-color) !important;
    }

    .stApp {
        background-color: var(--bg-color) !important;
    }
</style>
"""

DARK_THEME_CSS = """
<style>
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --bg-color: #0e1117;
        --text-color: #ffffff;
        --card-bg: #161b22;
        --shadow: rgba(102, 126, 234, 0.5);
    }

    body {
        background-color: var(--bg-color) !important;
        color: var(--text-color) !important;
    }

    .stApp {
        background-color: var(--bg-color) !important;
        color: var(--text-color) !important;
    }
</style>
"""

ULTIMATE_CSS = """
<style>
    * { transition: all 0.3s ease; }

    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    .stat-card-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0px 12px 24px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }

    .stat-card-box:hover {
        transform: translateY(-8px);
        box-shadow: 0px 16px 32px rgba(102, 126, 234, 0.4);
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        box-shadow: 0px 8px 16px rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0px 12px 24px rgba(102, 126, 234, 0.4) !important;
    }

    .title-gradient {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .badge-unlocked {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 0px 8px 20px rgba(255, 215, 0, 0.3);
    }

    .badge-locked {
        background: #ddd;
        opacity: 0.5;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
    }

    .source-citation {
        background: #f0f0f0;
        border-left: 3px solid #667eea;
        padding: 10px 12px;
        border-radius: 4px;
        font-size: 0.9em;
        color: #666;
        margin-top: 12px;
    }

    .welcome-container {
        text-align: center;
        padding: 60px 20px;
        animation: fadeIn 0.8s ease-in;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .feature-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0px 12px 24px rgba(102, 126, 234, 0.3);
        animation: slideUp 0.8s ease-out;
    }

    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
"""

def apply_theme(theme):
    if theme == "dark":
        st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)
    else:
        st.markdown(LIGHT_THEME_CSS, unsafe_allow_html=True)

    st.markdown(ULTIMATE_CSS, unsafe_allow_html=True)

# ============= SOURCE CLEANING =============
def clean_source_path(response_text, pdf_name):
    """Remove the internal RAG source block and return a display-safe citation."""
    source_block = re.compile(
        r"\n*\s*📄\s*Source:\s*.*?\n\s*📍\s*Page:\s*(\d+)\s*$",
        re.DOTALL,
    )
    match = source_block.search(response_text)

    if match:
        return source_block.sub("", response_text).strip(), pdf_name, int(match.group(1))

    return response_text.strip(), pdf_name, 1

# ============= PDF PROCESSING =============
def get_file_hash(file_bytes):
    return hashlib.md5(file_bytes).hexdigest()

def process_uploaded_pdf(pdf_file):
    try:
        file_bytes = pdf_file.read()
        file_hash = get_file_hash(file_bytes)

        temp_dir = tempfile.gettempdir()
        temp_pdf_path = Path(temp_dir) / f"edugenie_{file_hash}.pdf"

        if not temp_pdf_path.exists():
            with open(temp_pdf_path, 'wb') as f:
                f.write(file_bytes)

        return temp_pdf_path, file_hash, pdf_file.name
    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        return None, None, None

@st.cache_resource
def load_rag_with_pdf(pdf_path):
    try:
        if not OPENROUTER_API_KEY:
            raise ValueError("OpenRouter API key missing")

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found")

        loader = PDFLoader()
        chunks = loader.process_pdf(pdf_path)

        if not chunks:
            raise ValueError("No text extracted from PDF")

        vector_db = VectorStore()
        vector_db.create_vector_store(chunks)
        return RAGEngine(OPENROUTER_API_KEY)
    except Exception as e:
        st.error(f"Error loading RAG: {e}")
        return None

# ============= SESSION INIT =============
def initialize_session():
    defaults = {
        "welcome_done": False,
        "rag_loaded": False,
        "rag": None,
        "pdf_loaded": False,
        "current_pdf": None,
        "current_pdf_hash": None,
        "current_pdf_name": None,
        "theme": "light",
        "personality": "Friendly Genie",
        "difficulty": "Medium",
        "explain_style": "Normal",
        "messages": [],
        "quiz": None,
        "quiz_submitted": False,
        "quiz_answers": {},
        "summary": None,
        "flashcards": None,
        "xp": 0,
        "level": 1,
        "total_questions": 0,
        "total_quizzes": 0,
        "quiz_scores": [],
        "streak_days": 0,
        "all_badges": {
            "quiz_master": {"name": "Quiz Master", "requirement": "20 quizzes", "emoji": "🏅", "earned": False},
            "100_questions": {"name": "100 Questions", "requirement": "100 questions", "emoji": "💬", "earned": False},
            "streaker": {"name": "7-Day Streak", "requirement": "7 days", "emoji": "🔥", "earned": False},
        },
        "mood": "neutral",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def add_xp(amount):
    st.session_state.xp += amount
    old_level = st.session_state.level
    st.session_state.level = (st.session_state.xp // 100) + 1
    return st.session_state.level > old_level

def detect_mood(text):
    stress_words = ["stressed", "confused", "hard", "difficult", "help"]
    happy_words = ["great", "understood", "easy", "thanks", "good", "amazing"]
    text_lower = text.lower()
    if any(word in text_lower for word in stress_words):
        return "stressed"
    elif any(word in text_lower for word in happy_words):
        return "happy"
    return "neutral"

def check_achievements():
    if st.session_state.total_quizzes >= 20:
        st.session_state.all_badges["quiz_master"]["earned"] = True
    if st.session_state.total_questions >= 100:
        st.session_state.all_badges["100_questions"]["earned"] = True
    if st.session_state.streak_days >= 7:
        st.session_state.all_badges["streaker"]["earned"] = True

def welcome_animation():
    if not st.session_state.welcome_done:
        st.session_state.welcome_done = True
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.markdown('<div style="text-align: center; animation: slideUp 0.8s ease-out;"><h2 style="font-size: 3em; margin: 0;">🧞</h2></div>', unsafe_allow_html=True)

        time.sleep(0.5)
        st.success("Ready to learn!")

# ============= MAIN APP =============
def main():
    initialize_session()
    apply_theme(st.session_state.theme)

    # HEADER
    st.markdown("""
    <div style="text-align: center; margin: 40px 0 30px 0; animation: fadeIn 0.8s ease-in;">
        <h1 class="title-gradient" style="font-size: 3.5em; margin: 0;">🧞 EduGenie AI</h1>
        <p style="color: #666; font-size: 1.15em; margin-top: 10px; font-weight: 500;">Your AI-Powered Learning Companion</p>
    </div>
    """, unsafe_allow_html=True)

    welcome_animation()

    # SIDEBAR
    with st.sidebar:
        st.markdown("### Upload Your Study Material")

        uploaded_file = st.file_uploader(
            "Upload PDF (Notes, Textbook, Paper, etc.)",
            type=['pdf'],
            help="Upload any PDF to start learning"
        )

        if uploaded_file is not None:
            with st.spinner("Processing your PDF..."):
                pdf_path, pdf_hash, pdf_name = process_uploaded_pdf(uploaded_file)

                if pdf_path and pdf_hash:
                    if st.session_state.current_pdf_hash != pdf_hash:
                        st.session_state.current_pdf = pdf_path
                        st.session_state.current_pdf_hash = pdf_hash
                        st.session_state.current_pdf_name = pdf_name
                        st.session_state.rag = load_rag_with_pdf(pdf_path)
                        st.session_state.pdf_loaded = True
                        st.session_state.messages = []
                        st.session_state.quiz = None
                        st.session_state.summary = None
                        st.session_state.flashcards = None
                        st.rerun()

                    if st.session_state.pdf_loaded:
                        st.success(f"PDF Loaded: {pdf_name}")
                        st.caption(f"Size: {uploaded_file.size / 1024:.1f} KB")
        else:
            st.info("Upload a PDF to get started!")

        st.divider()

        st.markdown("### Settings")

        st.markdown("**Theme**")
        theme_col1, theme_col2 = st.columns(2)

        with theme_col1:
            if st.button("Light", use_container_width=True, key="theme_light"):
                st.session_state.theme = "light"
                st.rerun()

        with theme_col2:
            if st.button("Dark", use_container_width=True, key="theme_dark"):
                st.session_state.theme = "dark"
                st.rerun()

        st.caption(f"Current: {st.session_state.theme.upper()}")

        st.divider()

        if st.session_state.pdf_loaded:
            st.markdown("**AI Personality**")
            st.session_state.personality = st.selectbox(
                "Choose your assistant:",
                ["Friendly Genie", "Teacher", "Professor", "Exam Expert"],
                label_visibility="collapsed"
            )

            st.markdown("**Difficulty Level**")
            st.session_state.difficulty = st.selectbox(
                "Select difficulty:",
                ["Easy", "Medium", "Hard"],
                label_visibility="collapsed"
            )

            st.markdown("**Explain Like**")
            st.session_state.explain_style = st.selectbox(
                "Explanation style:",
                ["Beginner", "Normal", "College", "Professional"],
                label_visibility="collapsed"
            )

            st.divider()

            st.markdown("**Quick Actions**")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Summary", use_container_width=True):
                    with st.spinner("Summarizing..."):
                        try:
                            if st.session_state.rag:
                                summary = st.session_state.rag.summarize_document()
                                st.session_state.summary = summary
                                st.toast("Summary ready!")
                        except Exception as e:
                            st.error(f"Error: {e}")

            with col2:
                if st.button("Flashcards", use_container_width=True):
                    with st.spinner("Creating..."):
                        try:
                            if st.session_state.rag:
                                flashcards = st.session_state.rag.generate_flashcards()
                                st.session_state.flashcards = flashcards
                                st.toast("Flashcards ready!")
                        except Exception as e:
                            st.error(f"Error: {e}")

            col3, col4 = st.columns(2)
            with col3:
                if st.button("Quiz", use_container_width=True):
                    with st.spinner("Generating..."):
                        try:
                            if st.session_state.rag:
                                quiz_data = st.session_state.rag.generate_quiz()
                                st.session_state.quiz = json.loads(quiz_data)
                                st.session_state.quiz_submitted = False
                                st.session_state.quiz_answers = {}
                                st.session_state.total_quizzes += 1
                                add_xp(5)
                                st.toast("Quiz ready!")
                        except Exception as e:
                            st.error(f"Error: {e}")

            with col4:
                if st.button("Clear All", use_container_width=True):
                    st.session_state.messages = []
                    st.session_state.quiz = None
                    st.session_state.summary = None
                    st.session_state.flashcards = None
                    st.toast("Cleared!")
                    st.rerun()

    # Main Content
    if not st.session_state.pdf_loaded:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
    """<div class="welcome-container">
<h2 style="font-size: 2.5em; margin-bottom: 20px;">Welcome to EduGenie AI</h2>

<p style="font-size: 1.2em; color: #666; margin-bottom: 40px;">
Start by uploading your study material (PDF) from the sidebar
</p>

<div class="feature-box">
<h3>What You Can Do</h3>
<ul style="text-align: left; max-width: 500px; margin: 20px auto; line-height: 1.8;">
<li><strong>Chat:</strong> Ask questions about your PDF</li>
<li><strong>Quizzes:</strong> Generate practice questions</li>
<li><strong>Flashcards:</strong> Create learning cards</li>
<li><strong>Summarize:</strong> Get key points instantly</li>
<li><strong>Gamify:</strong> Earn XP and unlock badges</li>
</ul>
</div>

<p style="margin-top: 40px; color: #999;">
Works with any PDF: textbooks, notes, papers, assignments, etc.
</p>
</div>""",
    unsafe_allow_html=True,
)
    else:
        # STATS ROW
        stat_col1, stat_col2, stat_col3, stat_col4, stat_col5 = st.columns(5, gap="small")

        with stat_col1:
            st.markdown(f"""
            <div class="stat-card-box">
                <h4 style="margin: 0; font-size: 0.9em; opacity: 0.9;">Questions</h4>
                <p style="margin: 10px 0 0 0; font-size: 2em; font-weight: bold;">{st.session_state.total_questions}</p>
            </div>
            """, unsafe_allow_html=True)

        with stat_col2:
            st.markdown(f"""
            <div class="stat-card-box">
                <h4 style="margin: 0; font-size: 0.9em; opacity: 0.9;">Quizzes</h4>
                <p style="margin: 10px 0 0 0; font-size: 2em; font-weight: bold;">{st.session_state.total_quizzes}</p>
            </div>
            """, unsafe_allow_html=True)

        with stat_col3:
            st.markdown(f"""
            <div class="stat-card-box">
                <h4 style="margin: 0; font-size: 0.9em; opacity: 0.9;">Level</h4>
                <p style="margin: 10px 0 0 0; font-size: 2em; font-weight: bold;">{st.session_state.level}</p>
            </div>
            """, unsafe_allow_html=True)

        with stat_col4:
            st.markdown(f"""
            <div class="stat-card-box">
                <h4 style="margin: 0; font-size: 0.9em; opacity: 0.9;">Streak</h4>
                <p style="margin: 10px 0 0 0; font-size: 2em; font-weight: bold;">{st.session_state.streak_days}</p>
            </div>
            """, unsafe_allow_html=True)

        with stat_col5:
            avg = int(sum(st.session_state.quiz_scores) / len(st.session_state.quiz_scores)) if st.session_state.quiz_scores else 0
            st.markdown(f"""
            <div class="stat-card-box">
                <h4 style="margin: 0; font-size: 0.9em; opacity: 0.9;">Avg Score</h4>
                <p style="margin: 10px 0 0 0; font-size: 2em; font-weight: bold;">{avg}%</p>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # TABS
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "Chat", "Quiz", "Flashcards", "Summary",
            "Level & XP", "Achievements", "Progress", "Tools"
        ])

        # TAB 1: CHAT
        with tab1:
            st.markdown("### Chat with EduGenie")

            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
                    if "source" in msg and msg["source"]:
                        st.markdown(f"""
                        <div class="source-citation">
                            Source: {msg['source']} | Page: {msg.get('page', '1')}
                        </div>
                        """, unsafe_allow_html=True)

            user_input = st.chat_input("Ask me anything about your study material...")

            if user_input:
                st.session_state.total_questions += 1
                add_xp(5)
                st.session_state.mood = detect_mood(user_input)
                st.session_state.messages.append({"role": "user", "content": user_input})

                with st.chat_message("user"):
                    st.write(user_input)

                with st.chat_message("assistant"):
                    st.info(f"{st.session_state.personality} is thinking...")
                    time.sleep(0.8)

                    try:
                        response = st.session_state.rag.ask(user_input)

                        clean_response, source_name, page_num = clean_source_path(
                            response,
                            st.session_state.current_pdf_name
                        )

                        st.write(clean_response)

                        st.markdown(f"""
                        <div class="source-citation">
                            Source: {source_name} | Page: {page_num}
                        </div>
                        """, unsafe_allow_html=True)

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": clean_response,
                            "source": source_name,
                            "page": page_num
                        })
                    except Exception as e:
                        st.error(f"Error: {e}")

        # TAB 2: QUIZ
        with tab2:
            st.markdown("### Practice Quiz")

            if st.session_state.quiz is None:
                st.info("Generate a quiz from sidebar!")
            else:
                if not st.session_state.quiz_submitted:
                    for i, q in enumerate(st.session_state.quiz):
                        st.write(f"**Q{i+1}: {q.get('question')}**")
                        ans = st.radio("", q.get('options', []), key=f"q_{i}", label_visibility="collapsed")
                        st.session_state.quiz_answers[i] = ans

                    if st.button("Submit Quiz", use_container_width=True):
                        score = sum(1 for i, q in enumerate(st.session_state.quiz)
                                  if st.session_state.quiz_answers.get(i) == q.get('answer'))
                        percentage = int((score / len(st.session_state.quiz)) * 100)
                        st.session_state.quiz_submitted = True
                        st.session_state.quiz_scores.append(percentage)
                        add_xp(20)
                        st.rerun()
                else:
                    score = st.session_state.quiz_scores[-1]

                    if score == 100:
                        st.balloons()
                        st.success(f"Perfect Score! {score}%")
                        add_xp(50)
                    else:
                        st.markdown(f"### Your Score: {score}%")

                    for i, q in enumerate(st.session_state.quiz):
                        is_correct = st.session_state.quiz_answers.get(i) == q.get('answer')
                        if is_correct:
                            st.success(f"Q{i+1}: Correct!")
                        else:
                            st.error(f"Q{i+1}: Wrong")

                    if st.button("Retry Quiz", use_container_width=True):
                        st.session_state.quiz_submitted = False
                        st.session_state.quiz_answers = {}
                        st.rerun()

        # TAB 3: FLASHCARDS
        with tab3:
            st.markdown("### Flashcards")
            if st.session_state.flashcards:
                st.write(st.session_state.flashcards)
            else:
                st.info("Generate flashcards from sidebar!")

        # TAB 4: SUMMARY
        with tab4:
            st.markdown("### Document Summary")
            if st.session_state.summary:
                st.write(st.session_state.summary)
            else:
                st.info("Generate summary from sidebar!")

        # TAB 5: LEVEL & XP
        with tab5:
            st.markdown("### Level & XP System")
            xp_in_level = st.session_state.xp % 100
            st.markdown(f"""
            <div style="text-align: center;">
                <h2 style="color: #667eea;">Level {st.session_state.level}</h2>
                <div style="background: #eee; height: 20px; border-radius: 10px; margin: 15px 0; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #667eea, #764ba2);
                                height: 100%; width: {xp_in_level}%;"></div>
                </div>
                <p style="font-size: 1.1em;"><strong>{xp_in_level}/100 XP</strong></p>
            </div>
            """, unsafe_allow_html=True)

            st.info(f"""
            **XP Progress:**
            - Current XP: {st.session_state.xp}
            - Level: {st.session_state.level}
            - Next Level: {(st.session_state.level * 100)} XP

            **Earn XP by:**
            - +5 XP per question
            - +20 XP per quiz
            - +50 XP for perfect quiz
            """)

        # TAB 6: ACHIEVEMENTS
        with tab6:
            st.markdown("### Achievements Unlocked")
            check_achievements()

            cols = st.columns(3)
            for i, (key, badge) in enumerate(st.session_state.all_badges.items()):
                with cols[i % 3]:
                    if badge["earned"]:
                        st.markdown(f"""
                        <div class="badge-unlocked">
                            <h3 style="margin: 0; font-size: 2.5em;">{badge['emoji']}</h3>
                            <p style="margin: 8px 0 0 0; font-weight: bold;">{badge['name']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="badge-locked">
                            <h3 style="margin: 0; font-size: 2em;">🔒</h3>
                            <p style="margin: 8px 0 0 0; font-size: 0.9em;">{badge['requirement']}</p>
                        </div>
                        """, unsafe_allow_html=True)

        # TAB 7: PROGRESS
        with tab7:
            st.markdown("### Your Learning Progress")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Questions", st.session_state.total_questions)
            with col2:
                st.metric("Quizzes Completed", st.session_state.total_quizzes)
            with col3:
                avg = int(sum(st.session_state.quiz_scores) / len(st.session_state.quiz_scores)) if st.session_state.quiz_scores else 0
                st.metric("Average Score", f"{avg}%")

            if st.session_state.quiz_scores:
                st.markdown("**Score Progression:**")
                st.line_chart(st.session_state.quiz_scores)

        # TAB 8: TOOLS
        with tab8:
            st.markdown("### Additional Tools")

            tool = st.selectbox("Select a tool:", [
                "Explain Like...",
                "Mood Support",
                "Study Tips",
                "Concept Deep Dive"
            ])

            if tool == "Explain Like...":
                st.markdown(f"**Style:** {st.session_state.explain_style}")
                topic = st.text_input("Topic to explain:")
                if topic:
                    st.info(f"Explaining '{topic}' in {st.session_state.explain_style} level...")
                    time.sleep(0.8)
                    st.write("(AI would provide explanation tailored to this style)")

            elif tool == "Mood Support":
                st.write(f"**Your Current Mood:** {st.session_state.mood.upper()}")
                if st.session_state.mood == "stressed":
                    st.warning("I sense you're stressed. Let's break concepts into smaller, manageable chunks!")
                elif st.session_state.mood == "happy":
                    st.success("Great energy! Let's keep the momentum going and tackle more topics!")
                else:
                    st.info("Ready to learn? Let's explore together!")

            elif tool == "Study Tips":
                st.markdown("""
                **Smart Study Tips:**
                - Take quizzes after learning each topic
                - Review difficult areas multiple times
                - Use flashcards for quick recall
                - Take breaks every 25 minutes (Pomodoro)
                - Explain concepts in your own words
                """)

            elif tool == "Concept Deep Dive":
                concept = st.text_input("Enter a concept to explore deeply:")
                if concept:
                    st.info(f"Deep diving into '{concept}'...")
                    time.sleep(0.8)
                    st.write("(AI would provide comprehensive explanation with examples)")

        # FOOTER
        st.markdown("""
        <div style="text-align: center; margin-top: 60px; padding: 30px; border-top: 1px solid #eee;">
            <p style="color: #999; font-size: 0.95em;">
                EduGenie AI - Your AI-Powered Learning Assistant
            </p>
            <p style="color: #bbb; font-size: 0.85em; margin-top: 10px;">
                Transform your learning with intelligent study tools
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
