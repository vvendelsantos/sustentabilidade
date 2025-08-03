import streamlit as st
import random
import time

st.set_page_config(page_title="🎮 Construa seu Portfólio Verde", layout="wide")
st.markdown("## 🌱 Construa seu Portfólio Verde: O Desafio da Inovação Sustentável")
st.markdown("👩‍🔬 **Missão**: Escolher até 3 projetos de patente para investir e maximizar o impacto sustentável do seu fundo.")
st.markdown("---")

projetos = [
    {
        "titulo": "🔬 Cinza vulcânica no tratamento de efluentes",
        "resumo": "Tecnologia que usa cinza vulcânica como coagulante natural para tratar efluentes contaminados.",
        "custo": 3, "impacto": 8, "risco": 2, "retorno": 7,
        "ods": ["ODS 6", "ODS 12"]
    },
    {
        "titulo": "🔋 Sistema híbrido solar-eólico",
        "resumo": "Geração elétrica combinando painéis solares e turbinas eólicas em regiões remotas.",
        "custo": 4, "impacto": 9, "risco": 4, "retorno": 8,
        "ods": ["ODS 7", "ODS 13"]
    },
    {
        "titulo": "🌿 Biofertilizante com resíduos de pescado",
        "resumo": "Conversão de resíduos orgânicos da pesca em fertilizantes agrícolas.",
        "custo": 2, "impacto": 7, "risco": 3, "retorno": 6,
        "ods": ["ODS 2", "ODS 12"]
    },
    {
        "titulo": "🚗 Microveículo elétrico urbano",
        "resumo": "Veículo elétrico de baixo custo e alto desempenho aerodinâmico para cidades.",
        "custo": 5, "impacto": 8, "risco": 5, "retorno": 9,
        "ods": ["ODS 11", "ODS 9"]
    },
    {
        "titulo": "💧 Sensor de irrigação inteligente",
        "resumo": "Sensor que otimiza irrigação agrícola com base em umidade do solo.",
        "custo": 3, "impacto": 6, "risco": 1, "retorno": 5,
        "ods": ["ODS 2", "ODS 6"]
    }
]

st.subheader("📋 Projetos disponíveis")
selecionados = st.multiselect("Escolha até 3 para investir:", options=[p["titulo"] for p in projetos], max_selections=3)

if st.button("🚀 Lançar Investimento"):
    if not selecionados:
        st.warning("⚠️ Selecione ao menos um projeto!")
    else:
        with st.spinner("🔍 Avaliando seu portfólio..."):
            time.sleep(2)

        total_impacto = sum(p["impacto"] for p in projetos if p["titulo"] in selecionados)
        total_risco = sum(p["risco"] for p in projetos if p["titulo"] in selecionados)
        total_retorno = sum(p["retorno"] for p in projetos if p["titulo"] in selecionados)
        score = (total_impacto * 2 + total_retorno) - (total_risco * 1.5)

        if score >= 35:
            feedback = "🏆 **Inovador Verde** — Seu portfólio é exemplar!"
        elif score >= 28:
            feedback = "🥈 **Inovador Promissor** — Bons projetos com impacto!"
        else:
            feedback = "🔍 **Risco alto detectado** — Reavalie suas escolhas."

        st.success(feedback)
        st.metric("🎯 Score Final", f"{score:.1f}")
        st.progress(min(score / 50, 1.0))

        st.markdown("### 📊 Detalhes do Portfólio:")
        st.markdown(f"- Impacto Ambiental Total: **{total_impacto}**")
        st.markdown(f"- Risco Técnico Total: **{total_risco}**")
        st.markdown(f"- Retorno Tecnológico: **{total_retorno}**")

        ods_final = set()
        for p in projetos:
            if p["titulo"] in selecionados:
                ods_final.update(p["ods"])
        st.markdown(f"- ODS Atendidos: {', '.join(sorted(ods_final))}")
