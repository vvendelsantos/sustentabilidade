import streamlit as st
import random

st.title("🕵️‍♂️ Caça às Tecnologias Verdes")

# Lista de palavras verdes (corretas)
palavras_verdes = {
    "sustentabilidade", "biocombustível", "energia solar", "reflorestamento",
    "biodiesel", "eficiência energética", "eólica", "reciclagem",
    "tratamento de efluentes", "ODS", "patente verde", "propriedade intelectual",
    "bioetanol", "economia circular", "biomassa"
}

# Lista de palavras neutras ou erradas
palavras_erradas = {
    "computador", "internet", "telefone", "bicicleta",
    "cidade", "carro", "casa", "música", "livro",
    "revolução", "história", "médico", "filosofia", "arte"
}

# Criar lista misturada de palavras
palavras = list(palavras_verdes) + list(palavras_erradas)
random.shuffle(palavras)

# Estado para controlar acertos e erros
if 'acertos' not in st.session_state:
    st.session_state.acertos = 0
if 'erros' not in st.session_state:
    st.session_state.erros = 0
if 'selecionadas' not in st.session_state:
    st.session_state.selecionadas = set()

st.write("Clique nas palavras relacionadas a tecnologias verdes e sustentabilidade:")

# Função para tratar clique em palavra
def clicar_palavra(palavra):
    if palavra in st.session_state.selecionadas:
        return  # Ignorar cliques repetidos
    st.session_state.selecionadas.add(palavra)
    if palavra in palavras_verdes:
        st.session_state.acertos += 1
    else:
        st.session_state.erros += 1

# Mostrar palavras como botões
cols = st.columns(5)
for i, palavra in enumerate(palavras):
    with cols[i % 5]:
        if st.button(palavra):
            clicar_palavra(palavra)

# Mostrar feedback
st.markdown(f"**Acertos:** {st.session_state.acertos} | **Erros:** {st.session_state.erros}")

# Pontuação final (exemplo: acertos menos erros)
score = st.session_state.acertos - st.session_state.erros
st.markdown(f"### Pontuação final: {score}")

# Botão para reiniciar jogo
if st.button("🔄 Jogar novamente"):
    st.session_state.acertos = 0
    st.session_state.erros = 0
    st.session_state.selecionadas = set()
    st.experimental_rerun()
