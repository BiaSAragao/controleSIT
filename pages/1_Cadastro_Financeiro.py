import streamlit as st
import pandas as pd
from database import get_connection

engine = get_connection()

st.title("Cadastro Financeiro")

empresas = pd.read_sql("SELECT id_empresa, nome FROM empresas ORDER BY nome", engine)

empresa = st.selectbox(
    "Empresa",
    empresas["nome"]
)

id_empresa = empresas.loc[
    empresas["nome"] == empresa, "id_empresa"
].values[0]

periodo = st.date_input("Período (use o primeiro dia do mês)")

receita = st.number_input("Receita", min_value=0.0, format="%.2f")
subsidio = st.number_input("Subsídio", min_value=0.0, format="%.2f")

if st.button("Salvar"):

    query = """
        INSERT INTO fato_financeiro_empresa
        (id_empresa, periodo, receita, subsidio)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id_empresa, periodo)
        DO UPDATE SET
            receita = EXCLUDED.receita,
            subsidio = EXCLUDED.subsidio;
    """

    with engine.begin() as conn:
        conn.execute(query, (id_empresa, periodo, receita, subsidio))

    st.success("Dados salvos com sucesso!")
