"""Agente 4 — Message Generator.

Para cada segurado selecionado pelo Rules Engine, monta um prompt
contextualizado e chama o LLM (via llm_provider) para gerar uma mensagem
curta e personalizada de alerta preventivo.
"""

from __future__ import annotations

from .llm_provider import generate_message
from .state import SeguradoSelecionado

RECOMENDACOES_PADRAO = {
    "chuva_intensa": "verifique se calhas e ralos estão desobstruídos e evite deixar objetos de valor em áreas baixas",
    "risco_enchente": "desligue aparelhos elétricos próximos ao chão e mantenha um kit de emergência pronto",
    "granizo": "guarde o veículo em garagem coberta, se possível",
    "vento_forte": "reforce objetos soltos em quintais e varandas, e redobre a atenção ao dirigir",
    "onda_calor": "evite deixar aparelhos superaquecendo e mantenha-se hidratado",
}


def _fallback_message(item: SeguradoSelecionado) -> str:
    recomendacao = RECOMENDACOES_PADRAO.get(
        item.evento.tipo_evento, "tome os cuidados preventivos recomendados pela Defesa Civil"
    )
    return (
        f"Olá {item.segurado.nome.split()[0]}, identificamos risco de "
        f"{item.evento.tipo_evento.replace('_', ' ')} em {item.evento.cidade} "
        f"nas próximas horas. Recomendamos: {recomendacao}. Sua seguradora está de olho em você."
    )


def generate_personalized_message(item: SeguradoSelecionado) -> str:
    primeiro_nome = item.segurado.nome.split()[0]
    prompt = (
        "Você é o assistente de comunicação de uma seguradora brasileira. "
        "Escreva uma única mensagem curta (máximo 3 frases, tom cordial e direto, "
        "sem emojis) para alertar preventivamente um segurado sobre um evento climático, "
        "incluindo 1 recomendação prática.\n\n"
        f"Nome do segurado: {primeiro_nome}\n"
        f"Cidade: {item.evento.cidade}\n"
        f"Tipo de apólice: {item.segurado.tipo_apolice}\n"
        f"Evento detectado: {item.evento.tipo_evento.replace('_', ' ')} (severidade {item.evento.severidade})\n"
        f"Detalhe técnico do evento: {item.evento.detalhe}\n"
    )
    return generate_message(prompt, fallback=_fallback_message(item))


def generate_messages(selecionados: list[SeguradoSelecionado]) -> list[tuple[SeguradoSelecionado, str]]:
    return [(item, generate_personalized_message(item)) for item in selecionados]
