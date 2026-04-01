import streamlit as st
import pandas as pd
import os
import plotly.express as px

# ======================
# CONFIG
# ======================
st.set_page_config(layout="wide")

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "..", "data", "processed", "ecom_clean.csv")

    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])

    return df

df = load_data()

# ======================
# SIDEBAR (FILTROS)
# ======================
st.sidebar.title("Filtros")

data_min = df["date"].min()
data_max = df["date"].max()

data_range = st.sidebar.date_input("Período", [data_min, data_max])

produto = st.sidebar.multiselect(
    "Produto",
    options=df["product"].unique(),
    default=df["product"].unique()
)

# ======================
# FILTRO
# ======================
if len(data_range) == 2:
    data_inicio, data_fim = data_range
else:
    data_inicio, data_fim = data_min, data_max

df = df[
    (df["date"] >= pd.to_datetime(data_inicio)) &
    (df["date"] <= pd.to_datetime(data_fim)) &
    (df["product"].isin(produto))
]

if df.empty:
    st.warning("Nenhum dado encontrado com os filtros selecionados.")
    st.stop()

# ======================
# KPIs
# ======================
faturamento = df["total"].sum()

ticket_medio = (
    df.groupby("order_id")["total"]
    .sum()
    .mean()
)

pedidos = df["order_id"].nunique()
clientes = df["customer_id"].nunique()

def format_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.title("📊 InsightFlow - Dashboard Executivo")

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Faturamento", format_brl(faturamento))
col2.metric("🛒 Ticket Médio", format_brl(ticket_medio))
col3.metric("📦 Pedidos", pedidos)
col4.metric("👥 Clientes", clientes)

st.divider()

# ======================
# GRÁFICO TEMPORAL
# ======================
st.subheader("📈 Receita ao longo do tempo")

df_time = (
    df.groupby(pd.Grouper(key="date", freq="D"))["total"]
    .sum()
    .reset_index()
)

fig_time = px.line(df_time, x="date", y="total", title="Receita diária")
st.plotly_chart(fig_time, width='stretch')

# ======================
# PRODUTOS E CLIENTES
# ======================
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Receita por Produto")

    prod = (
        df.groupby("product")["total"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig_prod = px.bar(prod, x="product", y="total")
    st.plotly_chart(fig_prod, width='stretch')

with col2:
    st.subheader("🔥 Top Clientes")

    top_clientes = (
        df.groupby("customer_id")["total"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_cli = px.bar(top_clientes, x="customer_id", y="total")
    st.plotly_chart(fig_cli, width='stretch')

# ======================
# RFM (AQUI É O BLOCO NOVO)
# ======================
st.divider()
st.subheader("👥 Segmentação de Clientes (RFM)")

snapshot_date = df["date"].max()

rfm = df.groupby("customer_id").agg({
    "date": lambda x: (snapshot_date - x.max()).days,
    "order_id": "nunique",
    "total": "sum"
})

rfm.columns = ["recencia", "frequencia", "monetario"]

# Score
rfm["R_score"] = pd.qcut(rfm["recencia"], 5, labels=[5,4,3,2,1])
rfm["F_score"] = pd.qcut(rfm["frequencia"].rank(method="first"), 5, labels=[1,2,3,4,5])
rfm["M_score"] = pd.qcut(rfm["monetario"], 5, labels=[1,2,3,4,5])

rfm["RFM_score"] = (
    rfm["R_score"].astype(str) +
    rfm["F_score"].astype(str) +
    rfm["M_score"].astype(str)
)

# Segmentação
def segmentar(row):
    if row["R_score"] == 5 and row["F_score"] == 5:
        return "VIP"
    elif row["F_score"] >= 4:
        return "Leal"
    elif row["R_score"] <= 2:
        return "Em risco"
    else:
        return "Regular"

rfm["segmento"] = rfm.apply(segmentar, axis=1)

# ======================
# GRÁFICO RFM
# ======================
seg = rfm["segmento"].value_counts().reset_index()
seg.columns = ["segmento", "quantidade"]

fig_rfm = px.pie(seg, names="segmento", values="quantidade")
st.plotly_chart(fig_rfm, use_container_width=True)

# ======================
# TOP VIP
# ======================
st.subheader("🏆 Clientes VIP")

vip = (
    rfm[rfm["segmento"] == "VIP"]
    .sort_values("monetario", ascending=False)
    .head(10)
)

st.dataframe(vip)

# ======================
# INSIGHTS
# ======================
st.divider()
st.subheader("🧠 Insights Automáticos")

top_produto = prod.iloc[0]["product"]

crescimento = (
    df_time["total"]
    .pct_change()
    .dropna()
    .mean()
)

total_clientes = len(rfm)

vip_pct = (rfm[rfm["segmento"] == "VIP"].shape[0] / total_clientes)
risco_pct = (rfm[rfm["segmento"] == "Em risco"].shape[0] / total_clientes)

st.write(f"📌 Produto mais lucrativo: **{top_produto}**")
st.write(f"📊 Crescimento médio diário: **{crescimento:.2%}**")
st.write(f"🏆 % Clientes VIP: **{vip_pct:.2%}**")
st.write(f"⚠️ % Clientes em risco: **{risco_pct:.2%}**")

# ======================
# DOWNLOAD
# ======================
st.divider()

st.download_button(
    "📥 Baixar dados filtrados",
    df.to_csv(index=False),
    file_name="dados_filtrados.csv",
    mime="text/csv"
)

from sklearn.linear_model import LinearRegression
import numpy as np

# ======================
# FORECAST
# ======================

df_time = df.groupby("date")["total"].sum().reset_index()
df_time = df_time.sort_values("date")
df_time["t"] = np.arange(len(df_time))

model = LinearRegression()
model.fit(df_time[["t"]], df_time["total"])

df_time["forecast"] = model.predict(df_time[["t"]])

st.subheader("📈 Previsão de Receita")

st.line_chart(df_time.set_index("date")[["total", "forecast"]])