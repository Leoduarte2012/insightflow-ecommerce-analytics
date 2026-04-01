# 📊 InsightFlow - Data Analytics Project

## 🚀 Visão Geral

Projeto end-to-end de análise de dados simulando um e-commerce, cobrindo ETL, análise exploratória, SQL, dashboard e modelagem preditiva.

---

## 🧠 Objetivo

Transformar dados brutos em insights acionáveis para suporte à decisão de negócio.

---

## 🏗️ Arquitetura do Projeto

```
InsightFlow/
├── data/
├── src/
├── dashboard/
├── README.md
```

---

## 🔄 Pipeline de Dados

1. Geração de dados simulados
2. Limpeza e transformação (ETL)
3. Armazenamento em banco (SQLite)
4. Análise exploratória (EDA)
5. Segmentação de clientes (RFM)
6. Dashboard interativo
7. Previsão de receita (Machine Learning)

---

## 📊 Principais KPIs

* 💰 Faturamento Total
* 🛒 Ticket Médio
* 👥 Clientes Ativos
* 📦 Número de Pedidos

---

## 👥 Segmentação de Clientes (RFM)

Clientes classificados em:

* 🟢 VIP
* 🟡 Leais
* 🔵 Regulares
* 🔴 Perdidos

---

## 🤖 Modelagem Preditiva

Aplicação de Regressão Linear para previsão de receita ao longo do tempo.

---

## 💡 Principais Insights

* Crescimento consistente de receita
* Concentração de faturamento em clientes VIP
* Identificação de clientes com risco de churn
* Produtos com maior impacto no negócio

---

## 🛠️ Tecnologias Utilizadas

* Python
* Pandas, NumPy
* Scikit-learn
* Streamlit
* SQLite

---

## ▶️ Como Executar o Projeto

```bash
pip install -r requirements.txt
python src/generate_data.py
python src/etl.py
python src/db.py
streamlit run dashboard/app.py
```

---

## 📌 Autor

Leonardo Duarte
