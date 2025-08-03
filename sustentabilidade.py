import streamlit as st
import pandas as pd

# --------------------
# Configurações do Jogo
# --------------------
st.set_page_config(
    page_title="Gestor de Patentes Verdes",
    page_icon="🌱",
    layout="wide",
)

# --------------------
# Inicialização de Estado (Estado da Sessão)
# --------------------
# Usamos o `st.session_state` para armazenar variáveis entre as rodadas.
# Isso garante que o orçamento e os indicadores não resetem toda vez que a página é atualizada.
if "budget" not in st.session_state:
    st.session_state.budget = 1000  # Orçamento inicial
if "patents_registered" not in st.session_state:
    st.session_state.patents_registered = []
if "sustainability_score" not in st.session_state:
    st.session_state.sustainability_score = 0
if "financial_return" not in st.session_state:
    st.session_state.financial_return = 0

# --------------------
# Dados do Jogo (Patentes)
# --------------------
# Usamos um DataFrame do Pandas para armazenar as informações das patentes.
patents = {
    "name": [
        "Filtro de Água de Carbono Bio-Ativo",
        "Processo de Reciclagem de Plástico Ultrassônico",
        "Bateria de Íon de Sódio para Veículos",
        "Algoritmo de Otimização de Logística",
        "Material de Embalagem Biodegradável",
        "Cabo de Fibra Ótica de Alta Velocidade",
        "Fertilizante Orgânico de Liberação Lenta",
    ],
    "cost": [150, 200, 300, 100, 120, 250, 180],
    "financial_impact": [200, 250, 400, 150, 160, 350, 220],
    "sustainability_impact": [10, 8, 9, 3, 7, 2, 9],
}

patents_df = pd.DataFrame(patents)

# --------------------
# Lógica do Jogo
# --------------------
def register_patent(patent_name):
    """Função que registra uma patente, atualizando o estado do jogo."""
    patent_info = patents_df[patents_df["name"] == patent_name].iloc[0]
    
    if st.session_state.budget >= patent_info["cost"]:
        st.session_state.budget -= patent_info["cost"]
        st.session_state.financial_return += patent_info["financial_impact"]
        st.session_state.sustainability_score += patent_info["sustainability_impact"]
        st.session_state.patents_registered.append(patent_name)
        st.success(f"Patente '{patent_name}' registrada com sucesso!")
    else:
        st.error("Orçamento insuficiente para registrar esta patente.")

# Função para reiniciar o jogo
def reset_game():
    st.session_state.budget = 1000
    st.session_state.patents_registered = []
    st.session_state.sustainability_score = 0
    st.session_state.financial_return = 0
    st.experimental_rerun()


# --------------------
# Interface do Usuário (UI)
# --------------------
st.title("🌱 Gestor de Patentes Verdes")
st.markdown("""
Bem-vindo ao simulador de inovação! Seu desafio é equilibrar o **retorno financeiro** e o **impacto sustentável** da sua empresa, decidindo quais patentes registrar com um orçamento limitado.
""")

st.sidebar.title("Informações do Jogo")
st.sidebar.metric("Orçamento", f"R$ {st.session_state.budget}")
st.sidebar.metric("Retorno Financeiro Total", f"R$ {st.session_state.financial_return}")
st.sidebar.metric("Pontuação de Sustentabilidade", st.session_state.sustainability_score)

# Botão para reiniciar o jogo na barra lateral
st.sidebar.button("Reiniciar Jogo", on_click=reset_game)

st.subheader("Patentes Disponíveis")

# Mostra as patentes em um DataFrame
st.dataframe(patents_df, use_container_width=True)

# Cria os botões para registrar patentes
st.markdown("---")
st.subheader("Tome sua decisão:")
patents_to_register = [p for p in patents_df["name"] if p not in st.session_state.patents_registered]

cols = st.columns(len(patents_to_register))
for i, patent_name in enumerate(patents_to_register):
    with cols[i]:
        st.button(f"Registrar: {patent_name}", key=patent_name, on_click=register_patent, args=(patent_name,))

st.markdown("---")
st.subheader("Resultados do Jogo")

# Gráfico de barras comparando os indicadores
data_for_chart = pd.DataFrame(
    {
        "Indicador": ["Retorno Financeiro", "Pontuação de Sustentabilidade"],
        "Valor": [st.session_state.financial_return, st.session_state.sustainability_score],
    }
)
st.bar_chart(data_for_chart, x="Indicador", y="Valor")

# Exibe as patentes já registradas
st.markdown("---")
if st.session_state.patents_registered:
    st.subheader("Patentes Registradas:")
    for patent in st.session_state.patents_registered:
        st.success(f"- {patent}")
else:
    st.info("Nenhuma patente registrada ainda.")
