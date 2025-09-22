import streamlit as st

# --- Configuração da página ---
st.set_page_config(page_title="Gerador de HTML SEMPI", layout="wide")
st.title("Gerador de HTML - Avaliação Final SEMPI")

# --- Campos do formulário ---
st.header("Informações principais")
resultado = st.selectbox("Resultado do artigo:", ["APROVADO", "REPROVADO"])
revista1 = st.text_input("Nome da primeira revista parceira:", "Revista Meio Ambiente e Sustentabilidade")
revista2 = st.text_input("Nome da segunda revista parceira:", "Revista Sustentabilidade e Sociedade")
revista_final = st.text_input("Nome da revista para substituir 'nas revistas parceiras':", "")
link_revista = st.text_input("Link de cadastro no sistema da revista:", 
                             "https://www.revistasuninter.com/revistameioambiente/index.php/meioAmbiente/login")

st.header("Avaliação dos critérios")
criterios = [
    "Embasamento teórico",
    "Metodologia",
    "Resultados e discussão",
    "Adequação ao template",
    "Revisão linguística",
    "Relatório de similaridade",
    "Sugestões dos avaliadores"
]

# Descrições detalhadas
descricao_criterios = {
    "Embasamento teórico": "O artigo apresenta embasamento teórico adequado e atualizado, apoiando os argumentos e hipóteses.",
    "Metodologia": "Os métodos utilizados estão descritos de forma clara, confiável e replicável.",
    "Resultados e discussão": "Os resultados são apresentados de forma organizada e a discussão é coerente com os objetivos do estudo.",
    "Adequação ao template": "O artigo segue corretamente o template exigido pela revista parceira.",
    "Revisão linguística": "O texto está livre de erros ortográficos e gramaticais significativos.",
    "Relatório de similaridade": "O índice de similaridade é inferior a 10% e não apresenta trechos problemáticos.",
    "Sugestões dos avaliadores": "As sugestões de ajustes indicadas na etapa anterior foram devidamente atendidas."
}

avaliacoes = {}
for criterio in criterios:
    avaliacoes[criterio] = st.radio(f"{criterio}:", ["Sim", "Parcialmente", "Não"], index=0, horizontal=True)

st.header("Comentário ao editor")
codigo_permissao = st.text_input("Código de permissão:", "XXXXX")
revista_editor = st.selectbox("Selecione a revista para o comentário ao editor:", [revista1, revista2])

# --- Botão para gerar HTML ---
if st.button("Gerar HTML"):
    publicacao_texto = revista_final if (resultado=="APROVADO" and revista_final.strip() != "") else ("nas revistas parceiras" if resultado=="APROVADO" else "o resumo expandido será publicado nos anais do evento")

    html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Avaliação do Artigo – Resultado Final</title>
<style>
body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #eaf6ea; margin: 0; padding: 20px; color: #1c3d25; }}
.container {{ max-width: 900px; margin: 0 auto; background-color: #ffffff; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); overflow: hidden; }}
.header {{ background-color: #c6e7c3; padding: 20px 30px; border-bottom: 3px solid #94d194; text-align: center; }}
.header h1 {{ margin: 0; font-size: 22px; color: #0f3c1d; }}
.content {{ padding: 30px; line-height: 1.65; text-align: justify; }}
table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
th, td {{ border: 1px solid #c6e7c3; padding: 12px; text-align: center; }}
th {{ background-color: #dff4df; color: #0f3c1d; font-weight: bold; }}
td:first-child {{ text-align: justify; }}
.recommendation {{ background-color: #dff4df; border: 2px solid #94d194; border-radius: 12px; text-align: center; padding: 20px; margin-top: 30px; font-size: 20px; font-weight: bold; color: #0f3c1d; }}
.instructions {{ margin-top: 30px; background-color: #f5faf5; border-left: 4px solid #94d194; padding: 20px; text-align: left; }}
.instructions h2 {{ font-size: 18px; color: #0f3c1d; margin-top: 0; }}
.instructions ol {{ padding-left: 20px; text-align: left; }}
</style>
</head>
<body>
<div class="container">
<div class="header">
<h1>Resultado Final da Avaliação do Artigo</h1>
</div>
<div class="content">
<p>Prezados(as) autores(as),</p>
<p>É com satisfação que comunicamos o <strong>resultado final</strong> da avaliação do artigo submetido à 
VII Semana Acadêmica da Propriedade Intelectual (SEMPI). 
Após análise criteriosa do Comitê Científico, informamos que o trabalho {"foi <strong>APROVADO</strong>" if resultado=="APROVADO" else "<strong>REPROVADO</strong>"} para publicação {publicacao_texto}.</p>
"""

    # --- Tabela de avaliação ---
    html += "<table><thead><tr><th>Afirmação Avaliada</th><th>Sim</th><th>Parcialmente</th><th>Não</th></tr></thead><tbody>"
    for criterio in criterios:
        html += f"<tr><td>{descricao_criterios[criterio]}</td>"
        html += f"<td style='background-color: {'#b3f0b3' if avaliacoes[criterio]=='Sim' else '#ffffff'}; font-size: 26px;'>{'☑' if avaliacoes[criterio]=='Sim' else '☐'}</td>"
        html += f"<td style='background-color: {'#ffd699' if avaliacoes[criterio]=='Parcialmente' else '#ffffff'}; font-size: 26px;'>{'☑' if avaliacoes[criterio]=='Parcialmente' else '☐'}</td>"
        html += f"<td style='background-color: {'#ff9999' if avaliacoes[criterio]=='Não' else '#ffffff'}; font-size: 26px;'>{'☑' if avaliacoes[criterio]=='Não' else '☐'}</td></tr>"
    html += "</tbody></table>"

    html += f'<div class="recommendation">Recomendação Final: <strong>{resultado}</strong></div>'

    # --- Orientações finais se aprovado ---
    if resultado=="APROVADO":
        html += f"""
<div class="instructions">
<h2>Orientações para Submissão</h2>
<ol>
<li>Certifique-se de enviar a versão final do trabalho. Alterações substanciais no conteúdo, bem como a inclusão ou exclusão de autores, não são permitidas.</li>
<li>Submeta o artigo no sistema da revista até o dia <strong>30/09/2025</strong>.</li>
<li>Cadastre-se no sistema da revista, caso ainda não o tenha feito: <a href="{link_revista}" target="_blank">{link_revista}</a></li>
<li>Acesse o menu de submissão. Lembre-se de cadastrar todos os autores no sistema.</li>
<li>No campo "Comentários ao editor", insira o seguinte texto:<br><br>
<p style="text-align: justify;">
<em>
Prezado editor-chefe, este trabalho foi apresentado na VII Semana Acadêmica da Propriedade Intelectual (SEMPI), aprovado pelo Comitê Científico e recebeu autorização para submissão na {revista_editor} em 26/09/2025, com o código de permissão <strong>{codigo_permissao}</strong>.
</em>
</p>
<br>
</li>
<li>Não é necessário anexar o relatório de similaridade (plágio); a Comissão Organizadora se encarregará de enviá-lo diretamente ao editor-chefe.</li>
<li>Revise todos os dados antes de finalizar a submissão. A Comissão Organizadora não se responsabiliza por uma possível rejeição do artigo por parte do editor-chefe.</li>
</ol>
</div>
"""

    # --- Fechamento sem rodapé ---
    html += """
</div>
</body>
</html>
"""

    st.subheader("HTML Gerado")
    st.code(html, language="html")
    st.download_button("Baixar HTML", html, file_name="resultado_final.html", mime="text/html")
