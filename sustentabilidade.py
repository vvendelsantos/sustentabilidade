import streamlit as st
import pandas as pd
import re

# -----------------------------
# PALAVRAS-CHAVE POR SEGMENTO
# -----------------------------
SEGMENTOS = {
    "Energias Alternativas": ["solar", "eólica", "fotovoltaica", "biogás", "biocombustível", "energia renovável", "célula combustível"],
    "Transportes Sustentáveis": ["veículo elétrico", "híbrido", "célula combustível", "hidrogênio", "freios regenerativos"],
    "Conservação de Energia": ["armazenamento de energia", "iluminação eficiente", "isolamento térmico", "recuperação de energia"],
    "Gestão de Resíduos": ["tratamento de resíduos", "efluente", "reciclagem", "resíduos sólidos", "reuso de água", "controle de poluição"],
    "Agricultura Sustentável": ["irrigação", "reflorestamento", "fertilizante orgânico", "pesticida alternativo", "melhoria do solo"]
}

ODS_MAPEAMENTO = {
    "Energias Alternativas": [7, 13],
    "Transportes Sustentáveis": [9, 11],
    "Conservação de Energia": [7, 12],
    "Gestão de Resíduos": [6, 12, 13],
    "Agricultura Sustentável": [2, 12, 15]
}

# -----------------------------
# FUNÇÕES PRINCIPAIS
# -----------------------------
def classificar_segmento(texto):
    texto = texto.lower()
    resultado = {}
    for segmento, palavras in SEGMENTOS.items():
        score = sum(1 for palavra in palavras if re.search(rf"\\b{re.escape(palavra)}\\b", texto))
        if score > 0:
            resultado[segmento] = score
    return resultado

def classificar_sustentabilidade(score_dict):
    if not score_dict:
        return "Indefinido", [], []
    segmento_principal = max(score_dict, key=score_dict.get)
    pontuacao_total = sum(score_dict.values())
    if pontuacao_total >= 3:
        return "Sustentável (Alta Confiança)", [segmento_principal], ODS_MAPEAMENTO[segmento_principal]
    elif pontuacao_total == 2:
        return "Potencialmente Sustentável", [segmento_principal], ODS_MAPEAMENTO[segmento_principal]
    else:
        return "Indefinido", [], []

# -----------------------------
# INTERFACE STREAMLIT
# -----------------------------
st.set_page_config(page_title="Classificador de Patentes Verdes", layout="wide")
st.title("🌱 Classificador de Sustentabilidade Tecnológica em Pedidos de Patente")
st.markdown("""
Este protótipo analisa o texto técnico de um pedido de patente e indica seu potencial de alinhamento com a sustentabilidade, 
com base no inventário da OMPI e ODS associados.
""")

# Entrada do texto
txt_input = st.text_area("📄 Insira o texto técnico ou resumo do pedido de patente:", height=300)

if st.button("🔍 Analisar Texto"):
    if not txt_input.strip():
        st.warning("Por favor, insira um texto válido.")
    else:
        with st.spinner("Analisando..."):
            scores = classificar_segmento(txt_input)
            resultado, segmentos, ods = classificar_sustentabilidade(scores)

        st.subheader("🔎 Resultado da Classificação")
        st.write(f"**Classificação:** {resultado}")
        if segmentos:
            st.write(f"**Segmento Principal:** {segmentos[0]}")
            st.write(f"**ODS Relacionados:** {', '.join(['ODS ' + str(o) for o in ods])}")

        st.subheader("📊 Pontuação por Segmento")
        if scores:
            df = pd.DataFrame(list(scores.items()), columns=["Segmento", "Pontuação"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhum termo sustentável detectado no texto.")

st.markdown("---")
st.caption("Protótipo acadêmico - Desenvolvido para avaliação preliminar de sustentabilidade em PI")
