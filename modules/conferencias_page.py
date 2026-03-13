
import streamlit as st
import pandas as pd
from database.supabase_db import buscar_conferencia_filtrada, inserir_conferencia
from utils.dados import processar_planilha_conferencia
from relatorios.relatorio_conferencia import gerar_relatorio_conferencia_imagem


def tela_conferencia():

    st.subheader("📦 Conferência de Produtos")

    # =========================
    # BUSCAR DADOS DO BANCO
    # =========================

    dados_conf = buscar_conferencia_filtrada()
    df_conf = pd.DataFrame(dados_conf)

    colunas_esperadas = [
        "loja",
        "codigo",
        "produto",
        "quantidade",
        "status",
        "data_planilha",
        "valor",
        "total",
        "data_entrada"
    ]

    if df_conf.empty:
        df_conf = pd.DataFrame(columns=colunas_esperadas)
    else:
        for col in colunas_esperadas:
            if col not in df_conf.columns:
                df_conf[col] = None

        df_conf = df_conf[colunas_esperadas]

    # =========================
    # UPLOAD DA PLANILHA
    # =========================

    arquivo = st.file_uploader(
        "Enviar planilha de conferência",
        type=["xlsx"]
    )

    if arquivo:

        df_upload = processar_planilha_conferencia(arquivo)

        st.dataframe(
            df_upload[
                [
                    "loja",
                    "codigo",
                    "produto",
                    "quantidade",
                    "status",
                    "data_planilha",
                    "valor",
                    "total"
                ]
            ],
            use_container_width=True
        )

        if st.button("Salvar Conferência"):

            inserir_conferencia(df_upload.to_dict("records"))

            st.success("Conferência salva com sucesso!")

            st.rerun()

    # =========================
    # FILTROS DO RELATÓRIO
    # =========================

    st.divider()
    st.subheader("Filtros do Relatório")

    col1, col2, col3 = st.columns(3)

    with col1:

        lojas_conf = ["Todas"]

        if not df_conf.empty:
            lojas_conf += sorted(df_conf["loja"].dropna().unique().tolist())

        filtro_loja_conf = st.selectbox(
            "Loja",
            lojas_conf
        )

    with col2:

        filtro_data_inicio_conf = st.date_input(
            "Data inicial"
        )

    with col3:

        filtro_data_fim_conf = st.date_input(
            "Data final"
        )

    # =========================
    # FILTRAR DADOS
    # =========================

    df_relatorio = df_conf.copy()

    if not df_relatorio.empty:

        # converter data
        df_relatorio["data_entrada"] = pd.to_datetime(
            df_relatorio["data_entrada"], errors="coerce"
        )

        # filtro loja
        if filtro_loja_conf != "Todas":
            df_relatorio = df_relatorio[
                df_relatorio["loja"] == filtro_loja_conf
            ]

        # filtro data
        if filtro_data_inicio_conf and filtro_data_fim_conf:

            df_relatorio = df_relatorio[
                (df_relatorio["data_entrada"].dt.date >= filtro_data_inicio_conf) &
                (df_relatorio["data_entrada"].dt.date <= filtro_data_fim_conf)
            ]

    # =========================
    # VISUALIZAÇÃO DOS DADOS
    # =========================

    st.write("Dados carregados:")
    st.dataframe(df_relatorio, use_container_width=True)

    st.write("Quantidade de linhas:", len(df_relatorio))

    # =========================
    # GERAR RELATÓRIO
    # =========================

    if st.button("📋 Gerar Relatório Conferência"):

        if not df_relatorio.empty:

            img = gerar_relatorio_conferencia_imagem(
                df_relatorio,
                filtro_loja_conf
            )

            st.image(img)

        else:

            st.warning(
                "Nenhum dado encontrado para os filtros selecionados."
            )
