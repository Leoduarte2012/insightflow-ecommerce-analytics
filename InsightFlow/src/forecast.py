import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

def run_forecast():
    df = pd.read_csv("data/processed/ecom_clean.csv")
    df["date"] = pd.to_datetime(df["date"])

    # Agrupar por dia
    df_time = df.groupby("date")["total"].sum().reset_index()

    # Criar variável temporal
    df_time = df_time.sort_values("date")
    df_time["t"] = np.arange(len(df_time))

    # Modelo
    X = df_time[["t"]]
    y = df_time["total"]

    model = LinearRegression()
    model.fit(X, y)

    # Previsão futura (próximos 30 dias)
    future = pd.DataFrame({
        "t": np.arange(len(df_time), len(df_time) + 30)
    })

    future["forecast"] = model.predict(future)

    # Juntar histórico + previsão
    df_time["forecast"] = model.predict(X)

    # Plot
    plt.figure()
    plt.plot(df_time["date"], df_time["total"], label="Real")
    plt.plot(df_time["date"], df_time["forecast"], label="Tendência")
    plt.legend()
    plt.title("Previsão de Receita")
    plt.show()

    return df_time, future

if __name__ == "__main__":
    run_forecast()