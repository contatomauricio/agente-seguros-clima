"""Dashboard Streamlit — interface gráfica do agente.

Camada fina por cima de src/graph.py: nenhuma regra de negócio mora aqui,
só a apresentação visual das etapas do pipeline. Rodar com:

    streamlit run app.py
"""

from __future__ import annotations

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from src.data_loader import load_segurados
from src.graph import run_pipeline

load_dotenv()

st.set_page_config(page_title="Agente de Alerta Climático - Seguros", layout="wide")

st.title("🌦️ Agente de Comunicação Proativa com Segurados")
st.caption(
    "Monitora eventos meteorológicos, aplica regras de negócio e gera mensagens "
    "personalizadas simuladas, sem envio real de SMS, e-mail ou push."
)

segurados = load_segurados()

with st.sidebar:
    st.header("Base de segurados")
    st.write(f"{len(segurados)} segurados carregados")
    st.dataframe(
        pd.DataFrame([s.model_dump() for s in segurados]),
        hide_index=True,
        use_container_width=True,
    )
    rodar = st.button("▶️ Rodar monitoramento agora", type="primary", use_container_width=True)

if not rodar:
    st.info("Use o botão na barra lateral para rodar o pipeline completo.")
    st.stop()

with st.spinner("Consultando clima, detectando eventos e gerando mensagens..."):
    estado = run_pipeline(segurados)

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Dados meteorológicos coletados")
    weather_rows = [
        {
            "cidade": w.cidade,
            "temperatura_c": w.temperatura_c,
            "chuva_mm_3h": w.chuva_mm_3h,
            "vento_kmh": w.vento_kmh,
            "descrição": w.descricao,
        }
        for w in estado.weather_by_city.values()
    ]
    st.dataframe(pd.DataFrame(weather_rows), hide_index=True, use_container_width=True)

with col2:
    st.subheader("2. Eventos detectados")
    if estado.eventos:
        cores = {"alta": "🔴", "media": "🟡", "baixa": "🟢"}
        for e in estado.eventos:
            st.markdown(f"{cores.get(e.severidade, '⚪')} **{e.cidade}** - {e.tipo_evento} ({e.severidade}): {e.detalhe}")
    else:
        st.write("Nenhum evento relevante detectado no momento.")

st.subheader("3. Segurados selecionados pelo motor de regras")
if estado.selecionados:
    sel_rows = [
        {
            "segurado": s.segurado.nome,
            "cidade": s.evento.cidade,
            "apólice": s.segurado.tipo_apolice,
            "evento": s.evento.tipo_evento,
            "motivo": s.motivo,
        }
        for s in estado.selecionados
    ]
    st.dataframe(pd.DataFrame(sel_rows), hide_index=True, use_container_width=True)
else:
    st.write("Nenhum segurado precisa ser notificado agora.")

st.subheader("4. Notificações simuladas")
if estado.notificacoes:
    for n in estado.notificacoes:
        canal_icone = "📱" if n.canal_simulado == "sms" else "📧"
        with st.container(border=True):
            st.markdown(f"{canal_icone} **{n.nome}** - {n.cidade} · canal simulado: `{n.canal_simulado}` · evento: `{n.evento}`")
            st.write(n.mensagem)
    st.success(f"{len(estado.notificacoes)} notificações simuladas, registradas em output/notificacoes_simuladas.json")
else:
    st.write("Nenhuma notificação foi gerada nesta execução.")
