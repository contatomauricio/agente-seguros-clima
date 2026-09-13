"""Executa o pipeline completo via linha de comando, sem interface gráfica.

Uso:
    python main.py
"""

from __future__ import annotations

from dotenv import load_dotenv

from src.data_loader import load_segurados
from src.graph import run_pipeline


def main() -> None:
    load_dotenv()

    segurados = load_segurados()
    print(f"[1/5] {len(segurados)} segurados carregados de data/segurados.csv")

    estado = run_pipeline(segurados)

    print(f"[2/5] Clima coletado para {len(estado.weather_by_city)} cidades:")
    for cidade, w in estado.weather_by_city.items():
        print(f"       - {cidade}: {w.temperatura_c:.1f}°C, chuva {w.chuva_mm_3h:.1f}mm/3h, vento {w.vento_kmh:.1f}km/h — {w.descricao}")

    print(f"[3/5] {len(estado.eventos)} eventos climáticos detectados:")
    for e in estado.eventos:
        print(f"       - {e.cidade}: {e.tipo_evento} (severidade {e.severidade}) — {e.detalhe}")

    print(f"[4/5] {len(estado.selecionados)} segurados selecionados pelo motor de regras:")
    for sel in estado.selecionados:
        print(f"       - {sel.segurado.nome} ({sel.segurado.tipo_apolice}) — {sel.motivo}")

    print(f"[5/5] {len(estado.notificacoes)} notificações simuladas geradas (ver output/notificacoes_simuladas.json):")
    for n in estado.notificacoes:
        print(f"       - [{n.canal_simulado.upper()}] {n.nome} ({n.cidade}): {n.mensagem}")


if __name__ == "__main__":
    main()
