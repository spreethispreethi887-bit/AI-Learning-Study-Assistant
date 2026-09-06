import streamlit as st
import ollama

from memory import save_memory, get_memories
from rag import add_pdf_to_rag, search_documents
from tools import calculate, create_study_plan


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Learning Study Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Learning Study Assistant")
st.write("Your AI-powered college study assistant")


# -----------------------------
# Student Name
# -----------------------------
name = st.query_params.get("name", "")
name = st.text_input("👤 Enter your name", value=name)

if name:
    st.success(f"Welcome, {name}! 😊")


# -----------------------------
# RAG - Upload Study Material
# -----------------------------
st.header("📖 Upload Study Material")

pdf_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

if st.button("➕ Add PDF to Knowledge Base"):
    if pdf_file:
        with st.spinner("Reading and indexing your PDF..."):
            try:
                result = add_pdf_to_rag(pdf_file)
                st.success(f"PDF added successfully! {result}")
            except Exception as e:
                st.error(f"Could not add PDF: {e}")
    else:
        st.warning("Please upload a PDF first.")


# -----------------------------
# Ask Question
# -----------------------------
st.header("💬 Ask Your Question")

question = st.text_area(
    "Enter your study question",
    height=120
)


# -----------------------------
# AI Answer
# -----------------------------
if st.button("🤖 Get Answer"):

    if not question:
        st.warning("Please enter a question.")

    else:

        with st.spinner("AI is thinking..."):

            # Search PDF knowledge base
            try:
                documents = search_documents(question)
            except Exception:
                documents = []

            # Get previous memories
            try:
                memories = get_memories(name) if name else []
            except Exception:
                memories = []

            # Convert results to text
            if isinstance(documents, list):
                context = "\n\n".join(str(item) for item in documents)
            else:
                context = str(documents)

            if isinstance(memories, list):
                memory_text = "\n".join(str(item) for item in memories)
            else:
                memory_text = str(memories)

            # -----------------------------
            # Tools
            # -----------------------------
            tool_result = ""

            # Calculator tool
            if question.lower().startswith("calculate "):
                expression = question[10:].strip()
                tool_result = calculate(expression)

            # Study plan tool
            elif "study plan" in question.lower():

                subject = question

                tool_result = create_study_plan(
                    subject,
                    4
                )

            # -----------------------------
            # Prompt
            # -----------------------------
            prompt = f"""
You are an intelligent college study assistant.

Student name:
{name}

Previous memory:
{memory_text}

Study material from the student's PDF:
{context}

Tool result:
{tool_result}

Student question:
{question}

Instructions:
1. Answer clearly and simply.
2. Prefer information from the student's study material when available.
3. Use previous memory when useful.
4. If a tool result is available, use it.
5. Give a beginner-friendly explanation.
6. Use examples when helpful.
"""

            # -----------------------------
            # Ollama AI
            # -----------------------------
            response = ollama.chat(
                model="llama3.2:3b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            answer = response["message"]["content"]

        # -----------------------------
        # Display Answer
        # -----------------------------
        st.subheader("🤖 AI Assistant")
        st.write(answer)

        # -----------------------------
        # Save Memory
        # -----------------------------
        try:
            save_memory(question, answer)
        except Exception:
            try:
                save_memory(name, question, answer)
            except Exception:
                pass


# -----------------------------
# Features
# -----------------------------
st.divider()

st.subheader("✨ Project Features")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info("🧠 Memory")

with col2:
    st.info("📚 RAG")

with col3:
    st.info("🛠️ Tools")

with col4:
    st.info("🤖 Ollama")