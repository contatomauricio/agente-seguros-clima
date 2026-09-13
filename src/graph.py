"""Orquestrador — monta o pipeline de 5 agentes como um grafo LangGraph.

O grafo é linear (cada nó depende do resultado do anterior), mas modelar
como StateGraph deixa explícita a separação entre coleta, processamento,
decisão e comunicação, e facilita adicionar bifurcações no futuro (ex.:
um nó de validação humana antes do envio).
"""

from __future__ import annotations

from langgraph.graph import END, StateGraph

from .event_detector import detect_events_for_all
from .message_generator import generate_messages
from .notifier import salvar_notificacoes, simular_envio
from .rules_engine import select_segurados
from .state import PipelineState
from .weather_collector import collect_weather_for_cities


def node_weather_collector(state: PipelineState) -> dict:
    cidades_uf = sorted({(s.cidade, s.uf) for s in state.segurados})
    weather_by_city = collect_weather_for_cities(cidades_uf)
    return {"weather_by_city": weather_by_city}


def node_event_detector(state: PipelineState) -> dict:
    eventos = detect_events_for_all(state.weather_by_city)
    return {"eventos": eventos}


def node_rules_engine(state: PipelineState) -> dict:
    selecionados = select_segurados(state.eventos, state.segurados)
    return {"selecionados": selecionados}


def node_message_generator(state: PipelineState) -> dict:
    pares = generate_messages(state.selecionados)
    notificacoes = simular_envio(pares)
    return {"notificacoes": notificacoes}


def node_notifier(state: PipelineState) -> dict:
    salvar_notificacoes(state.notificacoes)
    return {}


def build_graph():
    graph = StateGraph(PipelineState)

    graph.add_node("weather_collector", node_weather_collector)
    graph.add_node("event_detector", node_event_detector)
    graph.add_node("rules_engine", node_rules_engine)
    graph.add_node("message_generator", node_message_generator)
    graph.add_node("notifier", node_notifier)

    graph.set_entry_point("weather_collector")
    graph.add_edge("weather_collector", "event_detector")
    graph.add_edge("event_detector", "rules_engine")
    graph.add_edge("rules_engine", "message_generator")
    graph.add_edge("message_generator", "notifier")
    graph.add_edge("notifier", END)

    return graph.compile()


def run_pipeline(segurados) -> PipelineState:
    """Ponto de entrada usado tanto pelo main.py (CLI) quanto pelo app.py (Streamlit)."""

    app = build_graph()
    estado_inicial = PipelineState(segurados=segurados)
    resultado = app.invoke(estado_inicial)
    return PipelineState(**resultado)
