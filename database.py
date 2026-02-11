from sqlalchemy import create_engine
import streamlit as st

# USE O SECRETS DO STREAMLIT (mais seguro)
DATABASE_URL = st.secrets["DATABASE_URL"]

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # reconecta automaticamente
    pool_size=5,
    max_overflow=10
)

def get_engine():
    return engine
