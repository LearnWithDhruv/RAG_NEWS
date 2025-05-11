
# 📰 RAG-Powered News Chatbot

This is a full-stack application that provides an interactive chatbot interface to explore and retrieve news articles using Retrieval-Augmented Generation (RAG). The app is built with **React** (frontend) and connects to a **Python backend** that powers the RAG model.

---

## 📁 Folder Structure (Frontend)

```
frontend/
├── public/
├── src/
│   ├── assets/
│   │   └── icons/
│   │       └── react.svg
│   ├── components/
│   │   ├── ChatInterface.jsx
│   │   ├── NewsList.jsx
│   │   └── SearchBar.jsx
│   ├── hooks/
│   │   └── useChat.js
│   ├── pages/
│   │   └── Home.jsx
│   ├── services/
│   │   └── api.js
│   ├── styles/
│   │   ├── main.css
│   ├── App.css
│   ├── App.jsx
│   ├── index.css
│   ├── main.jsx
├── .env
├── .gitignore
├── eslint.config.js
├── index.html
```

---

## ⚙️ Working Pipeline

### 1. **User Interface (React Frontend)**

- **Home.jsx**: Main landing page.
- **ChatInterface.jsx**: Displays the chatbot conversation UI.
- **SearchBar.jsx**: Optional component for keyword-based filtering.
- **NewsList.jsx**: Renders fetched news results in a scrollable list.

### 2. **Custom Hook: `useChat.js`**

- Manages chat input, state, and API integration.
- Sends user input to backend and receives the response.
- Handles loading states and error feedback.

### 3. **API Communication (`services/api.js`)**

- Centralized Axios or `fetch` wrapper to interact with the backend.
- Handles POST requests to the RAG-powered backend endpoint (e.g., `/api/chat`).
  
Example:
```js
export const sendMessage = async (message) => {
  const res = await fetch("http://localhost:5000/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query: message }),
  });
  return res.json();
};
```

### 4. **Backend RAG Pipeline (Assumed)**

- Accepts queries via REST API.
- Retrieves relevant documents from a vector DB (e.g., FAISS, Pinecone).
- Passes documents + query to a language model (e.g., OpenAI, Cohere, Mistral).
- Returns a generated response.

### 5. **Styling**

- Global styles via `main.css`, `App.css`.
- Tailwind CSS or traditional styles supported.

---

## 🛠️ Installation

```bash
git clone https://github.com/your-repo/news-chatbot
cd frontend
npm install
npm run dev
```

Make sure your backend is running on the expected port (usually `localhost:5000`).

---

## 🔧 Environment Variables (`.env`)

```env
VITE_BACKEND_URL=http://localhost:5000
```

---

## ✅ Features

- Chat-based interface for news exploration
- RAG-based answer generation
- Real-time API integration
- Modular, clean component structure

---

## 🧠 Future Improvements

- User authentication
- Search history
- Speech-to-text integration
- Better error handling

---

## 📜 License

MIT License
