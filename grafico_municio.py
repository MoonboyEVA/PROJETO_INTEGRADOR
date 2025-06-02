import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Sorotipagem", layout="wide")

# Carregar os dados
@st.cache_data
def carregar_dados():
    try:
        df = pd.read_csv("Dengue.csv", encoding='latin1') 
        df['prop_sorotipagem'] = df['casos_sorotipados'] / df['total_casos']
        return df
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame()

df = carregar_dados()
st.title("📊 Dashboard de Sorotipagem por Município")

df['prop_sorotipagem'] = df['prop_sorotipagem'].apply(lambda x: f"{x:.2%}")

# Filtro de busca por município
st.sidebar.header("🔍 Busca por Município")
busca = st.sidebar.text_input("Digite o nome do município").strip().lower()

if busca:
    df_filtrado = df[df['name_muni'].str.lower().str.contains(busca)]
    st.subheader(f"Resultados para: {busca.title()}")
    st.dataframe(df_filtrado)
else:
    st.subheader("📋 Tabela Completa")
    st.dataframe(df)

# Sessão de comparação entre municípios
st.markdown("---")
st.header("📌 Comparação entre Municípios")

cidades_selecionadas = st.multiselect(
    "Selecione os municípios para comparar",
    options=df['name_muni'].unique(),
    default=df['name_muni'].unique()[:2]
)

if cidades_selecionadas:
    df_comparacao = df[df['name_muni'].isin(cidades_selecionadas)]

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.bar(
            df_comparacao,
            x="name_muni",
            y="total_casos",
            title="Total de Casos",
            labels={"name_muni": "Município", "total_casos": "Casos"},
            text_auto=True
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.bar(
            df_comparacao,
            x="name_muni",
            y="prop_sorotipagem",
            title="Proporção de Sorotipagem",
            labels={"name_muni": "Município", "prop_sorotipagem": "Proporção"},
            text_auto=True
        )
        st.plotly_chart(fig2, use_container_width=True)
