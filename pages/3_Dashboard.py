import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_connection

st.set_page_config(layout="wide")

st.title("📊 Dashboard Financeiro e Operacional")

engine = get_connection()

# ----------------------------
# CARREGAR DADOS
# ----------------------------
@st.cache_data
def carregar_dados():
    query = "SELECT * FROM vw_indicadores_empresa"
    return pd.read_sql(query, engine)

df = carregar_dados()

if df.empty:
    st.warning("Nenhum dado encontrado na view.")
    st.stop()

# ----------------------------
# TRATAMENTO
# ----------------------------
df["periodo"] = pd.to_datetime(df["periodo"], errors="coerce")
df = df.dropna(subset=["periodo"])
df = df.sort_values("periodo")

df["ano"] = df["periodo"].dt.year
df["mes"] = df["periodo"].dt.month

df["total_recebido"] = df["receita"] + df["subsidio"]

df["percentual_subsidio"] = (
    df["subsidio"] / df["total_recebido"]
) * 100

# ----------------------------
# FILTRO
# ----------------------------
empresas = st.multiselect(
    "Selecione a(s) empresa(s)",
    df["nome"].unique(),
    default=df["nome"].unique()
)

df = df[df["nome"].isin(empresas)]

# ============================
# 1️⃣ RECEITA AO LONGO DO ANO
# ============================
st.subheader("📈 Receita ao longo do Ano")

fig1 = px.line(
    df,
    x="periodo",
    y="receita",
    color="nome",
    markers=True
)

st.plotly_chart(fig1, use_container_width=True)

# ============================
# 2️⃣ SUBSÍDIO AO LONGO DO ANO
# ============================
st.subheader("💰 Subsídio ao longo do Ano")

fig2 = px.line(
    df,
    x="periodo",
    y="subsidio",
    color="nome",
    markers=True
)

st.plotly_chart(fig2, use_container_width=True)

# ==============================================
# 3️⃣ % DE SUBSÍDIO SOBRE TOTAL RECEBIDO (MÊS)
# ==============================================
st.subheader("📊 Percentual de Subsídio sobre o Total Recebido (Mensal)")

fig3 = px.bar(
    df,
    x="periodo",
    y="percentual_subsidio",
    color="nome",
    text=df["percentual_subsidio"].round(1)
)

fig3.update_traces(textposition="outside")
fig3.update_layout(yaxis_title="% Subsídio")

st.plotly_chart(fig3, use_container_width=True)

# ==================================
# 4️⃣ KM PERCORRIDOS POR MÊS
# ==================================
st.subheader("🚌 Quilômetros Percorridos por Mês")

fig4 = px.bar(
    df,
    x="periodo",
    y="km_total",
    color="nome",
)

st.plotly_chart(fig4, use_container_width=True)

# ==================================================
# 5️⃣ RELAÇÃO FATURAMENTO x KM RODADO
# ==================================================
st.subheader("📉 Relação entre Faturamento e KM Rodado")

fig5 = px.scatter(
    df,
    x="km_total",
    y="receita",
    color="nome",
    size="subsidio",
    hover_data=["periodo"],
)

st.plotly_chart(fig5, use_container_width=True)
