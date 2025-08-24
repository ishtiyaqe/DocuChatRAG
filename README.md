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


---

## ⚡ Getting Started 
Clone the repo:  
```bash
git clone https://github.com/ishtiyaqe/DocuChatRAG.git
cd DocuChatRAG

# Backend run
cd backend
python3.13 -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver localhost:8000

# Frontend run
cd frontend
npm install
npm run dev

### You need to run this for local model if not have open ai key
# Setup Local Model
sudo snap install ollama
# Pull LLaMA 3
ollama pull llama3

# Start Ollama server
ollama serve
