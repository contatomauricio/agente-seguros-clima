"""Modelos de dados compartilhados entre os agentes do pipeline.

Cada agente do grafo (LangGraph) recebe e devolve um dicionário de estado.
Aqui definimos, com Pydantic, o "formato" de cada peça de informação que
circula por esse estado, para deixar o contrato entre etapas explícito.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Segurado(BaseModel):
    id: int
    nome: str
    cidade: str
    uf: str
    zona_costeira: bool
    tipo_apolice: str  # "residencial" | "automovel" | "ambos"
    email_simulado: str
    telefone_simulado: str


class WeatherData(BaseModel):
    cidade: str
    uf: Optional[str] = None
    temperatura_c: float
    chuva_mm_3h: float = 0.0
    vento_kmh: float = 0.0
    descricao: str = ""
    coletado_em: datetime = Field(default_factory=datetime.utcnow)


class EventoDetectado(BaseModel):
    cidade: str
    tipo_evento: str  # "chuva_intensa" | "granizo" | "vento_forte" | "onda_calor" | "risco_enchente"
    severidade: str  # "baixa" | "media" | "alta"
    detalhe: str


class SeguradoSelecionado(BaseModel):
    segurado: Segurado
    evento: EventoDetectado
    motivo: str


class Notificacao(BaseModel):
    segurado_id: int
    nome: str
    cidade: str
    canal_simulado: str  # "email" | "sms"
    evento: str
    severidade: str
    mensagem: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PipelineState(BaseModel):
    """Estado que trafega pelo grafo, enriquecido a cada nó."""

    segurados: list[Segurado] = Field(default_factory=list)
    weather_by_city: dict[str, WeatherData] = Field(default_factory=dict)
    eventos: list[EventoDetectado] = Field(default_factory=list)
    selecionados: list[SeguradoSelecionado] = Field(default_factory=list)
    notificacoes: list[Notificacao] = Field(default_factory=list)
    erros: list[str] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True
