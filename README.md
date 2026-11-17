# RAG Application

An AI-powered Retrieval-Augmented Generation (RAG) application that allows users to interact with documents and retrieve relevant information using semantic search and generative AI.

## 🚀 Features

- Document-based question answering
- Text extraction and processing
- Semantic search using vector embeddings
- Vector storage with ChromaDB
- Google Gemini embeddings integration
- Relevant context retrieval for user queries

## 🛠️ Tech Stack

- **Language:** Python
- **Backend:** FastAPI
- **AI/LLM:** Google Gemini
- **Embeddings:** Google Generative AI Embeddings
- **Vector Database:** ChromaDB
- **Framework:** LangChain

## 📁 Project Structure

```text
RAG Application/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── .env
│   └── myvenv/
├── README.md
└── .gitignore
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Adityahon3344/RAG-Application.git
cd RAG-Application
```

### 2. Navigate to backend

```bash
cd backend
```

### 3. Create and activate virtual environment

```bash
python3 -m venv myvenv
source myvenv/bin/activate
```

### 4. Install dependencies

```bash
pip install fastapi uvicorn python-dotenv langchain-chroma langchain-google-genai
```

### 5. Configure environment variables

Create a `.env` file inside the backend folder:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Never upload your actual API key to GitHub.

### 6. Run the application

```bash
python -m uvicorn main:app --reload
```

Open: http://127.0.0.1:8000

## 👨‍💻 Author

**Aditya Ashok Hon**

B.Tech – Artificial Intelligence and Machine Learning

GitHub: [Adityahon3344](https://github.com/Adityahon3344)

---

⭐ If you find this project useful, consider giving it a star!