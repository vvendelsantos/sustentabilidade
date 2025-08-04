import streamlit as st

# --- Funções auxiliares (manteremos as suas, pois já estão ótimas!) ---

def formatar_nota_br(nota, casas_decimais=1):
    """Formata uma nota float para o padrão brasileiro com vírgula."""
    if nota == int(nota):
        return str(int(nota)).replace('.', ',')
    else:
        return f"{nota:.{casas_decimais}f}".replace('.', ',')

def calcular_media_ponderada(notas, pesos):
    """Calcula a média ponderada de uma lista de notas com pesos."""
    if not notas or not pesos or len(notas) != len(pesos):
        return 0.0
    soma_produtos = sum(nota * peso for nota, peso in zip(notas, pesos))
    soma_pesos = sum(pesos)
    return soma_produtos / soma_pesos if soma_pesos > 0 else 0.0

# --- Textos e templates HTML (manteremos, pois já estão bem definidos) ---

LEMBRETE_ENVIO_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <style>
        /* ... Seu CSS ... */
    </style>
</head>
<body>
    <div class="container">
        </div>
</body>
</html>
"""

LEMBRETE_APRESENTACAO_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <style>
        /* ... Seu CSS ... */
    </style>
</head>
<body>
    <div class="container">
        </div>
</body>
</html>
"""

# HTML base para Desclassificação
HTML_DESCLASSIFICACAO = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <style>
        /* ... Seu CSS ... */
    </style>
</head>
<body>
    <div class="container">
        <div class="box">
            <p><strong>📌 Principais aspectos a serem corrigidos:</strong></p>
            <ol>
                {motivos_lista_html}
            </ol>
        </div>
        </div>
</body>
</html>
"""

# HTML base para Aprovação
HTML_APROVACAO = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <style>
        /* ... Seu CSS ... */
    </style>
</head>
<body>
    <div class="container">
        <div class="box">
            <p><strong>👤 Avaliador(a) I</strong></p>
            <table>
                <tr>
                    <th>Critério</th>
                    <th>Nota</th>
                </tr>
                {tabela_avaliador_i}
            </table>
            <p><strong>Média ponderada: {media_i}</strong></p>
            <p class="parecer">{parecer_i}</p>
        </div>
        <div class="box">
            <p><strong>👤 Avaliador(a) II</strong></p>
            <table>
                <tr>
                    <th>Critério</th>
                    <th>Nota</th>
                </tr>
                {tabela_avaliador_ii}
            </table>
            <p><strong>Média ponderada: {media_ii}</strong></p>
            <p class="parecer">{parecer_ii}</p>
        </div>
        <div class="nota-final">
            Nota final do trabalho: <strong>{nota_final}</strong>
        </div>
        </div>
</body>
</html>
"""

# HTML base para Reprovação (similar ao de Aprovação, apenas o CSS da nota final muda)
HTML_REPROVACAO = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <style>
        /* ... Seu CSS ... */
    </style>
</head>
<body>
    <div class="container">
        <div class="box">
            <p><strong>👤 Avaliador(a) I</strong></p>
            <table>
                <tr>
                    <th>Critério</th>
                    <th>Nota</th>
                </tr>
                {tabela_avaliador_i}
            </table>
            <p><strong>Média ponderada: {media_i}</strong></p>
            <p class="parecer">{parecer_i}</p>
        </div>
        <div class="box">
            <p><strong>👤 Avaliador(a) II</strong></p>
            <table>
                <tr>
                    <th>Critério</th>
                    <th>Nota</th>
                    </tr>
                {tabela_avaliador_ii}
            </table>
            <p><strong>Média ponderada: {media_ii}</strong></p>
            <p class="parecer">{parecer_ii}</p>
        </div>
        <div class="nota-final">
            Nota final do trabalho: <strong>{nota_final}</strong>
        </div>
        </div>
</body>
</html>
"""

# --- Funções de cada página ---

def pagina_desclassificacao():
    st.header("📄 Desclassificação")
    
    # Criando colunas para organizar a entrada de texto e a pré-visualização
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Configurações")
        motivos = st.text_area(
            "Liste os motivos da desclassificação, separados por '/' :",
            value="X/ Y/ Z"
        )
        motivos_lista = [m.strip() for m in motivos.split("/") if m.strip()]
    
    with col2:
        st.subheader("Pré-visualização do HTML")
        motivos_lista_html = "".join(f"<li>{m}</li>" for m in motivos_lista)
        html_desclassificacao = HTML_DESCLASSIFICACAO.format(motivos_lista_html=motivos_lista_html)
        st.components.v1.html(html_desclassificacao, height=500, scrolling=True)

    # Adicionando um expansor para exibir o código HTML, que pode ser copiado
    with st.expander("Ver código HTML"):
        st.code(html_desclassificacao, language="html")

def pagina_aprovacao():
    st.header("✅ Aprovação")

    criterios_avaliacao_aprov = [
        ("Correspondência do trabalho ao tema do evento", 2),
        ("Originalidade e contribuição do trabalho", 1),
        ("Definição clara do problema, objetivos e justificativa", 2),
        ("Adequação dos métodos à pesquisa", 2),
        ("Clareza, coerência e objetividade dos resultados", 3)
    ]
    nomes_criterios_aprov = [c[0] for c in criterios_avaliacao_aprov]
    pesos_criterios_aprov = [c[1] for c in criterios_avaliacao_aprov]

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Notas Avaliador(a) I")
        notas_i = {}
        for i, nome in enumerate(nomes_criterios_aprov):
            notas_i[nome] = st.number_input(f"{i+1}. {nome} (Peso {pesos_criterios_aprov[i]})", min_value=0.0, max_value=10.0, step=0.1, key=f"aprov_nota_i_{i}")
        
        media_ponderada_i = calcular_media_ponderada(list(notas_i.values()), pesos_criterios_aprov)
        st.info(f"Média ponderada: **{formatar_nota_br(media_ponderada_i, 2)}**")
        parecer_i = st.text_area("Parecer Avaliador(a) I", value='''"Parecer."''', key="aprov_parecer_i")
    
    with col2:
        st.subheader("Notas Avaliador(a) II")
        notas_ii = {}
        for i, nome in enumerate(nomes_criterios_aprov):
            notas_ii[nome] = st.number_input(f"{i+1}. {nome} (Peso {pesos_criterios_aprov[i]})", min_value=0.0, max_value=10.0, step=0.1, key=f"aprov_nota_ii_{i}")
        
        media_ponderada_ii = calcular_media_ponderada(list(notas_ii.values()), pesos_criterios_aprov)
        st.info(f"Média ponderada: **{formatar_nota_br(media_ponderada_ii, 2)}**")
        parecer_ii = st.text_area("Parecer Avaliador(a) II", value='''"Parecer."''', key="aprov_parecer_ii")

    # Separador visual
    st.markdown("---")

    nota_final_aprovacao = (media_ponderada_i + media_ponderada_ii) / 2
    st.metric("Nota final do trabalho:", formatar_nota_br(nota_final_aprovacao, 2))

    # Pré-visualização do HTML com a nota final
    with st.expander("Pré-visualização do HTML"):
        tabela_i = "".join(f'<tr><td>{i+1}. {c}</td><td>{formatar_nota_br(notas_i[c])}</td></tr>' for i, c in enumerate(nomes_criterios_aprov))
        tabela_ii = "".join(f'<tr><td>{i+1}. {c}</td><td>{formatar_nota_br(notas_ii[c])}</td></tr>' for i, c in enumerate(nomes_criterios_aprov))
        
        html_aprovacao = HTML_APROVACAO.format(
            tabela_avaliador_i=tabela_i,
            media_i=formatar_nota_br(media_ponderada_i, 2),
            parecer_i=parecer_i,
            tabela_avaliador_ii=tabela_ii,
            media_ii=formatar_nota_br(media_ponderada_ii, 2),
            parecer_ii=parecer_ii,
            nota_final=formatar_nota_br(nota_final_aprovacao, 2)
        )
        st.components.v1.html(html_aprovacao, height=800, scrolling=True)

    with st.expander("Ver código HTML"):
        st.code(html_aprovacao, language="html")

def pagina_reprovacao():
    st.header("❌ Reprovação")

    # Critérios e pesos são os mesmos da aprovação, então vamos reutilizar a lista
    criterios_avaliacao_reprov = [
        ("Correspondência do trabalho ao tema do evento", 2),
        ("Originalidade e contribuição do trabalho", 1),
        ("Definição clara do problema, objetivos e justificativa", 2),
        ("Adequação dos métodos à pesquisa", 2),
        ("Clareza, coerência e objetividade dos resultados", 3)
    ]
    nomes_criterios_reprov = [c[0] for c in criterios_avaliacao_reprov]
    pesos_criterios_reprov = [c[1] for c in criterios_avaliacao_reprov]

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Notas Avaliador(a) I")
        notas_i = {}
        for i, nome in enumerate(nomes_criterios_reprov):
            notas_i[nome] = st.number_input(f"{i+1}. {nome} (Peso {pesos_criterios_reprov[i]})", min_value=0.0, max_value=10.0, step=0.1, key=f"reprov_nota_i_{i}")
        
        media_ponderada_i = calcular_media_ponderada(list(notas_i.values()), pesos_criterios_reprov)
        st.info(f"Média ponderada: **{formatar_nota_br(media_ponderada_i, 2)}**")
        parecer_i = st.text_area("Parecer Avaliador(a) I", value='''"Parecer."''', key="reprov_parecer_i")
    
    with col2:
        st.subheader("Notas Avaliador(a) II")
        notas_ii = {}
        for i, nome in enumerate(nomes_criterios_reprov):
            notas_ii[nome] = st.number_input(f"{i+1}. {nome} (Peso {pesos_criterios_reprov[i]})", min_value=0.0, max_value=10.0, step=0.1, key=f"reprov_nota_ii_{i}")
        
        media_ponderada_ii = calcular_media_ponderada(list(notas_ii.values()), pesos_criterios_reprov)
        st.info(f"Média ponderada: **{formatar_nota_br(media_ponderada_ii, 2)}**")
        parecer_ii = st.text_area("Parecer Avaliador(a) II", value='''"Parecer."''', key="reprov_parecer_ii")

    st.markdown("---")

    nota_final_reprovacao = (media_ponderada_i + media_ponderada_ii) / 2
    st.metric("Nota final do trabalho:", formatar_nota_br(nota_final_reprovacao, 2))

    with st.expander("Pré-visualização do HTML"):
        tabela_i = "".join(f'<tr><td>{i+1}. {c}</td><td>{formatar_nota_br(notas_i[c])}</td></tr>' for i, c in enumerate(nomes_criterios_reprov))
        tabela_ii = "".join(f'<tr><td>{i+1}. {c}</td><td>{formatar_nota_br(notas_ii[c])}</td></tr>' for i, c in enumerate(nomes_criterios_reprov))
        
        html_reprovacao = HTML_REPROVACAO.format(
            tabela_avaliador_i=tabela_i,
            media_i=formatar_nota_br(media_ponderada_i, 2),
            parecer_i=parecer_i,
            tabela_avaliador_ii=tabela_ii,
            media_ii=formatar_nota_br(media_ponderada_ii, 2),
            parecer_ii=parecer_ii,
            nota_final=formatar_nota_br(nota_final_reprovacao, 2)
        )
        st.components.v1.html(html_reprovacao, height=800, scrolling=True)

    with st.expander("Ver código HTML"):
        st.code(html_reprovacao, language="html")

def pagina_lembretes():
    st.header("⏰ Lembretes")

    tab1, tab2 = st.tabs(["Lembrete de Envio", "Lembrete de Apresentação"])

    with tab1:
        st.markdown("### Texto para envio do arquivo de apresentação")
        texto_envio_arquivo = st.text_area(
            "Digite o texto para o lembrete de envio do arquivo:",
            value="""Para tanto, solicitamos que o arquivo de apresentação seja enviado até o dia <strong>29 de agosto de 2025</strong>, em formato PDF, por meio da Área do Participante. Para realizar o envio, acesse a plataforma com seu login e senha, clique no menu “Submissões”, selecione o trabalho correspondente, clique em “Editar” e anexe o arquivo no campo indicado. Após o envio, certifique-se de salvar as alterações.""",
            key="lembrete_envio_texto"
        )
        html_lembrete_envio = LEMBRETE_ENVIO_HTML.format(texto_envio_arquivo=texto_envio_arquivo)
        st.subheader("Pré-visualização")
        st.components.v1.html(html_lembrete_envio, height=500, scrolling=True)
        with st.expander("Ver código HTML"):
            st.code(html_lembrete_envio, language="html")

    with tab2:
        st.markdown("### Tempos para apresentação")
        col1, col2 = st.columns([1, 1])
        with col1:
            tempo_apresentacao = st.number_input("Tempo para apresentação (minutos)", min_value=1, max_value=60, value=10, key="tempo_apresentacao")
        with col2:
            tempo_arguicao = st.number_input("Tempo para arguição (minutos)", min_value=1, max_value=30, value=5, key="tempo_arguicao")

        html_lembrete_apresentacao = LEMBRETE_APRESENTACAO_HTML.format(tempo_apresentacao=tempo_apresentacao, tempo_arguicao=tempo_arguicao)
        st.subheader("Pré-visualização")
        st.components.v1.html(html_lembrete_apresentacao, height=500, scrolling=True)
        with st.expander("Ver código HTML"):
            st.code(html_lembrete_apresentacao, language="html")

def pagina_resultado_final():
    st.header("🏆 Resultado Final")

    criterios_avaliacao_final = [
        ("Correspondência do trabalho ao tema do evento", 1),
        ("Originalidade e contribuição do trabalho", 1),
        ("Definição clara do problema, objetivos e justificativa", 1),
        ("Adequação dos métodos à pesquisa", 2),
        ("Clareza, coerência e objetividade dos resultados", 2),
        ("Domínio do conteúdo apresentado", 2),
        ("Adequação ao tempo de apresentação", 1)
    ]
    nomes_criterios_final = [c[0] for c in criterios_avaliacao_final]
    pesos_criterios_final = [c[1] for c in criterios_avaliacao_final]

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Notas Apresentação - Avaliador(a) I")
        notas_final_i = {}
        for i, nome in enumerate(nomes_criterios_final):
            notas_final_i[nome] = st.number_input(f"{i+1}. {nome} (Peso {pesos_criterios_final[i]})", min_value=0.0, max_value=10.0, step=0.1, key=f"nota_final_i_{i}")
        media_ponderada_final_i = calcular_media_ponderada(list(notas_final_i.values()), pesos_criterios_final)
        st.info(f"Média ponderada Avaliador I: **{formatar_nota_br(media_ponderada_final_i, 2)}**")

    with col2:
        st.subheader("Notas Apresentação - Avaliador(a) II")
        notas_final_ii = {}
        for i, nome in enumerate(nomes_criterios_final):
            notas_final_ii[nome] = st.number_input(f"{i+1}. {nome} (Peso {pesos_criterios_final[i]})", min_value=0.0, max_value=10.0, step=0.1, key=f"nota_final_ii_{i}")
        media_ponderada_final_ii = calcular_media_ponderada(list(notas_final_ii.values()), pesos_criterios_final)
        st.info(f"Média ponderada Avaliador II: **{formatar_nota_br(media_ponderada_final_ii, 2)}**")

    st.markdown("---")
    
    col3, col4 = st.columns([1, 1])
    
    with col3:
        # Cálculo da Nota Final da Apresentação Oral (média aritmética)
        nota_final_apresentacao = (media_ponderada_final_i + media_ponderada_final_ii) / 2
        st.metric("Nota da Apresentação Oral:", formatar_nota_br(nota_final_apresentacao, 2))
    
    with col4:
        # Campo para inserir a Nota do Trabalho Escrito manualmente
        nota_final_escrito = st.number_input("Nota do Trabalho Escrito:", min_value=0.0, max_value=10.0, step=0.1, value=0.0)

    # Cálculo da Nota Geral Ponderada
    st.markdown("---")
    nota_geral_ponderada = calcular_media_ponderada(
        [nota_final_escrito, nota_final_apresentacao],
        [7, 3]  # Pesos: Trabalho Escrito (7), Apresentação Oral (3)
    )
    st.success(f"### Nota Geral Ponderada: {formatar_nota_br(nota_geral_ponderada, 2)}")

# --- Função principal para controlar o fluxo do aplicativo ---
def main():
    st.set_page_config(page_title="Gerador de HTML SEMPI", layout="wide", initial_sidebar_state="expanded")
    
    # Criando o cabeçalho e a barra lateral de navegação
    with st.sidebar:
        st.title("💻 Gerador de E-mails")
        st.markdown("---")
        aba_selecionada = st.radio(
            "Selecione o tipo de e-mail:",
            ["Desclassificação", "Aprovação", "Reprovação", "Lembretes", "Resultado Final"],
            icons=["x-octagon", "check-circle", "x-circle", "bell", "trophy"]
        )

    # Chamando a função da página selecionada
    if aba_selecionada == "Desclassificação":
        pagina_desclassificacao()
    elif aba_selecionada == "Aprovação":
        pagina_aprovacao()
    elif aba_selecionada == "Reprovação":
        pagina_reprovacao()
    elif aba_selecionada == "Lembretes":
        pagina_lembretes()
    elif aba_selecionada == "Resultado Final":
        pagina_resultado_final()

if __name__ == "__main__":
    main()
