"""Camada de abstração sobre o provedor de LLM.

Isola o resto do pipeline de qual serviço gera o texto. Hoje usa o Google
Gemini (tier gratuito via Google AI Studio), mas basta trocar o corpo de
`generate_message` para apontar para outro provedor (ex.: Groq) sem mexer
em mais nada do projeto. Se a chamada falhar por qualquer motivo (sem
chave, sem internet, cota estourada), cai num template local, para a
demonstração nunca travar.
"""

from __future__ import annotations

import os

_gemini_model = None


def _get_gemini_model():
    global _gemini_model
    if _gemini_model is not None:
        return _gemini_model

    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        return None

    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        _gemini_model = genai.GenerativeModel(model_name)
        return _gemini_model
    except Exception:
        return None


def generate_message(prompt: str, fallback: str) -> str:
    """Gera texto via Gemini; usa `fallback` se algo der errado."""

    model = _get_gemini_model()
    if model is None:
        return fallback

    try:
        response = model.generate_content(prompt)
        texto = (response.text or "").strip()
        return texto if texto else fallback
    except Exception:
        return fallback
