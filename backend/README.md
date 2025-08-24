# 📚 DocuChatRAG

DocuChatRAG is a full-stack web application that allows users to **upload documents** (TXT, PDF, DOCX) and **ask natural language questions** about their contents.  
The backend is powered by **Django + Django REST Framework**, the frontend is built with **React + Tailwind CSS**, and the AI model integration supports **OpenAI API** or a **local model (HuggingFace/Faiss)**.

---

## 🚀 Features
- Upload a document and convert it into a searchable knowledge base.
- Ask natural language questions, get answers grounded in the uploaded file.
- Supports multiple file formats: `.txt`, `.pdf`, `.docx`.
- AI Integration:
  - **Option 1:** Use OpenAI API (if API key is provided).
  - **Option 2:** Use a local HuggingFace model (fallback if no key or API limit).
- JWT Authentication (bonus).
- Stores uploaded documents & Q&A history in PostgreSQL (via Django ORM).
- Dockerized for easy deployment.

---

## 🛠️ Tech Stack
**Backend**
- Django + Django REST Framework
- PostgreSQL (can switch to SQLite for dev)
- LangChain + HuggingFace + OpenAI API

**Frontend**
- React (Vite) + Tailwind CSS
- Axios for API calls
- JWT Authentication flow

**Infra**
- Docker + docker-compose
- Gunicorn + Nginx for production

---

## ⚡ Getting Started

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/docuchatrag.git
cd docuchatrag


### 2️⃣ Setup Backend
cd backend
cp .env.example .env   # Add your configs here


Django will be available at:
👉 http://localhost:8000/api/
