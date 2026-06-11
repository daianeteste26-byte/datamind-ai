import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from fpdf import FPDF

# ========================================
# CONFIGURAÇÃO DA PÁGINA
# ========================================
st.set_page_config(
    page_title="DataMind AI - Análise de Excel",
    page_icon="📊",
    layout="wide"
)

st.title("📊 DataMind AI")
st.markdown("### Análise inteligente de planilhas Excel 🚀")
st.markdown("---")

# ========================================
# UPLOAD DO ARQUIVO
# ========================================
st.sidebar.header("📤 Upload do Arquivo")
arquivo = st.sidebar.file_uploader(
    "Escolha um arquivo Excel",
    type=["xlsx", "xls"]
)

if arquivo is not None:
    # Lê o arquivo Excel
    try:
        xls = pd.ExcelFile(arquivo)
        aba = st.sidebar.selectbox("📑 Selecione a aba:", xls.sheet_names)
        df = pd.read_excel(arquivo, sheet_name=aba)
    except Exception as e:
        st.error(f"❌ Erro ao ler o arquivo: {e}")
        st.stop()

    # ========================================
    # ABAS DE FUNCIONALIDADES
    # ========================================
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 Resumo Geral",
        "📈 Estatísticas",
        "🔍 Filtros",
        "🧹 Limpeza",
        "📊 Gráficos",
        "💾 Exportar"
    ])

    # ----------------------------------------
    # ABA 1: RESUMO GERAL
    # ----------------------------------------
    with tab1:
        st.subheader("📋 Resumo Geral da Planilha")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📏 Linhas", df.shape[0])
        col2.metric("📐 Colunas", df.shape[1])
        col3.metric("❓ Valores Vazios", int(df.isna().sum().sum()))
        col4.metric("🔁 Duplicados", int(df.duplicated().sum()))

        st.markdown("### 👀 Pré-visualização dos Dados")
        st.dataframe(df.head(10), use_container_width=True)

        st.markdown("### 🧬 Tipos de Dados")
        tipos = pd.DataFrame({
            "Coluna": df.columns,
            "Tipo": df.dtypes.astype(str).values,
            "Valores Únicos": [df[c].nunique() for c in df.columns],
            "Valores Vazios": [df[c].isna().sum() for c in df.columns]
        })
        st.dataframe(tipos, use_container_width=True)

    # ----------------------------------------
    # ABA 2: ESTATÍSTICAS
    # ----------------------------------------
    with tab2:
        st.subheader("📈 Estatísticas Básicas")

        colunas_numericas = df.select_dtypes(include="number").columns.tolist()

        if colunas_numericas:
            st.markdown("### 📊 Estatísticas das Colunas Numéricas")
            st.dataframe(df[colunas_numericas].describe(), use_container_width=True)

            st.markdown("### 🎯 Análise Individual por Coluna")
            coluna = st.selectbox("Escolha uma coluna:", colunas_numericas)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Soma", f"{df[coluna].sum():,.2f}")
            c2.metric("Média", f"{df[coluna].mean():,.2f}")
            c3.metric("Máximo", f"{df[coluna].max():,.2f}")
            c4.metric("Mínimo", f"{df[coluna].min():,.2f}")
        else:
            st.warning("⚠️ Não há colunas numéricas nesta planilha.")

    # ----------------------------------------
    # ABA 3: FILTROS E BUSCAS
    # ----------------------------------------
    with tab3:
        st.subheader("🔍 Filtros e Buscas")

        col_filtro = st.selectbox("Filtrar pela coluna:", df.columns)
        busca = st.text_input("🔎 Digite o valor para buscar:")

        if busca:
            df_filtrado = df[df[col_filtro].astype(str).str.contains(busca, case=False, na=False)]
            st.success(f"✅ {len(df_filtrado)} resultado(s) encontrado(s)")
            st.dataframe(df_filtrado, use_container_width=True)
        else:
            st.info("💡 Digite algo no campo acima para filtrar")
            st.dataframe(df, use_container_width=True)

    # ----------------------------------------
    # ABA 4: LIMPEZA DE DADOS
    # ----------------------------------------
    with tab4:
        st.subheader("🧹 Limpeza de Dados")

        st.markdown("### Selecione as opções de limpeza:")
        rem_dup = st.checkbox("🔁 Remover linhas duplicadas")
        rem_vazios = st.checkbox("❓ Remover linhas com valores vazios")
        preencher = st.checkbox("✏️ Preencher valores vazios com 0 (numéricos)")

        df_limpo = df.copy()

        if rem_dup:
            df_limpo = df_limpo.drop_duplicates()
        if rem_vazios:
            df_limpo = df_limpo.dropna()
        if preencher:
            for col in df_limpo.select_dtypes(include="number").columns:
                df_limpo[col] = df_limpo[col].fillna(0)

        st.markdown(f"### 📊 Resultado: {len(df_limpo)} linhas (antes: {len(df)})")
        st.dataframe(df_limpo, use_container_width=True)

        # Salva o df limpo na sessão para exportar
        st.session_state["df_limpo"] = df_limpo

    # ----------------------------------------
    # ABA 5: GRÁFICOS
    # ----------------------------------------
    with tab5:
        st.subheader("📊 Gráficos Automáticos")

        tipo_grafico = st.selectbox(
            "Tipo de gráfico:",
            ["Barras", "Linhas", "Pizza", "Dispersão"]
        )

        col_x = st.selectbox("Eixo X:", df.columns)
        col_y = st.selectbox("Eixo Y:", df.select_dtypes(include="number").columns)

        try:
            if tipo_grafico == "Barras":
                fig = px.bar(df, x=col_x, y=col_y, title=f"{col_y} por {col_x}")
            elif tipo_grafico == "Linhas":
                fig = px.line(df, x=col_x, y=col_y, title=f"{col_y} por {col_x}")
            elif tipo_grafico == "Pizza":
                fig = px.pie(df, names=col_x, values=col_y, title=f"{col_y} por {col_x}")
            else:
                fig = px.scatter(df, x=col_x, y=col_y, title=f"{col_y} vs {col_x}")

            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Não foi possível gerar o gráfico: {e}")

    # ----------------------------------------
    # ABA 6: EXPORTAR
    # ----------------------------------------
    with tab6:
        st.subheader("💾 Exportar Resultados")

        df_exportar = st.session_state.get("df_limpo", df)

        col1, col2 = st.columns(2)

        # Exportar Excel
        with col1:
            st.markdown("### 📊 Exportar como Excel")
            buffer_excel = BytesIO()
            with pd.ExcelWriter(buffer_excel, engine="xlsxwriter") as writer:
                df_exportar.to_excel(writer, index=False, sheet_name="Dados")
            st.download_button(
                label="⬇️ Baixar Excel",
                data=buffer_excel.getvalue(),
                file_name="dados_analisados.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # Exportar PDF
        with col2:
            st.markdown("### 📄 Exportar Resumo em PDF")
            if st.button("📄 Gerar PDF"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.cell(0, 10, "Relatorio - DataMind AI", ln=True, align="C")
                pdf.ln(10)

                pdf.set_font("Arial", "", 12)
                pdf.cell(0, 8, f"Total de linhas: {df.shape[0]}", ln=True)
                pdf.cell(0, 8, f"Total de colunas: {df.shape[1]}", ln=True)
                pdf.cell(0, 8, f"Valores vazios: {int(df.isna().sum().sum())}", ln=True)
                pdf.cell(0, 8, f"Duplicados: {int(df.duplicated().sum())}", ln=True)
                pdf.ln(5)

                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 8, "Colunas:", ln=True)
                pdf.set_font("Arial", "", 10)
                for col in df.columns:
                    pdf.cell(0, 6, f"- {col} ({df[col].dtype})", ln=True)

                buffer_pdf = BytesIO()
                pdf_bytes = pdf.output(dest="S").encode("latin-1")
                buffer_pdf.write(pdf_bytes)

                st.download_button(
                    label="⬇️ Baixar PDF",
                    data=buffer_pdf.getvalue(),
                    file_name="relatorio.pdf",
                    mime="application/pdf"
                )

else:
    st.info("👈 Faça upload de um arquivo Excel na barra lateral para começar!")
    st.markdown("""
    ### 🎯 O que você pode fazer aqui:
    - 📋 Ver um **resumo geral** da planilha
    - 📈 Calcular **estatísticas** automáticas
    - 🔍 **Filtrar e buscar** dados
    - 🧹 **Limpar** dados (duplicados, vazios)
    - 📊 Gerar **gráficos** interativos
    - 💾 **Exportar** para Excel ou PDF
    """)
