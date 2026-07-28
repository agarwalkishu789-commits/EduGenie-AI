import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from backend.pdf_loader import PDFLoader
from backend.vector_store import VectorStore
from backend.rag import RAGEngine

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI Study Assistant")
st.caption("Ask questions, summarize documents, and generate quizzes using AI.")

if not GOOGLE_API_KEY:
    st.error("Google API Key not found in .env file.")
    st.stop()

pdf_path = Path("data/raw/study_material.pdf")

if not pdf_path.exists():
    st.error("study_material.pdf not found inside data/raw/")
    st.stop()


@st.cache_resource
def load_rag():
    loader = PDFLoader()
    chunks = loader.process_pdf(pdf_path)

    vector_db = VectorStore(GOOGLE_API_KEY)
    vector_db.create_vector_store(chunks)

    return RAGEngine(GOOGLE_API_KEY)


rag = load_rag()

st.divider()

question = st.text_input(
    "💬 Ask a question from your study material:",
    placeholder="Example: What is Data Science?"
)

col1, col2, col3 = st.columns(3)

with col1:
    ask_btn = st.button("🔍 Get Answer", use_container_width=True)

with col2:
    summary_btn = st.button("📝 Summarize Document", use_container_width=True)

with col3:
    quiz_btn = st.button("🧠 Generate Quiz", use_container_width=True)


if ask_btn and question:

    with st.spinner("Searching documents..."):
        answer = rag.ask(question)

    st.success("Answer Generated")

    st.markdown("### 💡 Answer")
    st.write(answer)

elif summary_btn:

    with st.spinner("Generating summary..."):
        summary = rag.summarize_document()

    st.success("Summary Generated")

    st.markdown("### 📄 Document Summary")
    st.write(summary)

elif quiz_btn:

    with st.spinner("Generating Quiz..."):
        quiz = rag.generate_quiz()

    st.success("Quiz Generated")

    st.markdown("### 🧠 Quiz")
    st.write(quiz)