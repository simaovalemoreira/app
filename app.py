import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração inicial da página
st.set_page_config(page_title="HealthData Insights", layout="wide")

st.title("📊 HealthData Insights - Dashboard de Saúde")

# Upload do arquivo Excel
uploaded_file = st.file_uploader("Faça o upload do arquivo Excel", type=["xlsx"])

if uploaded_file:
    # Carregar as planilhas
    pacientes = pd.read_excel(uploaded_file, sheet_name="Pacientes")
    atendimentos = pd.read_excel(uploaded_file, sheet_name="Atendimentos")
    financeiro = pd.read_excel(uploaded_file, sheet_name="Financeiro")
    satisfacao = pd.read_excel(uploaded_file, sheet_name="Satisfação")

    # KPIs principais
    total_atendimentos = len(atendimentos)
    receita_total = financeiro["Receita"].sum()
    tempo_medio_atendimento = atendimentos["Duração_Atendimento_Min"].mean()
    nps_medio = satisfacao["NPS"].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📅 Total de Atendimentos", total_atendimentos)
    col2.metric("💰 Receita Total", f"R$ {receita_total:,.2f}")
    col3.metric("⏳ Tempo Médio de Atendimento", f"{tempo_medio_atendimento:.1f} min")
    col4.metric("😊 NPS Médio", f"{nps_medio:.1f}")

    # Gráficos Interativos
    st.subheader("📈 Evolução Financeira")
    fig_financeiro = px.line(financeiro, x="Data", y=["Receita", "Despesas"], markers=True, title="Receita x Despesas")
    st.plotly_chart(fig_financeiro, use_container_width=True)

    st.subheader("🔬 Atendimentos por Especialidade")
    fig_especialidade = px.bar(atendimentos, x="Especialidade", title="Distribuição de Atendimentos por Especialidade")
    st.plotly_chart(fig_especialidade, use_container_width=True)

    st.subheader("👨‍⚕️ Tempo Médio por Médico")
    fig_medico = px.box(atendimentos, x="Médico_Responsável", y="Duração_Atendimento_Min",
                         title="Tempo Médio de Atendimento por Médico")
    st.plotly_chart(fig_medico, use_container_width=True)

    st.subheader("📊 NPS - Satisfação do Paciente")
    fig_nps = px.histogram(satisfacao, x="NPS", nbins=10, title="Distribuição de NPS (Satisfação)")
    st.plotly_chart(fig_nps, use_container_width=True)

else:
    st.info("Por favor, faça o upload do arquivo Excel para visualizar o dashboard.")

