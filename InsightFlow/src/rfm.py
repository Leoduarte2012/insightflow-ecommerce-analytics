# ======================
# RFM ANALYSIS
# ======================
import streamlit as st
import pandas as pd
import os

# Obtém o caminho correto relativo ao arquivo atual
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "..", "data", "processed", "ecom_clean.csv")

df = pd.read_csv(data_path)

# Converte a coluna 'date' para datetime
df["date"] = pd.to_datetime(df["date"])

snapshot_date = df["date"].max()

rfm = df.groupby("customer_id").agg({
    "date": lambda x: (snapshot_date - x.max()).days,
    "order_id": "count",
    "total": "sum"
})

rfm.columns = ["recency", "frequency", "monetary"]

rfm["R_score"] = pd.qcut(rfm["recency"], 4, labels=[4,3,2,1])
rfm["F_score"] = pd.qcut(rfm["frequency"], 4, labels=[1,2,3,4])
rfm["M_score"] = pd.qcut(rfm["monetary"], 4, labels=[1,2,3,4])

rfm["RFM_score"] = (
    rfm["R_score"].astype(str) +
    rfm["F_score"].astype(str) +
    rfm["M_score"].astype(str)
)

def segment(row):
    if row["R_score"] == 4 and row["F_score"] >= 3:
        return "VIP 🟢"
    elif row["F_score"] >= 3:
        return "Leal 🟡"
    elif row["R_score"] == 1:
        return "Perdido 🔴"
    else:
        return "Regular 🔵"

rfm["segment"] = rfm.apply(segment, axis=1)

st.subheader("👥 Segmentação de Clientes (RFM)")

segment_count = rfm["segment"].value_counts()

st.bar_chart(segment_count)

st.subheader("💰 Receita por Segmento")

rfm["monetary"].groupby(rfm["segment"]).sum().sort_values().plot(kind="bar")
st.pyplot()

st.subheader("📋 Base de Clientes")

st.dataframe(rfm.sort_values("monetary", ascending=False).head(20))
