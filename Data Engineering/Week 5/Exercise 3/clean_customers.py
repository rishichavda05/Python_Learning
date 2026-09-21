import pandas as pd

# 1. Load the large customer dataset
df = pd.read_csv("messy_customers.csv")

print("Original shape:", df.shape)
print("\nMissing values:")
print(df.isnull().sum())
print("\nDuplicate rows:", df.duplicated().sum())

# 2. Clean column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# 3. Clean text columns
text_columns = ["customer_name", "email", "phone", "city", "state", "country", "segment"]

for column in text_columns:
    df[column] = df[column].astype("string").str.strip()

# 4. Standardize customer names
df["customer_name"] = df["customer_name"].str.title()

# 5. Standardize email
df["email"] = df["email"].str.lower()

# 6. Convert numeric columns
df["age"] = pd.to_numeric(df["age"], errors="coerce")
df["income"] = pd.to_numeric(df["income"], errors="coerce")

# 7. Handle invalid age values
df.loc[(df["age"] < 18) | (df["age"] > 100), "age"] = pd.NA

# 8. Handle invalid income values
df.loc[df["income"] <= 0, "income"] = pd.NA

# 9. Fill missing age with median
df["age"] = df["age"].fillna(df["age"].median())

# 10. Fill missing income with median
df["income"] = df["income"].fillna(df["income"].median())

# 11. Remove rows without essential customer information
df = df.dropna(subset=["customer_id", "customer_name"])

# 12. Remove duplicate customers
df = df.drop_duplicates(subset=["customer_id"])

# 13. Create a simple feature
df["income_category"] = pd.cut(
    df["income"],
    bins=[0, 30000, 75000, 150000, float("inf")],
    labels=["Low", "Medium", "High", "Very High"]
)

# 14. Save cleaned dataset
df.to_csv("cleaned_customers.csv", index=False)

print("\nCleaned shape:", df.shape)
print("\nSample cleaned data:")
print(df.head())

print("\nCleaning completed!")
print("Output: cleaned_customers.csv")
