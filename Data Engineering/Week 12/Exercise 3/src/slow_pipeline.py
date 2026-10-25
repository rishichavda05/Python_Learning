import pandas as pd
import time


start_time = time.time()


# Read complete dataset
df = pd.read_csv("data/sales.csv")


# Calculate total using a Python loop
totals = []

for _, row in df.iterrows():

    total = row["quantity"] * row["price"]

    totals.append(total)


df["total_amount"] = totals


# Keep high-value orders
df = df[df["total_amount"] > 500]


# Save output
df.to_csv(
    "output/slow_output.csv",
    index=False
)


end_time = time.time()


print(
    f"Slow pipeline completed in "
    f"{end_time - start_time:.2f} seconds"
)