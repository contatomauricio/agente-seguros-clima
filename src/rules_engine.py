"""Agente 3 — Rules Engine.

Cruza os eventos detectados com a base de segurados e decide quem deve
ser notificado, de acordo com a tabela de regras de negócio da spec
técnica (seção 5).
"""

from __future__ import annotations

from .state import EventoDetectado, Segurado, SeguradoSelecionado

# Para cada tipo de evento, quais tipos de apólice são elegíveis a receber
# a notificação. "ambos" sempre é elegível.
REGRAS_APOLICE: dict[str, set[str]] = {
    "chuva_intensa": {"residencial"},
    "risco_enchente": {"residencial"},
    "granizo": {"automovel"},
    "onda_calor": {"residencial"},
    # vento_forte tem regra especial: automóvel em qualquer lugar,
    # OU residencial apenas se o segurado estiver em zona costeira.
}


def _elegivel(segurado: Segurado, evento: EventoDetectado) -> tuple[bool, str]:
    tipo_apolice = segurado.tipo_apolice.lower()
    apolices_do_segurado = {tipo_apolice} if tipo_apolice != "ambos" else {"residencial", "automovel"}

    if evento.tipo_evento == "vento_forte":
        if "automovel" in apolices_do_segurado:
            return True, "apólice de automóvel + vento forte na região"
        if "residencial" in apolices_do_segurado and segurado.zona_costeira:
            return True, "apólice residencial em zona costeira + vento forte"
        return False, ""

    apolices_elegiveis = REGRAS_APOLICE.get(evento.tipo_evento, set())
    if apolices_do_segurado & apolices_elegiveis:
        return True, f"apólice {tipo_apolice} elegível para evento '{evento.tipo_evento}'"

    return False, ""


def select_segurados(
    eventos: list[EventoDetectado], segurados: list[Segurado]
) -> list[SeguradoSelecionado]:
    selecionados: list[SeguradoSelecionado] = []

    for evento in eventos:
        segurados_da_cidade = [s for s in segurados if s.cidade == evento.cidade]
        for segurado in segurados_da_cidade:
            ok, motivo = _elegivel(segurado, evento)
            if ok:
                selecionados.append(
                    SeguradoSelecionado(segurado=segurado, evento=evento, motivo=motivo)
                )

    return selecionados
