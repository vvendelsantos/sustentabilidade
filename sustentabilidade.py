import streamlit as st
from datetime import datetime

# Configurações da página
st.set_page_config(
    page_title="Gerador de HTML SEMPI",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cores e estilos personalizados
custom_css = """
<style>
    :root {
        --primary-color: #4a6fa5;
        --secondary-color: #166088;
        --accent-color: #4fc3f7;
        --success-color: #4caf50;
        --warning-color: #ff9800;
        --danger-color: #f44336;
        --light-bg: #f8f9fa;
        --dark-text: #212529;
    }
    
    .stApp {
        background-color: #f5f7fa;
    }
    
    .stSidebar {
        background-color: var(--primary-color) !important;
        color: white !important;
    }
    
    .stSidebar .sidebar-content {
        padding: 1rem;
    }
    
    .stButton>button {
        background-color: var(--secondary-color);
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: var(--accent-color);
        transform: translateY(-2px);
    }
    
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea,
    .stNumberInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #ced4da;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: var(--primary-color);
    }
    
    .tab-content {
        padding: 1rem;
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .highlight-box {
        background-color: var(--light-bg);
        border-left: 4px solid var(--accent-color);
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .success-box {
        background-color: #e8f5e9;
        border-left: 4px solid var(--success-color);
    }
    
    .warning-box {
        background-color: #fff3e0;
        border-left: 4px solid var(--warning-color);
    }
    
    .danger-box {
        background-color: #ffebee;
        border-left: 4px solid var(--danger-color);
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Funções auxiliares
def formatar_nota_br(nota, casas_decimais=1):
    """Formata notas no padrão brasileiro com vírgula decimal"""
    if nota == int(nota):
        return str(int(nota)).replace('.', ',')
    else:
        return f"{nota:.{casas_decimais}f}".replace('.', ',')

def calcular_media_ponderada(notas, pesos):
    """Calcula a média ponderada de uma lista de notas com seus respectivos pesos"""
    if not notas or not pesos or len(notas) != len(pesos):
        return 0.0
    soma_produtos = sum(nota * peso for nota, peso in zip(notas, pesos))
    soma_pesos = sum(pesos)
    return soma_produtos / soma_pesos if soma_pesos > 0 else 0.0

# Templates HTML
def get_email_template(template_type, **kwargs):
    """Retorna o template de e-mail apropriado com os valores preenchidos"""
    templates = {
        "desclassificacao": DESCLASSIFICACAO_HTML,
        "aprovacao": APROVACAO_HTML,
        "reprovacao": REPROVACAO_HTML,
        "lembrete_envio": LEMBRETE_ENVIO_HTML,
        "lembrete_apresentacao": LEMBRETE_APRESENTACAO_HTML,
        "resultado_final": RESULTADO_FINAL_HTML
    }
    return templates[template_type].format(**kwargs)

# Constantes com templates HTML
DESCLASSIFICACAO_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <style>
    body {{
      font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      line-height: 1.6;
      color: #333333;
      background-color: #ffffff;
      margin: 0;
      padding: 0 20px 20px 20px;
    }}
    .container {{
      max-width: 700px;
      margin: auto;
      padding: 20px;
    }}
    p {{
      margin-bottom: 16px;
      text-align: justify;
    }}
    .box {{
      background-color: #f8f9fa;
      border-left: 4px solid #ff9800;
      padding: 16px;
      margin: 20px 0;
      border-radius: 4px;
      text-align: justify;
    }}
    ol {{
      padding-left: 20px;
      margin: 0;
      text-align: justify;
    }}
    .header {{
      background-color: #166088;
      color: white;
      padding: 20px;
      text-align: center;
      border-radius: 4px 4px 0 0;
      margin-bottom: 20px;
    }}
    .footer {{
      margin-top: 20px;
      font-size: 0.9em;
      color: #666;
      text-align: center;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h2>VII Semana Acadêmica da Propriedade Intelectual</h2>
    </div>
    
    <p>Prezado(a) autor(a),</p>
    <p>Esperamos que esta mensagem o(a) encontre bem.</p>
    
    <div class="box">
      <p><strong>📌 Resultado da Análise Preliminar</strong></p>
      <p>Seu trabalho <strong>não atendeu</strong> integralmente às diretrizes estabelecidas pela Comissão Organizadora para avançar à próxima etapa de avaliação por pares.</p>
      <p><strong>Principais aspectos a serem corrigidos:</strong></p>
      <ol>
        {motivos_html}
      </ol>
    </div>
    
    <p>Solicitamos que as correções sejam realizadas e o trabalho corrigido seja ressubmetido no sistema até o dia <strong>19 de agosto de 2025</strong>.</p>
    
    <div class="footer">
      <p>VII SEMPI - Semana Acadêmica da Propriedade Intelectual</p>
      <p>submissoes.sempi@gmail.com</p>
    </div>
  </div>
</body>
</html>"""

# (Os outros templates HTML seriam definidos de forma similar, com estilos modernos)

# Página principal
def main():
    st.title("📝 Gerador de Comunicações - VII SEMPI")
    st.markdown("""
    <div class="highlight-box">
        Esta ferramenta auxilia na geração automatizada de comunicações para os participantes da 
        <strong>VII Semana Acadêmica da Propriedade Intelectual</strong>. Selecione o tipo de comunicação desejada na barra lateral.
    </div>
    """, unsafe_allow_html=True)
    
    # Menu lateral
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50?text=VII+SEMPI", use_column_width=True)
        st.markdown("### Navegação")
        menu_options = {
            "📋 Desclassificação": "desclassificacao",
            "✅ Aprovação": "aprovacao",
            "❌ Reprovação": "reprovacao",
            "🔔 Lembretes": "lembretes",
            "🏆 Resultado Final": "resultado_final"
        }
        selected = st.radio("Selecione o tipo de comunicação:", list(menu_options.keys()))
    
    # Conteúdo dinâmico baseado na seleção
    if menu_options[selected] == "desclassificacao":
        render_desclassificacao()
    elif menu_options[selected] == "aprovacao":
        render_aprovacao()
    # (Outras condições para cada tipo de comunicação)

# Funções de renderização para cada tipo de comunicação
def render_desclassificacao():
    with st.container():
        st.header("📋 Comunicação de Desclassificação")
        st.markdown("Preencha os campos abaixo para gerar a comunicação de desclassificação.")
        
        with st.expander("🔍 Detalhes da Desclassificação", expanded=True):
            motivos = st.text_area(
                "Liste os motivos da desclassificação (separados por /):",
                value="Formatação inadequada / Falta de elementos obrigatórios / Outro motivo",
                height=100
            )
            motivos_lista = [m.strip() for m in motivos.split("/") if m.strip()]
            
            data_limite = st.date_input("Data limite para ressubmissão:", value=datetime(2025, 8, 19))
            
            if st.button("Gerar Comunicação", key="btn_desclassificacao"):
                motivos_html = "".join(f"<li>{m}</li>" for m in motivos_lista)
                html = get_email_template(
                    "desclassificacao",
                    motivos_html=motivos_html,
                    data_limite=data_limite.strftime("%d de %B de %Y")
                )
                
                st.success("Comunicação gerada com sucesso!")
                with st.expander("📄 Visualizar HTML Gerado", expanded=True):
                    st.code(html, language="html")
                
                # Botões de ação
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.download_button(
                        label="📥 Baixar HTML",
                        data=html,
                        file_name="comunicacao_desclassificacao.html",
                        mime="text/html"
                    )
                with col2:
                    st.button("📋 Copiar para Área de Transferência")
                with col3:
                    st.button("📧 Enviar por E-mail")

# (Funções similares para render_aprovacao, render_reprovacao, etc.)

if __name__ == "__main__":
    main()
