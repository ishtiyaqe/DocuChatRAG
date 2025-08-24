import requests
from django.conf import settings
from .prompts import SYSTEM_INSTRUCTIONS, PROMPT_TEMPLATE

class ModelClient:
    def __init__(self):
        # OpenAI
        self.openai_key = settings.OPENAI_API_KEY
        self.openai_model = settings.OPENAI_MODEL or "gpt-4o-mini"

        # Ollama
        self.ollama_host = (settings.OLLAMA_HOST or "http://localhost:11434/api/generate").strip().strip('"')
        self.ollama_model = settings.LOCAL_MODEL or "llama3"

    def _format_prompt(self, context, question, max_length=4000):
        if isinstance(context, list):
            full_context = "\n\n".join(chunk.get('chunk', '') for chunk in context)
        else:
            full_context = str(context)
        full_context = full_context[:max_length]

        return PROMPT_TEMPLATE.format(
            system=SYSTEM_INSTRUCTIONS,
            context=full_context,
            question=question
        )

    def answer(self, context, question, prefer_openai=True):
        prompt = self._format_prompt(context, question)

        if prefer_openai and self.openai_key:
            try:
                return self._ask_openai(prompt)
            except Exception as e:
                print(f"OpenAI failed, falling back to Ollama: {e}")

        return self._ask_ollama(prompt)

    def _ask_openai(self, prompt):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.openai_model,
            "messages": [
                {"role": "system", "content": SYSTEM_INSTRUCTIONS},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500,
            "temperature": 0.2
        }

        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    def _ask_ollama(self, prompt):
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": self.ollama_model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(self.ollama_host, headers=headers, json=payload, timeout=260)
        response.raise_for_status()
        return response.json().get("response", "").strip()
