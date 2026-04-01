import pandas as pd

def run_etl():
    df = pd.read_csv("data/raw/ecom_data.csv")

    print("Antes:", df.shape)

    # remover duplicados
    df = df.drop_duplicates()

    # remover linhas totalmente vazias
    df = df.dropna(how="all")

    # tratar tipos
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    # preencher nulos
    df["price"] = df["price"].fillna(df["price"].mean())
    df["quantity"] = df["quantity"].fillna(1)

    # datas
    df["date"] = pd.to_datetime(df["date"])

    # criar coluna total
    df["total"] = df["price"] * df["quantity"]

    print("Depois:", df.shape)

    df.to_csv("data/processed/ecom_clean.csv", index=False)

if __name__ == "__main__":
    run_etl()