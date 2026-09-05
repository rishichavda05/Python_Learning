import pandas as pd

# 1. Load data
orders = pd.read_csv("orders.csv")
products = pd.read_csv("products.csv")

# 2. Inspect data
print("Orders:")
print(orders)
print("\nProducts:")
print(products)

# 3. Clean customer names
orders["customer_name"] = orders["customer_name"].str.strip()

# 4. Handle missing quantity
orders["quantity"] = orders["quantity"].fillna(1)

# 5. Remove duplicate orders
orders = orders.drop_duplicates()

# 6. Join orders with products
sales = orders.merge(
    products,
    on="product_id",
    how="left"
)

# 7. Create total_amount
sales["total_amount"] = sales["quantity"] * sales["unit_price"]

# 8. Total sales by product
product_sales = (
    sales.groupby(["product_id", "product_name"])["total_amount"]
    .sum()
    .reset_index()
)

print("\nTotal Sales by Product:")
print(product_sales)

# 9. Total sales by category
category_sales = (
    sales.groupby("category")["total_amount"]
    .sum()
    .reset_index()
)

print("\nTotal Sales by Category:")
print(category_sales)

# 10. Save transformed data
sales.to_csv("transformed_sales.csv", index=False)

print("\nTransformation completed!")
print("File created: transformed_sales.csv")
