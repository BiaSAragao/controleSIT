import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_connection

st.set_page_config(layout="wide")

engine = get_connection()

st.title("📊 Dashboard do Sistema")

# ----------------------------
# CARREGAMENTO COM CACHE
# ----------------------------
@st.cache_data
def carregar_dados():
    query = "SELECT * FROM vw_indicadores_empresa"
    return pd.read_sql(query, engine)

df = carregar_dados()

# ----------------------------
# DEBUG (pode remover depois)
# ----------------------------
st.write("Total de registros:", len(df))

if df.empty:
    st.warning("Nenhum dado encontrado na view.")
    st.stop()

# Garantir tipo datetime
df["periodo"] = pd.to_datetime(df["periodo"], errors="coerce")

# Remover linhas inválidas
df = df.dropna(subset=["periodo"])

# Ordenar por período
df = df.sort_values("periodo")

# ----------------------------
# FILTROS
# ----------------------------
empresas = st.multiselect(
    "Filtrar Empresa",
    options=df["nome"].unique(),
    default=df["nome"].unique()
)

df = df[df["nome"].isin(empresas)]

# ----------------------------
# RECEITA vs SUBSÍDIO
# ----------------------------
st.subheader("💰 Receita vs Subsídio")

fig1 = px.bar(
    df,
    x="periodo",
    y=["receita", "subsidio"],
    color="nome",
    barmode="group",
)

st.plotly_chart(fig1, use_container_width=True)

# ----------------------------
# SUBSÍDIO POR KM
# ----------------------------
if "subsidio_por_km" in df.columns:

    st.subheader("🚍 Subsídio por KM")

    fig2 = px.bar(
        df,
        x="periodo",
        y="subsidio_por_km",
        color="nome",
    )

    st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# RANKING
# ----------------------------
st.subheader("🏆 Ranking de Empresas por Subsídio")

ranking = (
    df.groupby("nome")["subsidio"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

st.dataframe(ranking, use_container_width=True)
