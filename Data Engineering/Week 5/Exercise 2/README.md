# Hands-on Exercise 2: Convert Pandas Logic into PySpark

## Goal

Convert the sales transformation logic from Exercise 1 (Pandas) into PySpark.

The business logic is the same. Only the processing framework changes.

---

## Input Files

- `orders.csv` - Raw order data
- `products.csv` - Product information

## Python File

- `transform_sales_pyspark.py` - PySpark transformation code

---

## Tasks

Implement the following transformations using PySpark:

1. Create a Spark session.
2. Read `orders.csv`.
3. Read `products.csv`.
4. Clean extra spaces from `customer_name`.
5. Handle missing `quantity`.
6. Remove duplicate orders.
7. Join orders with products using `product_id`.
8. Create `total_amount`.
9. Calculate total sales by product.
10. Calculate total sales by category.
11. Save the transformed data.

---

## Pandas vs PySpark

| Pandas | PySpark |
|---|---|
| `pd.read_csv()` | `spark.read.csv()` |
| `str.strip()` | `trim()` |
| `fillna()` | `fillna()` |
| `drop_duplicates()` | `dropDuplicates()` |
| `merge()` | `join()` |
| `df["a"] * df["b"]` | `col("a") * col("b")` |
| `groupby()` | `groupBy()` |
| `sum()` | `sum()` |
| `to_csv()` | `write.csv()` |

---

## How to Run

First install PySpark if you have not installed it:

```bash
pip install pyspark
```

Check the installation:

```bash
py -c "import pyspark; print(pyspark.__version__)"
```

Run the program:

```bash
py .\transform_sales_pyspark.py
```

---

## Expected Output

The program will display:

- Orders
- Products
- Transformed sales
- Total sales by product
- Total sales by category

It will also create:

```text
transformed_sales_pyspark/
```

This folder contains the Spark output files.

---

## Important Difference

In Pandas, this:

```python
sales.to_csv("transformed_sales.csv", index=False)
```

usually creates one CSV file.

In PySpark:

```python
sales.write.csv("transformed_sales_pyspark")
```

creates an **output folder** containing one or more part files.

This happens because Spark is designed for distributed processing.

---

## Learning Outcome

After completing this exercise, you should understand how common Pandas transformation operations are written in PySpark.

The main idea is:

```text
Pandas Logic
     |
     v
Understand the Transformation
     |
     v
Write the Same Logic in PySpark
```
