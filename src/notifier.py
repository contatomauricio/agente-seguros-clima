"""Agente 5 — Notification Simulator.

Não envia nada de verdade. Registra cada notificação simulada em memória
e persiste tudo em output/notificacoes_simuladas.json ao final, para servir
de evidência do fluxo completo no relatório/demo.
"""

from __future__ import annotations

import json
import os
from datetime import datetime

from .state import Notificacao, SeguradoSelecionado

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "output", "notificacoes_simuladas.json")


def _escolher_canal(item: SeguradoSelecionado) -> str:
    # Regra simples de demonstração: eventos de alta severidade viram SMS
    # (mais rápido de ler), o resto vira e-mail.
    return "sms" if item.evento.severidade == "alta" else "email"


def simular_envio(pares: list[tuple[SeguradoSelecionado, str]]) -> list[Notificacao]:
    notificacoes: list[Notificacao] = []

    for item, mensagem in pares:
        notificacoes.append(
            Notificacao(
                segurado_id=item.segurado.id,
                nome=item.segurado.nome,
                cidade=item.evento.cidade,
                canal_simulado=_escolher_canal(item),
                evento=item.evento.tipo_evento,
                severidade=item.evento.severidade,
                mensagem=mensagem,
            )
        )

    return notificacoes


def salvar_notificacoes(notificacoes: list[Notificacao]) -> str:
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    payload = [n.model_dump(mode="json") for n in notificacoes]
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return OUTPUT_PATH
