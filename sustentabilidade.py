# app.py
import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Classificador de Patentes Verdes", layout="wide")
st.title("🌱 Classificador de Sustentabilidade de Pedidos de Patente")

st.markdown("""
Este aplicativo visa apoiar Núcleos de Inovação Tecnológica (NITs) na identificação de pedidos de patente com potencial classificação como **patente verde**, com base em critérios técnicos e temáticos do inventário da OMPI.
""")

# ========================
# DEFINIÇÕES DE PALAVRAS-CHAVE E PESOS
# ========================
segmentos = {
    "Energias alternativas": {
        "palavras": ["fotovoltaic", "energia solar", "solar térmica", "biocombustível", "bioetanol", "biodiesel", "célula combustível", "energia eólica", "biogás", "energia hidráulica"],
        "peso": 2
    },
    "Transportes sustentáveis": {
        "palavras": ["veículo elétrico", "híbrido", "célula combustível", "propulsão solar", "freio regenerativo"],
        "peso": 1
    },
    "Conservação de energia": {
        "palavras": ["armazenamento de energia", "isolamento térmico", "iluminação eficiente", "medição de energia"],
        "peso": 1
    },
    "Gerenciamento de resíduos": {
        "palavras": ["reciclagem", "tratamento de resíduos", "gases residuais", "fertilizante", "esgoto", "aterro", "resíduo industrial"],
        "peso": 1
    },
    "Agricultura sustentável": {
        "palavras": ["irrigação", "fertilizante orgânico", "controle biológico", "reflorestamento", "pesticida alternativo"],
        "peso": 1
    },
}

# ========================
# FUNÇÕES
# ========================
def detectar_segmentos(texto):
    texto = texto.lower()
    resultados = []
    for segmento, dados in segmentos.items():
        for palavra in dados['palavras']:
            if re.search(rf"\\b{palavra}\\b", texto):
                resultados.append(segmento)
                break
    return list(set(resultados))

def pontuar_patente(texto, segmentos_detectados):
    pontuacao = 0
    for s in segmentos_detectados:
        pontuacao += segmentos[s]['peso']
    # Peso adicional por palavras de impacto
    impacto_extra = ["baixo carbono", "ods", "sustentabilidade", "economia circular"]
    if any(palavra in texto.lower() for palavra in impacto_extra):
        pontuacao += 1
    return pontuacao

# ========================
# INTERFACE DO APP
# ========================
st.subheader("1. Carregue ou cole o conteúdo do pedido de patente")

opcao = st.radio("Escolha a forma de entrada:", ["Upload de CSV", "Texto manual"])

if opcao == "Upload de CSV":
    arquivo = st.file_uploader("Envie um arquivo CSV com a coluna 'resumo'", type=["csv"])
    if arquivo:
        df = pd.read_csv(arquivo)
        if 'resumo' not in df.columns:
            st.error("O arquivo precisa ter uma coluna chamada 'resumo'.")
        else:
            with st.spinner("Classificando patentes..."):
                df['segmentos'] = df['resumo'].apply(detectar_segmentos)
                df['pontuacao'] = df.apply(lambda row: pontuar_patente(row['resumo'], row['segmentos']), axis=1)
                df['classificacao'] = df['pontuacao'].apply(lambda x: "Provável patente verde" if x >= 3 else "Indefinido")
            st.success("Análise concluída.")
            st.dataframe(df)
            st.download_button("📥 Baixar resultados", data=df.to_csv(index=False), file_name="resultado_patentes.csv")

elif opcao == "Texto manual":
    texto = st.text_area("Cole o resumo técnico do pedido de patente")
    if st.button("Analisar resumo"):
        segmentos_detectados = detectar_segmentos(texto)
        score = pontuar_patente(texto, segmentos_detectados)
        classificacao = "Provável patente verde" if score >= 3 else "Indefinido"

        st.markdown(f"**Segmentos detectados:** {', '.join(segmentos_detectados) if segmentos_detectados else 'Nenhum'}")
        st.markdown(f"**Pontuação:** {score}")
        st.markdown(f"**Classificação:** :green[{classificacao}]" if classificacao.startswith("Provável") else f"**Classificação:** :orange[{classificacao}]")
