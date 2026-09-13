"""Agente 2 — Event Detector.

Aplica thresholds simples sobre os dados meteorológicos normalizados para
classificar eventos de interesse do negócio de seguros. Os limiares estão
documentados na spec técnica (seção 5 — Regras de negócio) e podem ser
ajustados livremente aqui.
"""

from __future__ import annotations

from .state import EventoDetectado, WeatherData

CHUVA_INTENSA_MM = 20.0
VENTO_FORTE_KMH = 60.0
ONDA_CALOR_C = 38.0


def detect_events(weather: WeatherData) -> list[EventoDetectado]:
    eventos: list[EventoDetectado] = []

    if weather.chuva_mm_3h > CHUVA_INTENSA_MM:
        eventos.append(
            EventoDetectado(
                cidade=weather.cidade,
                tipo_evento="chuva_intensa",
                severidade="alta",
                detalhe=f"{weather.chuva_mm_3h:.1f} mm previstos em 3h (limite: {CHUVA_INTENSA_MM} mm)",
            )
        )

    if weather.vento_kmh > VENTO_FORTE_KMH:
        eventos.append(
            EventoDetectado(
                cidade=weather.cidade,
                tipo_evento="vento_forte",
                severidade="media",
                detalhe=f"{weather.vento_kmh:.1f} km/h previstos (limite: {VENTO_FORTE_KMH} km/h)",
            )
        )

    if weather.temperatura_c > ONDA_CALOR_C:
        eventos.append(
            EventoDetectado(
                cidade=weather.cidade,
                tipo_evento="onda_calor",
                severidade="baixa",
                detalhe=f"{weather.temperatura_c:.1f}°C registrados (limite: {ONDA_CALOR_C}°C)",
            )
        )

    if "granizo" in weather.descricao.lower() or "hail" in weather.descricao.lower():
        eventos.append(
            EventoDetectado(
                cidade=weather.cidade,
                tipo_evento="granizo",
                severidade="alta",
                detalhe=f"condição reportada pela API: '{weather.descricao}'",
            )
        )

    return eventos


def detect_events_for_all(weather_by_city: dict[str, WeatherData]) -> list[EventoDetectado]:
    eventos: list[EventoDetectado] = []
    for weather in weather_by_city.values():
        eventos.extend(detect_events(weather))
    return eventos
