# DocuChatRAG
**Document Chat with Retrieval‑Augmented Generation**  
Support for both **OpenAI** and **local LLaMA via Ollama**. DocuChatRAG enables chat-based querying of documents using a RAG approach. It supports OpenAI cloud API or local LLaMA via Ollama. Features include document chunking, vector search, prompt formatting, and fallback between models.

## Setup
**Prerequisites:** Python 3.10+, pip, Git, Ollama (optional for local model).  
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