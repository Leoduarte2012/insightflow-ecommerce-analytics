import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

n = 6000

data = []

for i in range(n):
    data.append({
        "order_id": i,
        "customer_id": np.random.randint(1000, 2000),
        "product": fake.random_element(elements=("Notebook", "Mouse", "Teclado", "Monitor")),
        "price": round(np.random.uniform(10, 500), 2),
        "quantity": np.random.randint(1, 5),
        "date": fake.date_time_between(start_date='-1y', end_date='now')
    })

df = pd.DataFrame(data)

# Inserindo ERROS reais (simulação)
df.loc[10:20, "price"] = None
df.loc[30:35, "quantity"] = None
df = pd.concat([df, df.iloc[0:50]])  # duplicados

df.to_csv("data/raw/ecom_data.csv", index=False)

print("Dataset criado com sucesso!")