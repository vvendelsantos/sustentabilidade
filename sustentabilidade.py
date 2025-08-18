# =================================================================================
# Documentação Completa do Código
# =================================================================================

# Este script cria um painel interativo de gráficos usando a biblioteca Streamlit.
# Ele utiliza pandas para a manipulação de dados e plotly.express para a visualização dos gráficos.
# Os dados são criados diretamente no script, mas podem ser facilmente substituídos
# por dados carregados de um arquivo (por exemplo, CSV, Excel, etc.).

# ---------------------------------------------------------------------------------
# 1. Importar as bibliotecas necessárias
# ---------------------------------------------------------------------------------
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------------------------------
# 2. Configuração da página do Streamlit
# ---------------------------------------------------------------------------------
# Define o título da página e o layout. O layout 'wide' utiliza toda a largura da tela.
st.set_page_config(page_title="Painel de Análise de Dados", layout="wide")

# =================================================================================
# 3. Preparação dos dados
# =================================================================================
# Criamos DataFrames do pandas a partir dos dados fornecidos nas imagens.
# A coluna 'N' foi renomeada para 'Contagem' para ser mais descritiva.

# Dados para o gráfico de Países
data_paises = {
    'País': ['BR', 'US', 'EP', 'CN', 'JP', 'NO', 'ES', 'KR'],
    'Contagem': [187, 34, 5, 4, 3, 2, 1, 1]
}
df_paises = pd.DataFrame(data_paises)

# Dados para o gráfico de Titulares
data_titulares = {
    'Titular': ['PETROLEO BRASILEIRO S.A.', 'JOAO BATISTA MAGLIA', 'INSTITUTO PRESBITERIANO MACKENZIE', 'UNICAMP', 'UNIV MINAS GERAIS'],
    'Contagem': [13, 6, 4, 3, 3]
}
df_titulares = pd.DataFrame(data_titulares)

# Dados para o gráfico de Códigos IPC
data_ipc = {
    'Código IPC': ['C02F1/44', 'A01K61/00', 'C02F9/00', 'F03B13/14', 'C02F1/32'],
    'Contagem': [7, 6, 6, 5, 5]
}
df_ipc = pd.DataFrame(data_ipc)

# Dados para o gráfico de Anos
data_anos = {
    'Ano': [1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1994, 1995, 1996, 1997, 1998, 1999, 2001, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'Contagem': [2, 2, 3, 1, 4, 4, 5, 3, 2, 1, 2, 4, 9, 1, 1, 1, 5, 18, 19, 15, 28, 26, 18, 2, 9, 1, 4, 10, 3, 4, 2, 3, 3, 8, 10, 3, 1]
}
df_anos = pd.DataFrame(data_anos)

# =================================================================================
# 4. Criação dos Gráficos com Plotly Express
# =================================================================================

# Gráfico de barras para Países
fig_paises = px.bar(df_paises,
                    x='País',
                    y='Contagem',
                    title='Distribuição por País',
                    color_discrete_sequence=px.colors.qualitative.Plotly)

# Gráfico de barras para Titulares (limitar o nome para melhor visualização)
# Adiciona um hover_name para mostrar o nome completo no tooltip
fig_titulares = px.bar(df_titulares,
                       x='Titular',
                       y='Contagem',
                       title='Distribuição por Titular',
                       color_discrete_sequence=px.colors.qualitative.Plotly)
fig_titulares.update_traces(text=df_titulares['Titular'])
fig_titulares.update_layout(xaxis_title='Titular',
                            showlegend=False)

# Gráfico de barras para Códigos IPC
fig_ipc = px.bar(df_ipc,
                 x='Código IPC',
                 y='Contagem',
                 title='Distribuição por Código IPC',
                 color_discrete_sequence=px.colors.qualitative.Plotly)

# Gráfico de linha para Anos (evolução ao longo do tempo)
fig_anos = px.line(df_anos,
                   x='Ano',
                   y='Contagem',
                   title='Evolução ao Longo do Tempo (Anos)',
                   markers=True)
fig_anos.update_traces(line_color='rgb(102, 194, 165)')

# =================================================================================
# 5. Criar o layout do painel (Dashboard)
# =================================================================================

# Título principal do painel
st.title("Painel de Gráficos de Dados")
st.markdown("Este painel exibe visualizações interativas de diferentes conjuntos de dados.")

# Utiliza colunas para dispor os gráficos lado a lado
col1, col2 = st.columns(2)

# Exibe o primeiro e o segundo gráfico na primeira coluna
with col1:
    st.header("Gráfico 1: Países")
    st.plotly_chart(fig_paises, use_container_width=True)

    st.header("Gráfico 2: Códigos IPC")
    st.plotly_chart(fig_ipc, use_container_width=True)

# Exibe o terceiro e o quarto gráfico na segunda coluna
with col2:
    st.header("Gráfico 3: Titulares")
    st.plotly_chart(fig_titulares, use_container_width=True)

    st.header("Gráfico 4: Evolução Temporal")
    st.plotly_chart(fig_anos, use_container_width=True)

# ---------------------------------------------------------------------------------
# 6. Instruções de Implementação
# ---------------------------------------------------------------------------------
# Para executar este código, salve-o como um arquivo .py (por exemplo, app.py).
# Em seguida, abra o terminal na mesma pasta e execute o comando:
# streamlit run app.py
#
# Isso iniciará um servidor web local e abrirá o painel no seu navegador padrão.
# Você pode interagir com os gráficos (zoom, pan, hover) diretamente no painel.
# =================================================================================
