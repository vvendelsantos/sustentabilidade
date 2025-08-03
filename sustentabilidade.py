import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# ---------------------------
# 1. Título e Introdução
# ---------------------------
st.title("🔍 Classificador Didático de Patentes Sustentáveis")
st.markdown("""
Este protótipo educacional mostra como é possível utilizar **indicadores simples** para explorar a relação entre patentes tecnológicas e **sustentabilidade**, com base em palavras-chave e classificações IPC.
""")

# ---------------------------
# 2. Dados simulados
# ---------------------------
dados = pd.DataFrame({
    'Título': [
        'Sistema de geração de energia solar com alta eficiência',
        'Método de produção de plástico biodegradável a partir de algas',
        'Aquecedor solar compacto para residências urbanas',
        'Processo de dessalinização de água por osmose reversa',
        'Sistema híbrido de reaproveitamento de resíduos eletrônicos'
    ],
    'Resumo': [
        'Painel solar integrado com otimização automática.',
        'Uso de algas para polímeros sustentáveis.',
        'Tecnologia limpa para aquecimento doméstico.',
        'Solução de acesso à água potável usando energia limpa.',
        'Tecnologia circular para resíduos de eletrônicos.'
    ],
    'IPC': ['Y02E', 'C08L', 'F24J', 'C02F', 'H01M'],
    'Ano': [2022, 2021, 2020, 2023, 2024]
})

# ---------------------------
# 3. Lista de palavras-chave sustentáveis
# ---------------------------
keywords_verdes = ['solar', 'energia', 'biodegradável', 'algas', 'limpa', 'reciclagem', 'resíduos', 'sustentável', 'água', 'potável', 'renovável']
ipcs_verdes = ['Y02', 'C02', 'F24J']  # IPCs ambientais

# ---------------------------
# 4. Função de pontuação
# ---------------------------
def classificar_patente(titulo, resumo, ipc):
    score = 0
    texto = (titulo + ' ' + resumo).lower()
    
    score += sum(1 for palavra in keywords_verdes if palavra in texto)
    score += any(ipc.startswith(code) for code in ipcs_verdes) * 2

    if score >= 6:
        return 'Alta', score
    elif score >= 3:
        return 'Média', score
    else:
        return 'Baixa', score

# ---------------------------
# 5. Aplicando classificação
# ---------------------------
resultados = []
for i, row in dados.iterrows():
    classe, score = classificar_patente(row['Título'], row['Resumo'], row['IPC'])
    resultados.append((classe, score))

dados[['Classificação Sustentável', 'Score']] = resultados

# ---------------------------
# 6. Exibindo tabela
# ---------------------------
st.subheader("📄 Resultados das Patentes Avaliadas")
st.dataframe(dados)

# ---------------------------
# 7. Gráfico de barras
# ---------------------------
st.subheader("📊 Distribuição por Nível de Sustentabilidade")
fig, ax = plt.subplots()
dados['Classificação Sustentável'].value_counts().plot(kind='bar', color=['green', 'orange', 'red'], ax=ax)
plt.xlabel("Classificação")
plt.ylabel("Número de Patentes")
st.pyplot(fig)

# ---------------------------
# 8. Nuvem de palavras
# ---------------------------
st.subheader("☁️ Palavras mais frequentes (Resumos)")
texto_total = ' '.join(dados['Resumo'].values).lower()
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(texto_total)
fig_wc, ax_wc = plt.subplots()
ax_wc.imshow(wordcloud, interpolation='bilinear')
ax_wc.axis('off')
st.pyplot(fig_wc)

# ---------------------------
# 9. Download dos dados
# ---------------------------
st.download_button(
    label="⬇️ Baixar Resultados em CSV",
    data=dados.to_csv(index=False).encode('utf-8'),
    file_name='resultados_patentes_sustentaveis.csv',
    mime='text/csv'
)
