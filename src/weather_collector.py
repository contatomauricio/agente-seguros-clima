"""Agente 1 — Weather Collector.

Consulta a API pública do OpenWeatherMap (endpoint "Current Weather Data")
para cada cidade presente na base de segurados e normaliza a resposta em
um objeto WeatherData interno, simples de consumir pelos próximos agentes.
"""

from __future__ import annotations

import os

import requests

from .state import WeatherData

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

# Ativado via SIMULAR_EVENTOS_EXTREMOS=true no .env, substitui o clima real
# dessas cidades por cenários fixos que estouram os thresholds do
# event_detector, útil para testar a geração/envio de mensagens sem depender
# do clima de verdade no momento da execução.
_CENARIOS_DEMO: dict[str, WeatherData] = {
    "São Paulo": WeatherData(
        cidade="São Paulo", uf="SP", temperatura_c=24.0, chuva_mm_3h=32.0,
        vento_kmh=18.0, descricao="chuva intensa simulada para demonstração",
    ),
    "Fortaleza": WeatherData(
        cidade="Fortaleza", uf="CE", temperatura_c=29.0, chuva_mm_3h=2.0,
        vento_kmh=75.0, descricao="vento forte simulado para demonstração",
    ),
    "Teresina": WeatherData(
        cidade="Teresina", uf="PI", temperatura_c=41.0, chuva_mm_3h=0.0,
        vento_kmh=10.0, descricao="onda de calor simulada para demonstração",
    ),
    "Santos": WeatherData(
        cidade="Santos", uf="SP", temperatura_c=22.0, chuva_mm_3h=5.0,
        vento_kmh=20.0, descricao="chuva de granizo simulada para demonstração",
    ),
}


def collect_weather(cidade: str, uf: str | None = None) -> WeatherData:
    """Busca o clima atual de uma cidade brasileira no OpenWeatherMap.

    Se a chamada falhar (sem chave configurada, API fora do ar, cidade não
    encontrada), devolve um WeatherData "vazio" em vez de estourar exceção,
    para o pipeline nunca travar durante uma demonstração.
    """

    if os.getenv("SIMULAR_EVENTOS_EXTREMOS", "").strip().lower() == "true" and cidade in _CENARIOS_DEMO:
        return _CENARIOS_DEMO[cidade]

    api_key = os.getenv("OPENWEATHER_API_KEY", "")
    query = f"{cidade},BR" if uf is None else f"{cidade},{uf},BR"

    if not api_key:
        return WeatherData(
            cidade=cidade,
            uf=uf,
            temperatura_c=0.0,
            chuva_mm_3h=0.0,
            vento_kmh=0.0,
            descricao="sem chave de API configurada (OPENWEATHER_API_KEY)",
        )

    try:
        resp = requests.get(
            OPENWEATHER_URL,
            params={
                "q": query,
                "appid": api_key,
                "units": "metric",
                "lang": "pt_br",
            },
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()

        chuva_mm = 0.0
        if "rain" in data:
            chuva_mm = data["rain"].get("3h", data["rain"].get("1h", 0.0))

        vento_ms = data.get("wind", {}).get("speed", 0.0)
        vento_kmh = vento_ms * 3.6

        descricao = ""
        if data.get("weather"):
            descricao = data["weather"][0].get("description", "")

        return WeatherData(
            cidade=cidade,
            uf=uf,
            temperatura_c=data.get("main", {}).get("temp", 0.0),
            chuva_mm_3h=chuva_mm,
            vento_kmh=vento_kmh,
            descricao=descricao,
        )
    except requests.RequestException as exc:
        return WeatherData(
            cidade=cidade,
            uf=uf,
            temperatura_c=0.0,
            chuva_mm_3h=0.0,
            vento_kmh=0.0,
            descricao=f"erro ao consultar OpenWeatherMap: {exc}",
        )


def collect_weather_for_cities(cidades_uf: list[tuple[str, str | None]]) -> dict[str, WeatherData]:
    """Coleta o clima para uma lista de (cidade, uf), retornando um dict por cidade."""

    resultado: dict[str, WeatherData] = {}
    for cidade, uf in cidades_uf:
        resultado[cidade] = collect_weather(cidade, uf)
    return resultado
