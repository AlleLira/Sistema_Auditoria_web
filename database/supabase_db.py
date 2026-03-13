from config.supabase_client import supabase
import bcrypt
from datetime import datetime
import streamlit as st


# ======================
# PRODUTOS
# ======================

def listar_produtos():

    response = (
        supabase
        .table("produtos")
        .select("nome_produto")
        .execute()
    )

    return response.data


# =========================
# PENDENCIAS
# =========================

def listar_pendencias():

    response = (
        supabase
        .table("pendencias")
        .select("*")
        .execute()
    )

    return response.data


def inserir_pendencia(dados):

    try:

        dados["data_entrada"] = datetime.now().isoformat()

        # mostrar o que está sendo enviado
        st.write("Dados enviados:", dados)

        resposta = supabase.table("pendencias").insert(dados).execute()

        # mostrar resposta do banco
        st.write("Resposta do banco:", resposta)

        return True

    except Exception as e:

        st.error("Erro ao inserir no banco")
        st.write(e)

        return False


def excluir_pendencia(id):

    supabase.table("pendencias").delete().eq("id", id).execute()


def finalizar_pendencia(id):

    supabase.table("pendencias").update(
        {"status": "finalizado"}
    ).eq("id", id).execute()

# =========================
# CONFERENCIA
# =========================

def inserir_conferencia(dados):
    supabase.table("conferencia").insert(dados).execute()

def buscar_conferencia_filtrada(loja=None, data_inicio=None, data_fim=None):

    query = supabase.table("conferencia").select("*")

    if loja and loja != "Todas":
        query = query.eq("loja", loja)

    if data_inicio:
        query = query.gte("data_entrada", data_inicio)

    if data_fim:
        query = query.lte("data_entrada", data_fim)

    return query.order("data_entrada", desc=True).execute().data

# =========================
# USUARIOS
# =========================

def buscar_usuario(usuario):
    resp = supabase.table("usuarios").select("*").eq("usuario", usuario).execute()

    if resp.data:
        return resp.data[0]
    
    return None

def criar_senha(usuario, senha):

    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

    supabase.table("usuarios").update({
        "senha": senha_hash,
        "primeiro_login": False
    }).eq("usuario", usuario).execute()

def validar_login(usuario, senha):
    user = buscar_usuario(usuario)

    if not user:
        return False
    
    if user["primeiro_login"]:
        return "primeiro"
    
    if bcrypt.checkpw(senha.encode(), user["senha"].encode()):
        return True
    
    return False






