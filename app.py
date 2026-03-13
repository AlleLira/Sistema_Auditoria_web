import streamlit as st
from modules.conferencias_page import tela_conferencia
from modules.pendencias_page import tela_pendencias

st.set_page_config(layout="wide")
st.markdown("""<style>
[data-testid="stSidebar] {
dispaly: none;
}</style>""", unsafe_allow_html=True)




# =========================
# SISTEMA
# =========================

st.title("📋 Sistema de Auditoria")

aba1, aba2 = st.tabs([
    "📋 Pendências",
    "📦 Conferência"
])

with aba1:
    tela_pendencias()

with aba2:
    tela_conferencia()