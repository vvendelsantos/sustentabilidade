import streamlit as st
from typing import List, Tuple, Dict
from dataclasses import dataclass
from datetime import datetime

# Configurações globais
CONFIG = {
    "event_name": "VII Semana Acadêmica da Propriedade Intelectual (VII SEMPI)",
    "event_url": "https://www.even3.com.br/vii-semana-academica-da-propriedade-intelectual-594540/",
    "submission_email": "submissoes.sempi@gmail.com",
    "submission_deadline": "29 de agosto de 2025",
    "resubmission_deadline": "19 de agosto de 2025",
    "theme_colors": {
        "primary": "#1a73e8",
        "secondary": "#f1f3f4",
        "success": "#4caf50",
        "error": "#d32f2f",
        "highlight": "#e0f7fa"
    }
}

# Critérios de avaliação
CRITERIOS_APROVACAO_REPROVACAO = [
    ("Correspondência ao tema do evento e à seção temática", 2),
    ("Originalidade e contribuição na área da Propriedade Intelectual", 1),
    ("Definição clara do problema, objetivos e justificativa", 2),
    ("Adequação dos métodos à pesquisa e confiabilidade", 2),
    ("Clareza, coerência e objetividade na apresentação dos resultados", 3)
]

CRITERIOS_RESULTADO_FINAL = CRITERIOS_APROVACAO_REPROVACAO + [
    ("Domínio do conteúdo apresentado", 2),
    ("Adequação ao tempo de apresentação", 1)
]

# Estilo CSS global para HTML
BASE_CSS = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
        body {
            font-family: 'Roboto', Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            background-color: #fafafa;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: auto;
            background: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        p {
            margin-bottom: 20px;
            text-align: justify;
        }
        a {
            color: {primary};
            text-decoration: none;
            transition: color 0.3s ease;
        }
        a:hover {
            color: darken({primary}, 10%);
            text-decoration: underline;
        }
        .highlight {
            background: {highlight};
            border-left: 4px solid {primary};
            padding: 15px 20px;
            border-radius: 6px;
            margin: 20px 0;
            font-size: 0.95em;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: {secondary};
            font-weight: bold;
        }
        .nota-final {
            background-color: {success};
            border-left: 4px solid {primary};
            padding: 15px;
            margin-top: 20px;
            border-radius: 6px;
            font-weight: bold;
        }
        .parecer {
            font-style: italic;
            color: #555;
            margin-top: 10px;
        }
        @media (max-width: 600px) {
            .container {
                padding: 15px;
            }
        }
    </style>
""".format(**CONFIG["theme_colors"])

@dataclass
class Avaliacao:
    notas: Dict[str, float]
    media_ponderada: float
    parecer: str

def formatar_nota_br(nota: float, casas_decimais: int = 1) -> str:
    """Formata número no padrão brasileiro."""
    if nota == int(nota):
        return str(int(nota)).replace('.', ',')
    return f"{nota:.{casas_decimais}f}".replace('.', ',')

def calcular_media_ponderada(notas: List[float], pesos: List[int]) -> float:
    """Calcula a média ponderada."""
    if not notas or not pesos or len(notas) != len(pesos):
        return 0.0
    soma_produtos = sum(nota * peso for nota, peso in zip(notas, pesos))
    soma_pesos = sum(pesos)
    return soma_produtos / soma_pesos if soma_pesos > 0 else 0.0

def gerar_html_desclassificacao(motivos: List[str]) -> str:
    """Gera HTML para notificação de desclassificação."""
    motivos_html = "".join(f"<li>{m}</li>" for m in motivos)
    return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    {BASE_CSS}
</head>
<body>
    <div class="container">
        <p>Prezado(a) autor(a),</p>
        <p>Esperamos que esta mensagem o(a) encontre bem.</p>
        <p>Agradecemos o envio do seu resumo expandido à <strong>{CONFIG['event_name']}</strong>. Após análise preliminar (<em>desk review</em>), informamos que seu trabalho <strong>não atendeu</strong> às diretrizes estabelecidas.</p>
        <div class="highlight">
            <p><strong>📌 Principais aspectos a serem corrigidos:</strong></p>
            <ol>{motivos_html}</ol>
        </div>
        <p>Solicitamos que as correções sejam realizadas e o trabalho ressubmetido até <strong>{CONFIG['resubmission_deadline']}</strong>.</p>
        <p>Permanecemos à disposição para quaisquer dúvidas.</p>
    </div>
</body>
</html>
"""

def gerar_html_aprovacao_reprovacao(tipo: str, avaliacao_i: Avaliacao, avaliacao_ii: Avaliacao, nota_final: float) -> str:
    """Gera HTML para aprovação ou reprovação."""
    status = "aprovado" if tipo == "Aprovação" else "reprovado"
    nota_final_class = "nota-final" if tipo == "Aprovação" else "nota-final error"
    criterios = [c[0] for c in CRITERIOS_APROVACAO_REPROVACAO]
    
    tabela_i = "".join(f'<tr><td>{i+1}. {c}</td><td>{formatar_nota_br(avaliacao_i.notas[c])}</td></tr>' 
                       for i, c in enumerate(criterios))
    tabela_ii = "".join(f'<tr><td>{i+1}. {c}</td><td>{formatar_nota_br(avaliacao_ii.notas[c])}</td></tr>' 
                        for i, c in enumerate(criterios))
    
    return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    {BASE_CSS}
    <style>
        .error {{ background-color: {CONFIG['theme_colors']['error']}; color: #fff; }}
    </style>
</head>
<body>
    <div class="container">
        <p>Prezados(as),</p>
        <p>Esperamos que esta mensagem os(as) encontre bem.</p>
        <p>Informamos que o seu resumo expandido foi <strong>{status}</strong> para apresentação na <strong>{CONFIG['event_name']}</strong>.</p>
        <div class="highlight">
            <p><strong>👤 Avaliador(a) I</strong></p>
            <table>
                <tr><th>Critério</th><th>Nota</th></tr>
                {tabela_i}
            </table>
            <p><strong>Média ponderada: {formatar_nota_br(avaliacao_i.media_ponderada, 2)}</strong></p>
            <p class="parecer">{avaliacao_i.parecer}</p>
        </div>
        <div class="highlight">
            <p><strong>👤 Avaliador(a) II</strong></p>
            <table>
                <tr><th>Critério</th><th>Nota</th></tr>
                {tabela_ii}
            </table>
            <p><strong>Média ponderada: {formatar_nota_br(avaliacao_ii.media_ponderada, 2)}</strong></p>
            <p class="parecer">{avaliacao_ii.parecer}</p>
        </div>
        <div class="{nota_final_class}">
            Nota final do trabalho: <strong>{formatar_nota_br(nota_final, 2)}</strong>
        </div>
        <p>Consulte as orientações no site do evento: <br>
        <a href="{CONFIG['event_url']}" target="_blank">{CONFIG['event_url']}</a></p>
        <p>Permanecemos à disposição.</p>
    </div>
</body>
</html>
"""

def gerar_html_lembrete_envio(texto_envio_arquivo: str) -> str:
    """Gera HTML para lembrete de envio de arquivo."""
    return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    {BASE_CSS}
</head>
<body>
    <div class="container">
        <p>Prezados(as) autores(as),</p>
        <p>Esperamos que esta mensagem os(as) encontre bem.</p>
        <p>A Comissão Organizadora da <strong>{CONFIG['event_name']}</strong> relembra que os trabalhos aprovados devem ser apresentados em sessão pública e avaliados pelo Comitê Científico.</p>
        <p>{texto_envio_arquivo}</p>
        <div class="highlight">
            <p>Se o autor principal não puder apresentar, um coautor inscrito deve ser designado e comunicado até <strong>{CONFIG['submission_deadline']}</strong> via <a href="mailto:{CONFIG['submission_email']}">{CONFIG['submission_email']}</a>.</p>
        </div>
        <p>Consulte a programação no site: <a href="{CONFIG['event_url']}" target="_blank">{CONFIG['event_url']}</a>.</p>
        <p>Permanecemos à disposição.</p>
    </div>
</body>
</html>
"""

def gerar_html_lembrete_apresentacao(tempo_apresentacao: int, tempo_arguicao: int) -> str:
    """Gera HTML para lembrete de apresentação."""
    return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    {BASE_CSS}
</head>
<body>
    <div class="container">
        <p>Prezados(as),</p>
        <p>A Comissão Organizadora da <strong>{CONFIG['event_name']}</strong> relembra que as apresentações ocorrerão <strong>amanhã</strong>. Consulte a programação em: <a href="{CONFIG['event_url']}" target="_blank">{CONFIG['event_url']}</a>.</p>
        <div class="highlight">
            <p><strong>⚠️ Orientações importantes:</strong></p>
            <ul>
                <li>Comparecer com <strong>20 minutos de antecedência</strong>.</li>
                <li>Não serão permitidas correções no arquivo durante o evento.</li>
            </ul>
        </div>
        <p>Cada apresentador(a) terá <strong>{tempo_apresentacao} minutos</strong> para exposição e <strong>{tempo_arguicao} minutos</strong> para arguição.</p>
        <p>Permanecemos à disposição.</p>
    </div>
</body>
</html>
"""

def coletar_notas(criterios: List[Tuple[str, int]], key_prefix: str) -> Tuple[Dict[str, float], float]:
    """Coletar notas do usuário e calcular média ponderada."""
    nomes_criterios = [c[0] for c in criterios]
    pesos = [c[1] for c in criterios]
    
    st.markdown(f"**Critérios de Avaliação**")
    for i, criterio in enumerate(nomes_criterios, 1):
        st.write(f"{i}. {criterio} (Peso: {pesos[i-1]})")
    
    default_notas = "\n".join(["0.0" for _ in nomes_criterios])
    notas_input = st.text_area(
        "Digite as notas (uma por linha):",
        value=default_notas,
        key=f"{key_prefix}_input"
    )
    
    try:
        notas = [float(n.strip().replace(',', '.')) for n in notas_input.split('\n') if n.strip()]
        if len(notas) != len(nomes_criterios):
            st.warning(f"Insira exatamente {len(nomes_criterios)} notas.")
            return {c: 0.0 for c in nomes_criterios}, 0.0
        return {c: n for c, n in zip(nomes_criterios, notas)}, calcular_media_ponderada(notas, pesos)
    except ValueError:
        st.error("Insira notas válidas (números).")
        return {c: 0.0 for c in nomes_criterios}, 0.0

def main():
    """Função principal do aplicativo Streamlit."""
    st.set_page_config(
        page_title="Gerador de HTML SEMPI",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Tema personalizado
    st.markdown("""
        <style>
            .stApp {
                background-color: #f5f5f5;
            }
            .sidebar .sidebar-content {
                background-color: #ffffff;
                border-right: 1px solid #ddd;
            }
            h1, h2, h3 {
                color: #1a73e8;
            }
            .stButton>button {
                background-color: #1a73e8;
                color: white;
                border-radius: 8px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("📊 Gerador de Notificações - VII SEMPI")
    st.markdown(f"Gerencie notificações para a **{CONFIG['event_name']}** com facilidade e profissionalismo.")

    abas = ["Desclassificação", "Aprovação", "Reprovação", "Lembretes", "Resultado Final"]
    aba = st.sidebar.selectbox("Selecione a aba:", abas)

    if aba == "Desclassificação":
        with st.container():
            st.header("📛 Desclassificação")
            motivos = st.text_area(
                "Motivos da desclassificação (separados por '/'):",
                value="Falta de clareza / Formatação incorreta / Fora do tema"
            )
            motivos_lista = [m.strip() for m in motivos.split("/") if m.strip()]
            if motivos_lista:
                html = gerar_html_desclassificacao(motivos_lista)
                st.code(html, language="html")
            else:
                st.error("Insira pelo menos um motivo válido.")

    elif aba in ["Aprovação", "Reprovação"]:
        with st.container():
            st.header(f"{'✅' if aba == 'Aprovação' else '❌'} {aba}")
            
            st.subheader("Avaliador(a) I")
            notas_i, media_i = coletar_notas(CRITERIOS_APROVACAO_REPROVACAO, f"{aba.lower()}_i")
            if media_i > 0:
                st.info(f"Média ponderada: **{formatar_nota_br(media_i, 2)}**")
            parecer_i = st.text_area("Parecer Avaliador(a) I", value="Parecer detalhado.", key=f"{aba.lower()}_parecer_i")
            
            st.subheader("Avaliador(a) II")
            notas_ii, media_ii = coletar_notas(CRITERIOS_APROVACAO_REPROVACAO, f"{aba.lower()}_ii")
            if media_ii > 0:
                st.info(f"Média ponderada: **{formatar_nota_br(media_ii, 2)}**")
            parecer_ii = st.text_area("Parecer Avaliador(a) II", value="Parecer detalhado.", key=f"{aba.lower()}_parecer_ii")
            
            nota_final = (media_i + media_ii) / 2 if media_i > 0 and media_ii > 0 else 0.0
            st.metric("Nota Final do Trabalho", formatar_nota_br(nota_final, 2))
            
            avaliacao_i = Avaliacao(notas_i, media_i, parecer_i)
            avaliacao_ii = Avaliacao(notas_ii, media_ii, parecer_ii)
            html = gerar_html_aprovacao_reprovacao(aba, avaliacao_i, avaliacao_ii, nota_final)
            st.code(html, language="html")

    elif aba == "Lembretes":
        with st.container():
            st.header("⏰ Lembretes")
            
            st.markdown("#### Envio do Arquivo")
            texto_envio = st.text_area(
                "Texto para envio do arquivo:",
                value=f"Solicitamos o envio do arquivo até <strong>{CONFIG['submission_deadline']}</strong> em formato PDF."
            )
            st.code(gerar_html_lembrete_envio(texto_envio), language="html")
            
            st.markdown("#### Apresentação")
            col1, col2 = st.columns(2)
            with col1:
                tempo_apresentacao = st.number_input("Tempo de apresentação (min)", min_value=1, max_value=60, value=10)
            with col2:
                tempo_arguicao = st.number_input("Tempo de arguição (min)", min_value=1, max_value=30, value=5)
            st.code(gerar_html_lembrete_apresentacao(tempo_apresentacao, tempo_arguicao), language="html")

    elif aba == "Resultado Final":
        with st.container():
            st.header("🏆 Resultado Final")
            
            st.subheader("Avaliador(a) I - Apresentação")
            notas_i, media_i = coletar_notas(CRITERIOS_RESULTADO_FINAL, "final_i")
            if media_i > 0:
                st.info(f"Média ponderada: **{formatar_nota_br(media_i, 2)}**")
            
            st.subheader("Avaliador(a) II - Apresentação")
            notas_ii, media_ii = coletar_notas(CRITERIOS_RESULTADO_FINAL, "final_ii")
            if media_ii > 0:
                st.info(f"Média ponderada: **{formatar_nota_br(media_ii, 2)}**")
            
            nota_final_apresentacao = (media_i + media_ii) / 2 if media_i > 0 and media_ii > 0 else 0.0
            st.metric("Nota da Apresentação Oral", formatar_nota_br(nota_final_apresentacao, 2))
            
            nota_escrito = st.number_input("Nota do Trabalho Escrito", min_value=0.0, max_value=10.0, step=0.1, value=0.0)
            nota_geral = calcular_media_ponderada([nota_escrito, nota_final_apresentacao], [7, 3])
            st.metric("Nota Geral", formatar_nota_br(nota_geral, 2))
            
            hora_encerramento = st.text_input("Hora da cerimônia de encerramento", value="19h")
            # HTML para resultado final pode ser implementado conforme necessário

if __name__ == "__main__":
    main()
