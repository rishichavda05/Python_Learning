# Hands-on Exercise 1: Transform Sales Dataset

## Goal

Practice basic data transformation using Pandas.

## Files

- `orders.csv` - Raw sales/order data
- `products.csv` - Product information
- `transform_sales.py` - Python transformation script

## Tasks

1. Load both CSV files.
2. Inspect the data.
3. Remove extra spaces from customer names.
4. Handle missing quantity values.
5. Remove duplicate orders.
6. Join orders with products using `product_id`.
7. Create `total_amount = quantity * unit_price`.
8. Calculate total sales by product.
9. Calculate total sales by category.
10. Save the final data as `transformed_sales.csv`.

## Run

Put all files in the same folder and run:

```bash
python transform_sales.py
```

## Expected Final Columns

```text
order_id
order_date
product_id
customer_name
quantity
product_name
category
unit_price
total_amount
```

## Concepts Practiced

- Data cleaning
- Null handling
- Duplicate removal
- Joins
- Aggregations
- Feature engineering
- Saving transformed data
