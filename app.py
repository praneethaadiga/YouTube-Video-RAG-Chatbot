import streamlit as st
import os
import json
from utils.youtube_loader import YouTubeLoader
from utils.helper import extract_video_id
from utils.chunking import TranscriptChunker
from utils.embeddings import EmbeddingGenerator
from utils.vector_db import VectorDatabase
from utils.rag import RAG


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="YouTube RAG Chatbot",
    page_icon="🎥",
    layout="wide"
)

st.title("🎥 YouTube Video RAG Chatbot")
st.markdown(
    "Ask questions about any YouTube video using **RAG + FAISS + Ollama**."
)

st.divider()


# -----------------------------
# Session State
# -----------------------------
if "db" not in st.session_state:
    st.session_state.db = None

if "embedder" not in st.session_state:
    st.session_state.embedder = None

if "rag" not in st.session_state:
    st.session_state.rag = None

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "video_loaded" not in st.session_state:
    st.session_state.video_loaded = False


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("⚙️ Settings")

st.sidebar.success("Ollama Connected")

st.sidebar.write("Embedding Model")
st.sidebar.info("all-MiniLM-L6-v2")

st.sidebar.write("LLM")
st.sidebar.info("phi3:mini")


st.sidebar.divider()

st.sidebar.write("Project")

st.sidebar.markdown("""
- Transcript Extraction
- Chunking
- Embeddings
- FAISS Search
- Ollama LLM
""")


# -----------------------------
# Video Input
# -----------------------------
youtube_url = st.text_input(
    "Paste YouTube URL"
)


if st.button("📥 Load Video"):

    if youtube_url.strip() == "":
        st.error("Please enter a YouTube URL.")
        st.stop()

    try:

        with st.spinner("Downloading transcript..."):

            loader = YouTubeLoader()

            transcript_path = loader.save_transcript(
                youtube_url
            )

        video_id = extract_video_id(
            youtube_url
        )

        st.success("Transcript downloaded!")

        with st.spinner("Creating chunks..."):

            chunker = TranscriptChunker()

            chunks = chunker.create_chunks(
                transcript_path,
                video_id
            )

        st.success(f"{len(chunks)} chunks created.")

        with st.spinner("Loading embedding model..."):

            embedder = EmbeddingGenerator()

        with st.spinner("Generating embeddings..."):

            embeddings = embedder.embed_chunks(
                chunks
            )

        st.success("Embeddings generated.")

        db = VectorDatabase()

        db.build_index(
            embeddings,
            chunks
        )

        db.save()

        rag = RAG()

        st.session_state.db = db
        st.session_state.embedder = embedder
        st.session_state.rag = rag
        st.session_state.chunks = chunks
        st.session_state.video_loaded = True

        st.success("Video is ready for chatting!")

    except Exception as e:

        st.error(str(e))

    # ---------------------------------------------------
# Question Answering
# ---------------------------------------------------

st.divider()

st.header("💬 Ask Questions")

if st.session_state.video_loaded:

    question = st.text_input(
        "Enter your question"
    )

    if st.button("🚀 Ask"):

        if question.strip() == "":
            st.warning("Please enter a question.")
            st.stop()

        with st.spinner("Searching relevant information..."):

            query_embedding = st.session_state.embedder.embed_query(
                question
            )

            retrieved_chunks = st.session_state.db.search(
                query_embedding,
                top_k=4
            )

        with st.spinner("Generating answer with Ollama..."):

            answer = st.session_state.rag.answer(
                retrieved_chunks,
                question
            )

        st.divider()

        st.subheader("🤖 Answer")

        st.success(answer)

        st.divider()

        st.subheader("📚 Retrieved Sources")

        for i, chunk in enumerate(retrieved_chunks, start=1):

            minutes = int(chunk["start_time"] // 60)
            seconds = int(chunk["start_time"] % 60)

            with st.expander(
                f"Source {i} ({minutes}:{seconds:02d})"
            ):

                st.write(chunk["text"])

                youtube_link = (
                    f"https://www.youtube.com/watch?"
                    f"v={chunk['video_id']}&t={int(chunk['start_time'])}s"
                )

                st.markdown(
                    f"[▶ Open at {minutes}:{seconds:02d}]({youtube_link})"
                )

else:

    st.info(
        "Please load a YouTube video first."
    )

# ---------------------------------------------------
# Chat History
# ---------------------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


st.divider()

st.subheader("💬 Conversation")

if st.session_state.chat_history:

    for chat in st.session_state.chat_history:

        with st.chat_message("user"):
            st.write(chat["question"])

        with st.chat_message("assistant"):
            st.write(chat["answer"])

else:

    st.info("No conversation yet.")


# ---------------------------------------------------
# Store Chat History
# ---------------------------------------------------

if st.session_state.video_loaded:

    question = st.text_input(
        "Ask another question",
        key="chat_question"
    )

    if st.button(
        "Ask Again",
        use_container_width=True
    ):

        if question.strip() == "":
            st.warning("Please enter a question.")
            st.stop()

        with st.spinner("Searching..."):

            query_embedding = st.session_state.embedder.embed_query(
                question
            )

            retrieved_chunks = st.session_state.db.search(
                query_embedding,
                top_k=4
            )

            answer = st.session_state.rag.answer(
                retrieved_chunks,
                question
            )

        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": answer
            }
        )

        st.rerun()


# ---------------------------------------------------
# Sidebar Buttons
# ---------------------------------------------------

st.sidebar.divider()

if st.sidebar.button(
    "🗑 Clear Chat",
    use_container_width=True
):

    st.session_state.chat_history = []

    st.rerun()


if st.sidebar.button(
    "♻ Reset Video",
    use_container_width=True
):

    st.session_state.video_loaded = False

    st.session_state.db = None

    st.session_state.embedder = None

    st.session_state.rag = None

    st.session_state.chunks = None

    st.session_state.chat_history = []

    st.rerun()


# ---------------------------------------------------
# Footer
# ---------------------------------------------------

st.divider()

st.caption(
    "YouTube RAG Chatbot | Built using Streamlit, FAISS, Sentence Transformers and Ollama"
)