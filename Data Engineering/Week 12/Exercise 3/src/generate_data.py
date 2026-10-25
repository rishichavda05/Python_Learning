import pandas as pd
import random
from datetime import datetime, timedelta


ROWS = 500_000


products = [
    "Laptop",
    "Mouse",
    "Keyboard",
    "Monitor",
    "Headphones"
]

customers = [
    "Alice",
    "Bob",
    "Charlie",
    "David",
    "Eva"
]


data = []

start_date = datetime(2025, 1, 1)


for i in range(ROWS):

    data.append({
        "order_id": i + 1,
        "customer": random.choice(customers),
        "product": random.choice(products),
        "quantity": random.randint(1, 10),
        "price": random.randint(10, 1000),
        "order_date": start_date + timedelta(
            days=random.randint(0, 365)
        )
    })


df = pd.DataFrame(data)

df.to_csv(
    "data/sales.csv",
    index=False
)

print(f"Generated {ROWS:,} records")