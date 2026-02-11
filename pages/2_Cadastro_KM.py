import streamlit as st
import pandas as pd
from database import get_connection

engine = get_connection()

st.title("Cadastro de Quilometragem")

empresas = pd.read_sql("SELECT id_empresa, nome FROM empresas ORDER BY nome", engine)

empresa = st.selectbox("Empresa", empresas["nome"])

id_empresa = empresas.loc[
    empresas["nome"] == empresa, "id_empresa"
].values[0]

periodo = st.date_input("Período")

km_aferido = st.number_input("KM Aferido", min_value=0.0, format="%.3f")
km_total = st.number_input("KM Total", min_value=0.0, format="%.3f")

if st.button("Salvar KM"):

    query = """
        INSERT INTO fato_km_empresa
        (id_empresa, periodo, km_aferido, km_total)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id_empresa, periodo)
        DO UPDATE SET
            km_aferido = EXCLUDED.km_aferido,
            km_total = EXCLUDED.km_total;
    """

    with engine.begin() as conn:
        conn.execute(query, (id_empresa, periodo, km_aferido, km_total))

    st.success("KM salvo com sucesso!")
