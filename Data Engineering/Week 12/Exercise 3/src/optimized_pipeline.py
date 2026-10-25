import pandas as pd
import time


start_time = time.time()


# Read only required columns
df = pd.read_csv(
    "data/sales.csv",
    usecols=[
        "order_id",
        "quantity",
        "price"
    ]
)


# Vectorized calculation
df["total_amount"] = (
    df["quantity"] * df["price"]
)


# Filter high-value orders
df = df[df["total_amount"] > 500]


# Save output
df.to_csv(
    "output/optimized_output.csv",
    index=False
)


end_time = time.time()


print(
    f"Optimized pipeline completed in "
    f"{end_time - start_time:.2f} seconds"
)