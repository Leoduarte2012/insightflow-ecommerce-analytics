import pandas as pd
import matplotlib.pyplot as plt

def run_eda():
    df = pd.read_csv("data/processed/ecom_clean.csv")

    print(df.describe())

    receita = df.groupby("product")["total"].sum()

    receita.plot(kind="bar")
    plt.title("Receita por Produto")
    plt.show()

if __name__ == "__main__":
    run_eda()