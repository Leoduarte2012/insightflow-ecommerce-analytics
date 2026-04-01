from sqlalchemy import create_engine
import pandas as pd

def load_db():
    engine = create_engine("sqlite:///ecommerce.db")

    df = pd.read_csv("data/processed/ecom_clean.csv")

    df.to_sql("vendas", engine, if_exists="replace", index=False)

    print("Dados carregados no banco!")

if __name__ == "__main__":
    load_db()