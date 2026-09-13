"""Carrega a base fictícia de segurados a partir do CSV em data/."""

from __future__ import annotations

import csv
import os

from .state import Segurado

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "segurados.csv")


def load_segurados(path: str = DEFAULT_PATH) -> list[Segurado]:
    segurados: list[Segurado] = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            segurados.append(
                Segurado(
                    id=int(row["id"]),
                    nome=row["nome"],
                    cidade=row["cidade"],
                    uf=row["uf"],
                    zona_costeira=row["zona_costeira"].strip().lower() == "true",
                    tipo_apolice=row["tipo_apolice"].strip().lower(),
                    email_simulado=row["email_simulado"],
                    telefone_simulado=row["telefone_simulado"],
                )
            )
    return segurados
