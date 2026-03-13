import streamlit as st
import pandas as pd
from database.supabase_db import(listar_pendencias,inserir_pendencia,excluir_pendencia,listar_produtos,finalizar_pendencia)
from utils.dados import BLOCOS, ERROS, TIPOS
from relatorios.relatorio_pendencias import (gerar_relatorio_imagem, gerar_relatorio_excel)


def tela_pendencias():
    dados = listar_pendencias()
    df = pd.DataFrame(dados)

    produtos = listar_produtos()
    df_prod = pd.DataFrame(produtos)
    
    lista_produtos = []

    if not df_prod.empty:
        lista_produtos = df_prod["nome_produto"].tolist()

    # =========================
    # FILTROS
    # =========================

    st.subheader("Filtros")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        filtro_bloco = st.selectbox(
            "Bloco",
            ["Todos"] + list(BLOCOS.keys())
        )

    with col2:

        lojas = []

        if filtro_bloco != "Todos":
            lojas = BLOCOS[filtro_bloco]

        filtro_loja = st.selectbox(
            "Loja",
            ["Todas"] + lojas
        )

    with col3:

        consultores = []

        if not df.empty:

            df_temp = df.copy()

            if filtro_bloco != "Todos":
                df_temp = df_temp[df_temp["bloco"] == filtro_bloco]

            if filtro_loja != "Todas":
                df_temp = df_temp[df_temp["loja"] == filtro_loja]

            consultores = sorted(df_temp["consultor"].dropna().unique())

        filtro_consultor = st.selectbox(
            "Consultor",
            ["Todos"] + consultores
        )

    with col4:

        filtro_status = st.selectbox(
            "Status",
            ["pendente", "finalizado","Todos"]
        )

    with col5:
        filtro_data_inicial = st.date_input(
            "Data Inicial",
            value=None,
            key="filtro_data_inicial"
        )
        filtro_data_final = st.date_input(
            "Data Final",
            value=None,
            key="filtro_data_final"
        )

    # =========================
    # APLICAR FILTROS
    # =========================

    df_f = df.copy()

    if not df_f.empty:
        

        if filtro_bloco != "Todos":
            df_f = df_f[df_f["bloco"] == filtro_bloco]

        if filtro_loja != "Todas":
            df_f = df_f[df_f["loja"] == filtro_loja]

        if filtro_consultor != "Todos":
            df_f = df_f[df_f["consultor"] == filtro_consultor]

        if filtro_status != "Todos":
            df_f = df_f[df_f["status"] == filtro_status]

        if filtro_data_inicial and filtro_data_final:
            df_f = df_f[
                (pd.to_datetime(df_f["data"]).dt.date >= filtro_data_inicial) &
                (pd.to_datetime(df_f["data"]).dt.date <= filtro_data_final)
            ]

    # =========================
    # TABELA
    # =========================

    st.subheader("Pendências")

    if not df_f.empty:
        df_f["data"] = pd.to_datetime(df_f["data"]).dt.strftime("%d/%m/%Y")

    selecionado = st.dataframe(
        df_f,
        use_container_width=True,
        on_select="rerun",
        selection_mode="single-row"
    )

    # =========================
    # EXCLUIR
    # =========================

    if selecionado.selection.rows:

        index = selecionado.selection.rows[0]

        id_pendencia = df_f.iloc[index]["id"]

        col1, col2 = st.columns(2)

        with col1:

            if st.button("🗑 Excluir pendência"):

                excluir_pendencia(id_pendencia)

                st.success("Excluído!")
                st.rerun()

        with col2:

            if st.button("✅ Finalizar pendência"):

                finalizar_pendencia(id_pendencia)

                st.success("Finalizado!")
                st.rerun()

    # =========================
    # BOTÃO CADASTRO
    # =========================
    st.divider()

    if "abrir_form" not in st.session_state:
        st.session_state["abrir_form"] = False

    if st.button("➕ Nova Pendência"):
        st.session_state["abrir_form"] = True


    # =========================
    # FORMULÁRIO
    # =========================

    if st.session_state["abrir_form"]:

        st.subheader("Cadastro de Pendência")

        if st.session_state.get("pendencia_salva"):
            st.success("✅ Pendência cadastrada com sucesso!")
            del st.session_state["pendencia_salva"]

        col1, col2 = st.columns(2)

        with col1:

            data_pendencia = st.date_input(
                "Data da Pendência",
                key="cadastro_data"
            )

            bloco = st.selectbox(
                "Bloco",
                list(BLOCOS.keys()),
                key="select_bloco"
            )

            lojas = BLOCOS.get(bloco, [])

            loja = st.selectbox(
                "Loja",
                lojas,
                key="select_loja"
            )

            produto = st.selectbox(
                "Produto",
                lista_produtos,
                key="select_produto"
            )

            erro = st.selectbox(
                "Erro",
                ERROS,
                key="select_erro"
            )

        with col2:

            tipo = st.selectbox(
                "Tipo",
                TIPOS,
                key="select_tipo"
            )

            valor = st.number_input(
                "Valor",
                step=1.0,
                key="input_valor"
            )

            controle_dav = st.text_input(
                "Controle DAV",
                key="input_controle_dav"
            )

            consultor = st.text_input(
                "Consultor",
                key="input_consultor"
            )

            observacao = st.text_area(
                "Observação",
                key="input_observacao"
            )

        if st.button("Salvar pendência"):

            dados = {
                "data": data_pendencia.strftime("%Y-%m-%d"),
                "bloco": bloco,
                "loja": loja,
                "produto": produto,
                "erro": erro,
                "tipo": tipo,
                "valor": valor,
                "controle_dav": controle_dav,
                "consultor": consultor,
                "observacao": observacao
            }

            inserir_pendencia(dados)

            st.session_state["pendencia_salva"] = True
            st.rerun()
            

    # =========================
    # RELATÓRIO WHATSAPP
    # =========================

    if st.button("📋 Relatório de Pendências"):
        if not df_f.empty:
            img = gerar_relatorio_imagem(df_f, filtro_consultor, filtro_loja, filtro_data_inicial, filtro_data_final)
            st.image(img, caption="📋 Relatório de Pendências")

    # =========================
    # EXCEL DESCONTOS
    # =========================

    if st.button("📊 Gerar Excel de Descontos"):
        if not df_f.empty:
            excel_buffer = gerar_relatorio_excel(
                df_f,
                filtro_data_inicial=filtro_data_inicial,
                filtro_data_final=filtro_data_final
            )

            st.download_button(
                label="⬇️ Baixar Relatório Excel",
                data=excel_buffer,
                file_name="desconto_auditoria.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:

            st.warning("Nenhuma pendência encontrada no período selecionado.")






