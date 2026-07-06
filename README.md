# 🎥 YouTube Multilingual RAG Chatbot

A Retrieval-Augmented Generation (RAG) based chatbot that allows users to ask questions about any YouTube video. The application automatically extracts video transcripts, creates semantic chunks, generates embeddings, stores them in a FAISS vector database, and uses an Ollama LLM to answer user questions.

---

## 🚀 Features

- 📺 Load any YouTube video using its URL
- 🌍 Supports multiple transcript languages
- 📝 Automatic transcript extraction
- ✂️ Intelligent transcript chunking
- 🔍 Semantic search using FAISS
- 🧠 Sentence Transformer embeddings
- 🤖 Local LLM inference using Ollama (Phi-3 Mini)
- 💬 Interactive Streamlit interface
- 📚 Displays retrieved transcript sources with timestamps

---

## 🛠️ Tech Stack

| Component | Technology |
|------------|------------|
| Frontend | Streamlit |
| Language | Python |
| Transcript Extraction | youtube-transcript-api |
| Embedding Model | sentence-transformers (all-MiniLM-L6-v2) |
| Vector Database | FAISS |
| LLM | Ollama (phi3:mini) |
| Retrieval | RAG |

---

## 📂 Project Structure

```
YouTube-RAG/
│
├── app.py
│
├── data/
│   └── transcripts/
│
├── utils/
│   ├── youtube_loader.py
│   ├── helper.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vector_db.py
│   └── rag.py
│
├── requirements.txt
│
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/YouTube-RAG.git

cd YouTube-RAG
```

---

### 2. Create a virtual environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Install Ollama

Download Ollama from

https://ollama.com/

Pull the Phi-3 Mini model

```bash
ollama pull phi3:mini
```

Start Ollama

```bash
ollama serve
```

---

### 5. Run the application

```bash
streamlit run app.py
```

---

## 📖 How It Works

### Step 1

Paste any YouTube video URL.

↓

### Step 2

The application extracts the available transcript.

↓

### Step 3

Transcript is divided into semantic chunks.

↓

### Step 4

Embeddings are generated using Sentence Transformers.

↓

### Step 5

Embeddings are stored in a FAISS vector database.

↓

### Step 6

For every user question,

- Similar transcript chunks are retrieved.
- Retrieved chunks are sent to the LLM.
- Ollama generates an answer grounded in the video content.

---

## 🧠 Architecture

```
YouTube URL
      │
      ▼
Transcript Extraction
      │
      ▼
Transcript Chunking
      │
      ▼
Sentence Embeddings
      │
      ▼
FAISS Vector Store
      │
      ▼
User Question
      │
      ▼
Similarity Search
      │
      ▼
Retrieved Context
      │
      ▼
Ollama (Phi3 Mini)
      │
      ▼
Generated Answer
```

---

## 📦 Required Packages

- streamlit
- youtube-transcript-api
- sentence-transformers
- faiss-cpu
- requests
- numpy

Install using

```bash
pip install -r requirements.txt
```

---

## 💡 Example

### Input

```
https://www.youtube.com/watch?v=VIDEO_ID
```

Question

```
What is the main topic discussed in the video?
```

Output

```
The video explains Retrieval-Augmented Generation (RAG), including transcript extraction,
semantic search, FAISS indexing, and answer generation using an LLM.
```

---

## 📸 Screenshots
<img width="1917" height="922" alt="image" src="https://github.com/user-attachments/assets/ae043f47-f15e-482f-b00c-e3f5cb7dea98" />
<img width="1912" height="912" alt="image" src="https://github.com/user-attachments/assets/c8cf89af-bc50-4d0a-8d32-f05615932eb2" />


---

## 🔮 Future Improvements

- 🎙️ Audio transcription for videos without subtitles
- 🌐 Translation support
- 📄 PDF summary generation
- 💾 Persistent FAISS database
- 🖥️ Multi-video chat
- 📱 Responsive UI
- 🔊 Voice-based interaction

---

## 👨‍💻 Author

Praneetha 

B.Tech Artificial Intelligence & Machine Learning

BMS College of Engineering

---

