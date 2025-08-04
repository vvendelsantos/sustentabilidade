# Arquivo: streamlit_sempi.py

import streamlit as st
from utils import formatar_nota_br, calcular_media_ponderada
from templates import (
    gerar_html_desclassificacao,
    gerar_html_aprovacao,
    gerar_html_reprovacao,
    gerar_html_lembrete_envio,
    gerar_html_lembrete_apresentacao,
    gerar_html_resultado_final
)

st.set_page_config(page_title="Gerador de HTML SEMPI", layout="wide")
st.title("📑 Notificações e Avaliações - VII SEMPI")

abas = [
    "Desclassificação",
    "Aprovação",
    "Reprovação",
    "Lembretes",
    "Resultado final"
]

aba = st.sidebar.radio("Selecione a aba:", abas)

if aba == "Desclassificação":
    st.header("Desclassificação")
    motivos = st.text_area("Motivos (separe por '/'):", value="X/ Y/ Z")
    motivos_lista = [m.strip() for m in motivos.split("/") if m.strip()]
    html = gerar_html_desclassificacao(motivos_lista)
    st.code(html, language="html")

elif aba == "Aprovação":
    from sections.aprovacao import interface_aprovacao
    interface_aprovacao()

elif aba == "Reprovação":
    from sections.reprovacao import interface_reprovacao
    interface_reprovacao()

elif aba == "Lembretes":
    st.header("Lembretes")
    texto_envio = st.text_area("Texto do lembrete de envio:", value="...HTML...")
    tempo_apresentacao = st.number_input("Minutos de apresentação", 1, 60, 10)
    tempo_arguicao = st.number_input("Minutos de arguição", 1, 30, 5)
    st.subheader("HTML - Envio")
    st.code(gerar_html_lembrete_envio(texto_envio), language="html")
    st.subheader("HTML - Apresentação")
    st.code(gerar_html_lembrete_apresentacao(tempo_apresentacao, tempo_arguicao), language="html")

elif aba == "Resultado final":
    from sections.resultado_final import interface_resultado_final
    interface_resultado_final()
