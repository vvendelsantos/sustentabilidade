import streamlit as st

# --- Funções Auxiliares (idealmente em um arquivo utils/calculos.py) ---
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
    return soma_produtos / soma_pesos

# --- Constantes (idealmente em um arquivo de dados) ---
CRITERIOS_APROVACAO = {
    "Correspondência do trabalho ao tema do evento e à seção temática escolhida": 2,
    "Originalidade e contribuição do trabalho na área da Propriedade Intelectual": 1,
    "Definição clara do problema, dos objetivos e da justificativa do trabalho": 2,
    "Adequação dos métodos à pesquisa e confiabilidade dos procedimentos apresentados": 2,
    "Clareza, coerência e objetividade na apresentação e discussão dos resultados": 3
}

# --- Função para gerar HTML (idealmente em um arquivo utils/html_templates.py) ---
def gerar_html_aprovacao(notas_i, media_i, parecer_i, notas_ii, media_ii, parecer_ii, nota_final):
    # A string HTML aqui seria um template mais limpo e profissional
    html_template = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
    <meta charset="UTF-8" />
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 700px; margin: auto; padding: 20px; border-radius: 8px; background-color: #f9f9f9; }}
        h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        .section {{ background-color: #ecf0f1; border-left: 4px solid #3498db; padding: 15px; margin-bottom: 20px; border-radius: 4px; }}
        .nota-final {{ background-color: #dff0d8; border-left: 4px solid #2ecc71; padding: 20px; margin-top: 30px; font-weight: bold; font-size: 1.1em; color: #27ae60; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th, td {{ text-align: left; padding: 10px; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #bdc3c7; color: #fff; }}
        .parecer {{ margin-top: 10px; font-style: italic; color: #555; }}
    </style>
    </head>
    <body>
        <div class="container">
            <h2>🎉 Aprovação de Trabalho - VII SEMPI</h2>
            <p>Prezados(as) autores(as),</p>
            <p>Com grande satisfação, informamos que seu resumo expandido foi <strong>aprovado</strong> para apresentação oral na <strong>VII Semana Acadêmica da Propriedade Intelectual (VII SEMPI)</strong>.</p>
            
            <p>Confira abaixo as avaliações detalhadas do Comitê Científico:</p>

            <div class="section">
                <h3>👤 Avaliador(a) I</h3>
                <table>
                    <thead>
                        <tr><th>Critério</th><th>Nota</th></tr>
                    </thead>
                    <tbody>
                        {"".join(f"<tr><td>{i+1}. {c}</td><td>{formatar_nota_br(n)}</td></tr>" for i, (c, n) in enumerate(notas_i.items()))}
                    </tbody>
                </table>
                <p><strong>Média ponderada:</strong> {formatar_nota_br(media_i, 2)}</p>
                <p class="parecer">{parecer_i}</p>
            </div>
            
            <div class="section">
                <h3>👤 Avaliador(a) II</h3>
                <table>
                    <thead>
                        <tr><th>Critério</th><th>Nota</th></tr>
                    </thead>
                    <tbody>
                        {"".join(f"<tr><td>{i+1}. {c}</td><td>{formatar_nota_br(n)}</td></tr>" for i, (c, n) in enumerate(notas_ii.items()))}
                    </tbody>
                </table>
                <p><strong>Média ponderada:</strong> {formatar_nota_br(media_ii, 2)}</p>
                <p class="parecer">{parecer_ii}</p>
            </div>

            <div class="nota-final">
                Nota final do trabalho: <strong>{formatar_nota_br(nota_final, 2)}</strong>
            </div>
        </div>
    </body>
    </html>
    """
    return html_template

# --- Função Principal do Streamlit ---
def main():
    st.set_page_config(page_title="Gerador de HTML SEMPI", layout="wide")
    st.title("Gerador de Notificações Internas")
    
    # Adicionando um container para a identidade visual
    with st.container():
        st.markdown(
            f"""
            <div style="background-color: #004d99; padding: 15px; border-radius: 10px; color: white;">
                <h1 style="color: white; text-align: center;">💻 Notificação Interna Even3 (VII SEMPI)</h1>
                <p style="text-align: center; font-style: italic;">Ferramenta para facilitar a comunicação com os autores.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.sidebar.title("Navegação")
    abas = ["Aprovação", "Reprovação", "Desclassificação", "Lembretes", "Resultado Final"]
    aba = st.sidebar.radio("Selecione uma opção:", abas)

    # Exemplo para a aba de Aprovação
    if aba == "Aprovação":
        st.header("✅ Aprovação de Trabalho")
        
        col1, col2 = st.columns(2)

        # Avaliador I
        with col1:
            with st.expander("📝 Notas Avaliador I", expanded=True):
                notas_i = {}
                for criterio, peso in CRITERIOS_APROVACAO.items():
                    key = f"aprov_i_{criterio}"
                    nota = st.number_input(f"Nota para '{criterio}' (Peso: {peso})", min_value=0.0, max_value=10.0, step=0.1, key=key)
                    notas_i[criterio] = nota
                parecer_i = st.text_area("Parecer do Avaliador I", key="aprov_parecer_i")
                media_ponderada_i = calcular_media_ponderada(list(notas_i.values()), list(CRITERIOS_APROVACAO.values()))
                st.metric("Média Ponderada Avaliador I", formatar_nota_br(media_ponderada_i, 2))

        # Avaliador II
        with col2:
            with st.expander("📝 Notas Avaliador II", expanded=True):
                notas_ii = {}
                for criterio, peso in CRITERIOS_APROVACAO.items():
                    key = f"aprov_ii_{criterio}"
                    nota = st.number_input(f"Nota para '{criterio}' (Peso: {peso})", min_value=0.0, max_value=10.0, step=0.1, key=key)
                    notas_ii[criterio] = nota
                parecer_ii = st.text_area("Parecer do Avaliador II", key="aprov_parecer_ii")
                media_ponderada_ii = calcular_media_ponderada(list(notas_ii.values()), list(CRITERIOS_APROVACAO.values()))
                st.metric("Média Ponderada Avaliador II", formatar_nota_br(media_ponderada_ii, 2))

        nota_final_aprovacao = (media_ponderada_i + media_ponderada_ii) / 2
        st.subheader("Resultado Final")
        st.success(f"Nota final do trabalho: **{formatar_nota_br(nota_final_aprovacao, 2)}**")

        st.subheader("HTML Gerado")
        html_aprovacao = gerar_html_aprovacao(notas_i, media_ponderada_i, parecer_i, notas_ii, media_ponderada_ii, parecer_ii, nota_final_aprovacao)
        st.code(html_aprovacao, language="html")

if __name__ == "__main__":
    main()
