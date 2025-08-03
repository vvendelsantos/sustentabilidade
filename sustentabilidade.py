import streamlit as st
import random

st.set_page_config(page_title="Construa seu Portfólio Verde", layout="wide")
st.title("🌱 Construa seu Portfólio Verde")

st.markdown("""
Você é gestor de um fundo de inovação sustentável.  
Selecione **até 3 projetos** de patente nos quais deseja investir.  
Seu objetivo é maximizar o impacto ambiental e retorno tecnológico, com risco mínimo.
""")

# Projetos simulados
projetos = [
    {
        "titulo": "Tratamento de efluentes com cinza vulcânica",
        "resumo": "Uso de cinza vulcânica como coagulante natural para remover poluentes de efluentes industriais.",
        "custo": 3,
        "impacto": 8,
        "risco": 2,
        "retorno": 7,
        "ods": ["ODS 6", "ODS 12"]
    },
    {
        "titulo": "Sistema híbrido solar-eólico para comunidades isoladas",
        "resumo": "Tecnologia de geração elétrica off-grid combinando energia solar e eólica.",
        "custo": 4,
        "impacto": 9,
        "risco": 4,
        "retorno": 8,
        "ods": ["ODS 7", "ODS 13"]
    },
    {
        "titulo": "Biofertilizante feito com resíduos de pescado",
        "resumo": "Produção de fertilizantes orgânicos a partir de resíduos da indústria pesqueira.",
        "custo": 2,
        "impacto": 7,
        "risco": 3,
        "retorno": 6,
        "ods": ["ODS 2", "ODS 12"]
    },
    {
        "titulo": "Veículo urbano leve elétrico com baixo arrasto aerodinâmico",
        "resumo": "Projeto de microveículo elétrico com design eficiente para mobilidade urbana.",
        "custo": 5,
        "impacto": 8,
        "risco": 5,
        "retorno": 9,
        "ods": ["ODS 11", "ODS 9"]
    },
    {
        "titulo": "Sensor inteligente para controle de irrigação",
        "resumo": "Sensor que mede a umidade do solo e reduz desperdício de água em lavouras.",
        "custo": 3,
        "impacto": 6,
        "risco": 1,
        "retorno": 5,
        "ods": ["ODS 2", "ODS 6"]
    }
]

# Seleção de projetos
selecionados = st.multiselect(
    "Escolha até 3 pedidos para investir:",
    options=[p["titulo"] for p in projetos],
    max_selections=3
)

# Botão de avaliação
if st.button("💡 Avaliar Portfólio") and selecionados:
    total_custo = 0
    total_impacto = 0
    total_risco = 0
    total_retorno = 0
    ods_totais = set()

    for p in projetos:
        if p["titulo"] in selecionados:
            total_custo += p["custo"]
            total_impacto += p["impacto"]
            total_risco += p["risco"]
            total_retorno += p["retorno"]
            ods_totais.update(p["ods"])

    # Score final (pode ajustar fórmula depois)
    score = (total_impacto * 2 + total_retorno) - (total_risco * 1.5)

    st.success(f"🏆 Seu Portfólio Sustentável obteve um score final de: **{score:.1f}**")
    st.markdown(f"- **Custo total**: {total_custo}")
    st.markdown(f"- **Impacto ambiental total**: {total_impacto}")
    st.markdown(f"- **Risco médio**: {total_risco / len(selecionados):.1f}")
    st.markdown(f"- **Retorno estimado**: {total_retorno}")
    st.markdown(f"- **ODS atendidos**: {', '.join(sorted(ods_totais))}")

elif len(selecionados) == 0:
    st.info("Selecione pelo menos um projeto.")
