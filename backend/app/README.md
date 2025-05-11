
# 🧠 Backend - RAG-Powered News Chatbot

This is the backend service that powers the RAG-based chatbot for retrieving and generating news content. The backend is built with **FastAPI** and integrates document databases, embedding models, and generative LLMs to serve intelligent responses.

---

## 📁 Folder Structure

```
backend/
├── app/
│   ├── database/
│   │   ├── chroma_client.py
│   │   └── redis_client.py
│   ├── models/
│   │   ├── chat.py
│   │   ├── session.py
│   ├── routes/
│   │   ├── chat.py
│   │   ├── news.py
│   │   └── session.py
│   ├── services/
│   │   ├── chat_service.py
│   │   ├── embedding_service.py
│   │   ├── gemini_service.py
│   │   ├── news_service.py
│   │   └── rag_service.py
│   └── utils/
├── .env
├── config.py
```

---

## ⚙️ Working Pipeline

### 1. **API Routing Layer (`routes/`)**

- `chat.py`: Receives user queries and routes them to the RAG pipeline.
- `news.py`: Provides access to news-related endpoints.
- `session.py`: Manages user session logic (if applicable).

### 2. **Service Layer (`services/`)**

- `chat_service.py`: Handles chat logic, integrates session history and RAG inference.
- `embedding_service.py`: Generates embeddings using a specified model.
- `gemini_service.py`: Interacts with Gemini or another LLM to generate final answers.
- `news_service.py`: Retrieves or manages structured news data.
- `rag_service.py`: Central orchestrator for retrieval and generation logic.

### 3. **Database Layer (`database/`)**

- `chroma_client.py`: Connects to a ChromaDB vector store for retrieval.
- `redis_client.py`: Optional fast-access cache or session store.

### 4. **Data Models (`models/`)**

- Pydantic models for request/response schemas.
- Defines chat and session data structures.

---

## 🔧 Environment Variables (`.env`)

```env
OPENAI_API_KEY=your_openai_key
CHROMA_DB_PATH=./chroma
REDIS_URL=redis://localhost:6379
```

---

## 🚀 How to Run

```bash
cd backend
pip install -r requirements.txt
uvicorn app.routes.chat:app --reload
```

Make sure to update the `.env` file with valid API keys and DB paths.

---

## ✅ Features

- Vector DB retrieval (ChromaDB)
- Redis caching for speed
- Modular and scalable architecture
- RAG + LLM pipeline integration
- RESTful API endpoints

---

## 🧠 Future Improvements

- Add support for multiple LLMs (OpenAI, Cohere, Gemini)
- Advanced session management with user tracking
- Asynchronous processing with background tasks
- Logging and monitoring tools

---

## 📜 License

MIT License
