from database.supabase_db import validar_login, criar_senha
import streamlit as st

# sessão
if "logado" not in st.session_state:
    st.session_state["logado"] = False


# =========================
# PRIMEIRO LOGIN
# =========================

if "primeiro_login" in st.session_state:

    st.title("🔑 Primeiro acesso")

    nova_senha = st.text_input("Criar senha", type="password")
    confirmar = st.text_input("Confirmar senha", type="password")

    if st.button("Salvar senha"):

        if nova_senha != confirmar:
            st.error("As senhas não coincidem")

        else:
            criar_senha(st.session_state["primeiro_login"], nova_senha)

            st.success("Senha criada com sucesso!")

            del st.session_state["primeiro_login"]

            st.rerun()

    st.stop()


# =========================
# LOGIN
# =========================

if not st.session_state["logado"]:

    st.title("🔐 Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        resultado = validar_login(usuario, senha)

        if resultado == True:

            st.session_state["logado"] = True
            st.session_state["usuario"] = usuario
            st.rerun()

        elif resultado == "primeiro":

            st.session_state["primeiro_login"] = usuario
            st.rerun()

        else:

            st.error("Usuário ou senha inválidos")

    st.stop()