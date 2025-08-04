import streamlit as st

# --- 1. Funções Auxiliares ---
def formatar_nota_br(nota, casas_decimais=1):
    """Formata um número float para o padrão brasileiro com vírgula."""
    if nota == int(nota):
        return str(int(nota)).replace('.', ',')
    return f"{nota:.{casas_decimais}f}".replace('.', ',')

def calcular_media_ponderada(notas, pesos):
    """Calcula a média ponderada de uma lista de notas com seus respectivos pesos."""
    if not notas or not pesos or len(notas) != len(pesos) or sum(pesos) == 0:
        return 0.0
    soma_produtos = sum(nota * peso for nota, peso in zip(notas, pesos))
    soma_pesos = sum(pesos)
    return soma_produtos / soma_pesos if soma_pesos > 0 else 0.0

# --- 2. Constantes ---

# Critérios para Aprovação e Reprovação (Trabalho Escrito)
CRITERIOS_AVALIACAO_ESCRITO = {
    "Correspondência ao tema e à seção temática": 2,
    "Originalidade e contribuição do trabalho": 1,
    "Definição de problema, objetivos e justificativa": 2,
    "Adequação dos métodos e confiabilidade": 2,
    "Clareza, coerência e objetividade": 3
}

# Critérios para a Apresentação Oral
CRITERIOS_AVALIACAO_ORAL = {
    "Correspondência ao tema e à seção temática": 1,
    "Originalidade e contribuição do trabalho": 1,
    "Definição de problema, objetivos e justificativa": 1,
    "Adequação dos métodos e confiabilidade": 2,
    "Clareza, coerência e objetividade": 2,
    "Domínio do conteúdo apresentado": 2,
    "Adequação ao tempo de apresentação": 1
}

# CSS Global para os templates HTML
CSS_GLOBAL = """
<style>
    body {
        font-family: Arial, sans-serif;
        line-height: 1.6;
        color: #333333;
        background-color: #f9f9f9;
        margin: 0;
        padding: 0;
    }
    .container {
        max-width: 700px;
        margin: auto;
        padding: 20px;
        background-color: #ffffff;
        border: 1px solid #ddd;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h2 {
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 10px;
    }
    p {
        margin-bottom: 16px;
        text-align: justify;
    }
    .box {
        background-color: #ecf0f1;
        border-left: 4px solid #3498db;
        padding: 16px;
        margin: 20px 0;
        border-radius: 4px;
        text-align: justify;
    }
    .highlight {
        background-color: #f0f0f0;
        border-left: 4px solid #999999;
        padding: 12px 16px;
        border-radius: 4px;
        margin: 16px 0;
        font-size: 0.95em;
        text-align: justify;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
    }
    th, td {
        text-align: left;
        padding: 10px;
        border-bottom: 1px solid #ddd;
    }
    th {
        background-color: #bdc3c7;
        color: #fff;
    }
    .nota-aprovacao {
        background-color: #dff0d8;
        border-left: 4px solid #5cb85c;
        padding: 16px;
        margin-top: 20px;
        border-radius: 4px;
        font-weight: bold;
        text-align: justify;
    }
    .nota-reprovacao {
        background-color: #f8d7da;
        border-left: 4px solid #d9534f;
        padding: 16px;
        margin-top: 20px;
        border-radius: 4px;
        font-weight: bold;
        color: #721c24;
        text-align: justify;
    }
    .parecer {
        margin-top: 10px;
        font-style: italic;
        color: #444;
        text-align: justify;
    }
    a {
        color: #0645ad;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    ul {
        padding-left: 20px;
        text-align: justify;
    }
    ol {
        padding-left: 20px;
        margin: 0;
        text-align: justify;
    }
</style>
"""

# --- 3. Funções de Template HTML ---
def gerar_html_desclassificacao(motivos_lista):
    motivos_html = "".join(f"<li>{m}</li>" for m in motivos_lista)
    return f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>{CSS_GLOBAL}</head>
    <body>
    <div class="container">
        <p>Prezado(a) autor(a),</p>
        <p>Esperamos que esta mensagem o(a) encontre bem.</p>
        <p>Agradecemos o envio do seu resumo expandido à <strong>VII Semana Acadêmica da Propriedade Intelectual (VII SEMPI)</strong>. Após análise preliminar (desk review), informamos que seu trabalho <strong>não atendeu</strong> integralmente às diretrizes estabelecidas pela Comissão Organizadora para avançar à próxima etapa de avaliação por pares.</p>
        <div class="box">
            <p><strong>📌 Principais aspectos a serem corrigidos:</strong></p>
            <ol>{motivos_html}</ol>
        </div>
        <p>Solicitamos, gentilmente, que as correções sejam realizadas e o trabalho corrigido seja ressubmetido no sistema até o dia <strong>19 de agosto de 2025</strong>.</p>
        <p>Permanecemos à disposição para quaisquer dúvidas ou esclarecimentos que se fizerem necessários.</p>
    </div>
    </body>
    </html>
    """

def gerar_html_avaliacao(tipo_notificacao, notas_i, media_i, parecer_i, notas_ii, media_ii, parecer_ii, nota_final):
    titulo = "🎉 Aprovação de Trabalho" if tipo_notificacao == "Aprovação" else "❌ Reprovação de Trabalho"
    paragrafo_inicial = (
        "Temos o prazer de informar que o seu resumo expandido foi <strong>aprovado</strong> para apresentação oral na "
        "<strong>VII Semana Acadêmica da Propriedade Intelectual (VII SEMPI)</strong>."
    ) if tipo_notificacao == "Aprovação" else (
        "Informamos que o seu resumo expandido foi <strong>reprovado</strong> para apresentação na "
        "<strong>VII Semana Acadêmica da Propriedade Intelectual (VII SEMPI)</strong>."
    )
    classe_nota_final = "nota-aprovacao" if tipo_notificacao == "Aprovação" else "nota-reprovacao"
    link_orientacoes = (
        '<p>As orientações para a elaboração e o envio do arquivo da apresentação estão disponíveis no site do evento:<br />'
        '🔗 <a href="https://www.even3.com.br/vii-semana-academica-da-propriedade-intelectual-594540/" target="_blank">'
        'https://www.even3.com.br/vii-semana-academica-da-propriedade-intelectual-594540/</a></p>'
    ) if tipo_notificacao == "Aprovação" else ""

    tabela_i = "".join(f'<tr><td>{i+1}. {c}</td><td>{formatar_nota_br(n)}</td></tr>' for i, (c, n) in enumerate(notas_i.items()))
    tabela_ii = "".join(f'<tr><td>{i+1}. {c}</td><td>{formatar_nota_br(n)}</td></tr>' for i, (c, n) in enumerate(notas_ii.items()))

    return f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>{CSS_GLOBAL}</head>
    <body>
    <div class="container">
        <h2>{titulo}</h2>
        <p>Prezados(as),</p>
        <p>Esperamos que esta mensagem os(as) encontre bem.</p>
        <p>{paragrafo_inicial}</p>
        <p>Abaixo, apresentamos as avaliações realizadas pelos membros do Comitê Científico:</p>

        <div class="box">
            <p><strong>👤 Avaliador(a) I</strong></p>
            <table><tr><th>Critério</th><th>Nota</th></tr>{tabela_i}</table>
            <p><strong>Média ponderada: {formatar_nota_br(media_i, 2)}</strong></p>
            <p class="parecer">{parecer_i}</p>
        </div>

        <div class="box">
            <p><strong>👤 Avaliador(a) II</strong></p>
            <table><tr><th>Critério</th><th>Nota</th></tr>{tabela_ii}</table>
            <p><strong>Média ponderada: {formatar_nota_br(media_ii, 2)}</strong></p>
            <p class="parecer">{parecer_ii}</p>
        </div>

        <div class="{classe_nota_final}">
            Nota final do trabalho: <strong>{formatar_nota_br(nota_final, 2)}</strong>
        </div>

        {link_orientacoes}
        <p>Permanecemos à disposição para quaisquer dúvidas ou esclarecimentos que se fizerem necessários.</p>
    </div>
    </body>
    </html>
    """

def gerar_html_lembrete_envio(texto_envio_arquivo):
    return f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>{CSS_GLOBAL}</head>
    <body>
    <div class="container">
        <p>Prezados(as) autores(as),</p>
        <p>Esperamos que esta mensagem os(as) encontre bem.</p>
        <p>A Comissão Organizadora da <strong>VII Semana Acadêmica da Propriedade Intelectual (VII SEMPI)</strong> relembra que todos os trabalhos aprovados deverão ser apresentados em sessão pública e avaliados por membros do Comitê Científico.</p>
        <p>{texto_envio_arquivo}</p>
        <div class="highlight">
            Se o autor principal não for apresentar o trabalho, seja por impossibilidade de comparecimento à sessão ou por outra razão, deverá designar um coautor para realizar a apresentação, respeitando o prazo estipulado. O coautor designado deverá, obrigatoriamente, estar inscrito no evento. Ressalta-se, porém, que os demais coautores que não participarão do evento, seja de forma presencial ou on-line, não precisam estar inscritos, ainda que seus nomes constem no trabalho. A alteração deverá ser comunicada à Comissão Organizadora no e-mail <a href="mailto:submissoes.sempi@gmail.com">submissoes.sempi@gmail.com</a> até <strong>29 de agosto de 2025</strong>.
        </div>
        <p>A ordem das apresentações, tanto presenciais quanto on-line, seguirá a programação previamente divulgada em nossos canais oficiais, salvo em casos excepcionais devidamente justificados. Autores que submeteram mais de um resumo expandido, especialmente em sessões temáticas diferentes, terão suas apresentações organizadas de forma a evitar conflitos de horário.</p>
        <p>O modelo editável está disponível no site do evento: <br />🔗 <a href="https://www.even3.com.br/vii-semana-academica-da-propriedade-intelectual-594540/" target="_blank" rel="noopener noreferrer">https://www.even3.com.br/vii-semana-academica-da-propriedade-intelectual-594540/</a>. Embora não haja limite de quantidade de slides, é obrigatório manter integralmente a formatação original (estilo, tamanho da fonte e cores).</p>
        <p>Permanecemos à disposição para quaisquer dúvidas ou esclarecimentos que se fizerem necessários.</p>
    </div>
    </body>
    </html>
    """

def gerar_html_lembrete_apresentacao(tempo_apresentacao, tempo_arguicao):
    return f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>{CSS_GLOBAL}</head>
    <body>
    <div class="container">
        <p>Prezados(as),</p>
        <p>A Comissão Organizadora da <strong>VII Semana Acadêmica da Propriedade Intelectual (VII SEMPI)</strong> relembra que as apresentações dos resumos aprovados acontecerão <strong>amanhã</strong>. A programação completa, contendo datas, horários, locais e a ordem das apresentações, já se encontra disponível no site oficial do evento:</p>
        <p>🔗 <a href="https://www.even3.com.br/vii-semana-academica-da-propriedade-intelectual-594540/" target="_blank" rel="noopener noreferrer">https://www.even3.com.br/vii-semana-academica-da-propriedade-intelectual-594540/</a></p>
        <div class="highlight">
            <p style="text-align: left;"><strong>⚠️ Orientações importantes:</strong></p>
            <ul style="margin-top: 0; padding-left: 20px;">
                <li style="text-align: left;">Autores que apresentarão seus trabalhos presencialmente devem comparecer ao local da sessão com, no mínimo, <strong>20 minutos de antecedência</strong>.</li>
                <li style="text-align: left;">Essa orientação também se aplica aos participantes com apresentação on-line autorizada, mediante justificativa formal.</li>
                <li style="text-align: left;"><strong>Não serão permitidas correções ou substituições</strong> do arquivo de apresentação durante o evento.</li>
            </ul>
        </div>
        <p>Cada apresentador(a) disporá de até <strong>{tempo_apresentacao} minutos</strong> para a exposição do trabalho, seguidos de até <strong>{tempo_arguicao} minutos</strong> para arguição e/ou comentários dos(as) avaliadores(as).</p>
        <p>Cada trabalho será avaliado por, no mínimo, dois pareceristas. Os critérios de avaliação da apresentação oral seguem os mesmos adotados para o trabalho escrito, com o acréscimo dos seguintes itens:</p>
        <ul style="padding-left: 20px; text-align: justify;">
            <li>🎤 Domínio do conteúdo apresentado;</li>
            <li>⏳ Adequação ao tempo de apresentação.</li>
        </ul>
        <p>Cada critério será avaliado em uma escala de 0 a 10, e a nota final de cada avaliador será calculada com base na média ponderada das notas atribuídas. A nota final da apresentação corresponderá à média aritmética das avaliações dos dois pareceristas.</p>
        <p>Para fins de premiação, será considerada a média ponderada entre a nota do resumo e a nota da apresentação.</p>
        <p>Desejamos uma excelente apresentação!</p>
    </div>
    </body>
    </html>
    """

def gerar_html_resultado_final(nota_apresentacao, nota_escrito, nota_geral, hora_encerramento):
    return f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>{CSS_GLOBAL}</head>
    <body>
    <div class="container">
        <h2>Resultado Final</h2>
        <p>Prezados(as),</p>
        <p>A Comissão Organizadora da <strong>VII Semana Acadêmica da Propriedade Intelectual (VII SEMPI)</strong> gostaria de parabenizá-lo(a) pela participação e excelente apresentação do seu trabalho.</p>
        <p>Abaixo, detalhamos o cálculo da nota final do seu trabalho, que considera tanto a avaliação do resumo expandido quanto a da apresentação oral.</p>

        <div class="box">
            <p><strong>Notas:</strong></p>
            <p><strong>Nota do Trabalho Escrito:</strong> {formatar_nota_br(nota_escrito, 2)}</p>
            <p><strong>Nota da Apresentação Oral:</strong> {formatar_nota_br(nota_apresentacao, 2)}</p>
        </div>

        <div class="nota-aprovacao">
            Nota Geral (Trabalho Escrito: Peso 7, Apresentação Oral: Peso 3): <strong>{formatar_nota_br(nota_geral, 2)}</strong>
        </div>

        <p>Convidamos você a participar da cerimônia de encerramento do evento, onde anunciaremos os trabalhos premiados. A cerimônia ocorrerá hoje, às <strong>{hora_encerramento}</strong>, no local do evento.</p>
        <p>Permanecemos à disposição para quaisquer dúvidas ou esclarecimentos que se fizerem necessários.</p>
    </div>
    </body>
    </html>
    """

# --- 4. Função Principal do Streamlit ---
def main():
    st.set_page_config(page_title="Gerador de HTML SEMPI", layout="wide")
    
    with st.container():
        st.markdown(
            """
            <div style="background-color: #004d99; padding: 15px; border-radius: 10px; color: white;">
                <h1 style="color: white; text-align: center; font-family: 'Arial Black', sans-serif;">💻 Notificação Interna Even3 (VII SEMPI)</h1>
                <p style="text-align: center; font-style: italic;">Uma ferramenta para agilizar a comunicação com os autores.</p>
            </div>
            <br>
            """,
            unsafe_allow_html=True
        )

    st.sidebar.title("Navegação")
    aba = st.sidebar.radio("Selecione uma opção:", ["Aprovação", "Reprovação", "Desclassificação", "Lembretes", "Resultado Final"])
    
    st.markdown("---")
    
    if aba == "Desclassificação":
        st.header("❌ Desclassificação")
        motivos = st.text_area(
            "Liste os motivos da desclassificação, separados por barra (ex: 'Motivo 1 / Motivo 2'):",
            value="O trabalho não atende ao tema do evento e/ou à seção temática escolhida / O trabalho não apresenta um problema de pesquisa claro / Formatação fora das normas."
        )
        motivos_lista = [m.strip() for m in motivos.split("/") if m.strip()]
        html_desclassificacao = gerar_html_desclassificacao(motivos_lista)
        st.code(html_desclassificacao, language="html")

    elif aba == "Aprovação" or aba == "Reprovação":
        titulo = "✅ Aprovação de Trabalho" if aba == "Aprovação" else "❌ Reprovação de Trabalho"
        st.header(titulo)
        
        col1, col2 = st.columns(2)

        # Coletar notas para o Avaliador I
        with col1:
            with st.expander("📝 Notas Avaliador I", expanded=True):
                notas_i = {}
                for criterio, peso in CRITERIOS_AVALIACAO_ESCRITO.items():
                    key = f"{aba}_i_{criterio}"
                    notas_i[criterio] = st.number_input(f"Nota para '{criterio}' (Peso: {peso})", min_value=0.0, max_value=10.0, step=0.1, key=key)
                parecer_i = st.text_area("Parecer do Avaliador I", key=f"{aba}_parecer_i")
                media_ponderada_i = calcular_media_ponderada(list(notas_i.values()), list(CRITERIOS_AVALIACAO_ESCRITO.values()))
                st.metric("Média Ponderada Avaliador I", formatar_nota_br(media_ponderada_i, 2))

        # Coletar notas para o Avaliador II
        with col2:
            with st.expander("📝 Notas Avaliador II", expanded=True):
                notas_ii = {}
                for criterio, peso in CRITERIOS_AVALIACAO_ESCRITO.items():
                    key = f"{aba}_ii_{criterio}"
                    notas_ii[criterio] = st.number_input(f"Nota para '{criterio}' (Peso: {peso})", min_value=0.0, max_value=10.0, step=0.1, key=key)
                parecer_ii = st.text_area("Parecer do Avaliador II", key=f"{aba}_parecer_ii")
                media_ponderada_ii = calcular_media_ponderada(list(notas_ii.values()), list(CRITERIOS_AVALIACAO_ESCRITO.values()))
                st.metric("Média Ponderada Avaliador II", formatar_nota_br(media_ponderada_ii, 2))

        nota_final_trabalho = (media_ponderada_i + media_ponderada_ii) / 2
        
        st.subheader("Resultado Final")
        if aba == "Aprovação":
            st.success(f"Nota final do trabalho: **{formatar_nota_br(nota_final_trabalho, 2)}**")
        else:
            st.error(f"Nota final do trabalho: **{formatar_nota_br(nota_final_trabalho, 2)}**")

        st.markdown("### HTML Gerado")
        html_avaliacao = gerar_html_avaliacao(aba, notas_i, media_ponderada_i, parecer_i, notas_ii, media_ponderada_ii, parecer_ii, nota_final_trabalho)
        st.code(html_avaliacao, language="html")

    elif aba == "Lembretes":
        st.header("🔔 Lembretes")
        
        st.subheader("Lembrete de Envio do Arquivo")
        texto_envio_arquivo = st.text_area(
            "Digite o texto para o lembrete de envio do arquivo:", 
            value="Para tanto, solicitamos que o arquivo de apresentação seja enviado até o dia <strong>29 de agosto de 2025</strong>, em formato PDF, por meio da Área do Participante. Para realizar o envio, acesse a plataforma com seu login e senha, clique no menu “Submissões”, selecione o trabalho correspondente, clique em “Editar” e anexe o arquivo no campo indicado. Após o envio, certifique-se de salvar as alterações."
        )
        html_lembrete_envio = gerar_html_lembrete_envio(texto_envio_arquivo)
        st.code(html_lembrete_envio, language="html")

        st.subheader("Lembrete de Apresentação")
        tempo_apresentacao = st.number_input("Tempo para apresentação (minutos)", min_value=1, max_value=60, value=10)
        tempo_arguicao = st.number_input("Tempo para arguição (minutos)", min_value=1, max_value=30, value=5)
        html_lembrete_apresentacao = gerar_html_lembrete_apresentacao(tempo_apresentacao, tempo_arguicao)
        st.code(html_lembrete_apresentacao, language="html")

    elif aba == "Resultado Final":
        st.header("🏆 Resultado Final")
        
        st.subheader("Avaliação da Apresentação Oral")
        col1, col2 = st.columns(2)
        
        # Coletar notas para o Avaliador I (Oral)
        with col1:
            with st.expander("📝 Notas Avaliador I (Oral)", expanded=True):
                notas_final_i = {}
                for criterio, peso in CRITERIOS_AVALIACAO_ORAL.items():
                    key = f"final_i_{criterio}"
                    notas_final_i[criterio] = st.number_input(f"Nota para '{criterio}' (Peso: {peso})", min_value=0.0, max_value=10.0, step=0.1, key=key)
                media_ponderada_final_i = calcular_media_ponderada(list(notas_final_i.values()), list(CRITERIOS_AVALIACAO_ORAL.values()))
                st.metric("Média Ponderada Avaliador I", formatar_nota_br(media_ponderada_final_i, 2))

        # Coletar notas para o Avaliador II (Oral)
        with col2:
            with st.expander("📝 Notas Avaliador II (Oral)", expanded=True):
                notas_final_ii = {}
                for criterio, peso in CRITERIOS_AVALIACAO_ORAL.items():
                    key = f"final_ii_{criterio}"
                    notas_final_ii[criterio] = st.number_input(f"Nota para '{criterio}' (Peso: {peso})", min_value=0.0, max_value=10.0, step=0.1, key=key)
                media_ponderada_final_ii = calcular_media_ponderada(list(notas_final_ii.values()), list(CRITERIOS_AVALIACAO_ORAL.values()))
                st.metric("Média Ponderada Avaliador II", formatar_nota_br(media_ponderada_final_ii, 2))

        nota_final_apresentacao = (media_ponderada_final_i + media_ponderada_final_ii) / 2
        st.success(f"Nota da Apresentação Oral: **{formatar_nota_br(nota_final_apresentacao, 2)}**")

        st.markdown("### Cálculo da Nota Geral")
        nota_final_escrito = st.number_input("Nota do Trabalho Escrito (Manual):", min_value=0.0, max_value=10.0, step=0.1, value=0.0)
        
        nota_geral_ponderada = calcular_media_ponderada([nota_final_escrito, nota_final_apresentacao], [7, 3])
        st.balloons()
        st.success(f"Nota Geral Ponderada (Peso 7/3): **{formatar_nota_br(nota_geral_ponderada, 2)}**")

        hora_encerramento = st.text_input("Hora da cerimônia de encerramento:", value="18h30")
        
        st.markdown("### HTML Gerado")
        html_resultado_final = gerar_html_resultado_final(nota_final_apresentacao, nota_final_escrito, nota_geral_ponderada, hora_encerramento)
        st.code(html_resultado_final, language="html")

if __name__ == "__main__":
    main()
