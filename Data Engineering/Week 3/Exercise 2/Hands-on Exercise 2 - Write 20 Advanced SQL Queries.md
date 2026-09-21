# Hands-on Exercise 2: Write 20 Advanced SQL Queries

## Goal

Practice advanced SQL concepts using the **Sales Warehouse** created in Exercise 1.

### Tables Used

```text
dim_customer
dim_product
dim_date
dim_store
fact_sales
```

The queries cover:

- JOINs
- GROUP BY
- HAVING
- Aggregate Functions
- Window Functions
- CTEs
- Subqueries
- CASE
- Ranking
- Running Totals
- Date-based analysis

---

## 1. Get Customer and Total Sales

Find how much each customer has spent.

```sql
SELECT
    c.customer_name,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
GROUP BY c.customer_name;
```

---

## 2. Find the Highest-Selling Product

```sql
SELECT
    p.product_name,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_product p
    ON f.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_sales DESC
LIMIT 1;
```

---

## 3. Find Sales by Category

```sql
SELECT
    p.category,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_product p
    ON f.product_id = p.product_id
GROUP BY p.category;
```

---

## 4. Find Customers Who Spent More Than 5,000

```sql
SELECT
    c.customer_name,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
GROUP BY c.customer_name
HAVING SUM(f.sales_amount) > 5000;
```

`HAVING` is used to filter grouped results.

---

## 5. Find Sales by Store

```sql
SELECT
    s.store_name,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_store s
    ON f.store_id = s.store_id
GROUP BY s.store_name;
```

---

## 6. Find Average Sale Amount

```sql
SELECT
    AVG(sales_amount) AS average_sales
FROM fact_sales;
```

---

## 7. Find the Largest Single Sale

```sql
SELECT
    MAX(sales_amount) AS highest_sale
FROM fact_sales;
```

---

## 8. Rank Products by Sales

```sql
SELECT
    p.product_name,
    SUM(f.sales_amount) AS total_sales,
    RANK() OVER (
        ORDER BY SUM(f.sales_amount) DESC
    ) AS sales_rank
FROM fact_sales f
JOIN dim_product p
    ON f.product_id = p.product_id
GROUP BY p.product_name;
```

`RANK()` assigns a ranking based on total sales.

---

## 9. Rank Customers by Spending

```sql
SELECT
    c.customer_name,
    SUM(f.sales_amount) AS total_sales,
    RANK() OVER (
        ORDER BY SUM(f.sales_amount) DESC
    ) AS customer_rank
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
GROUP BY c.customer_name;
```

---

## 10. Find the Top 2 Products

```sql
SELECT
    p.product_name,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_product p
    ON f.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_sales DESC
LIMIT 2;
```

---

## 11. Classify Sales Using CASE

```sql
SELECT
    sale_id,
    sales_amount,
    CASE
        WHEN sales_amount >= 10000 THEN 'High'
        WHEN sales_amount >= 5000 THEN 'Medium'
        ELSE 'Low'
    END AS sales_category
FROM fact_sales;
```

`CASE` is used to create conditional logic in SQL.

---

## 12. Find Sales by Year

```sql
SELECT
    d.year,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_date d
    ON f.date_id = d.date_id
GROUP BY d.year;
```

---

## 13. Find Sales by Month

```sql
SELECT
    d.year,
    d.month,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_date d
    ON f.date_id = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;
```

---

## 14. Find High-Value Customers Using a CTE

```sql
WITH customer_sales AS (
    SELECT
        customer_id,
        SUM(sales_amount) AS total_sales
    FROM fact_sales
    GROUP BY customer_id
)
SELECT
    c.customer_name,
    cs.total_sales
FROM customer_sales cs
JOIN dim_customer c
    ON cs.customer_id = c.customer_id
WHERE cs.total_sales > 5000;
```

The CTE first calculates sales for each customer. The main query then filters customers with sales greater than 5,000.

---

## 15. Find the Most Expensive Product

```sql
SELECT
    product_name,
    price
FROM dim_product
WHERE price = (
    SELECT MAX(price)
    FROM dim_product
);
```

This query uses a **subquery** to find the maximum product price.

---

## 16. Find Total Quantity Sold by Product

```sql
SELECT
    p.product_name,
    SUM(f.quantity) AS total_quantity
FROM fact_sales f
JOIN dim_product p
    ON f.product_id = p.product_id
GROUP BY p.product_name;
```

---

## 17. Find Customers Who Purchased a Laptop

```sql
SELECT DISTINCT
    c.customer_name
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
JOIN dim_product p
    ON f.product_id = p.product_id
WHERE p.product_name = 'Laptop';
```

`DISTINCT` prevents the same customer from appearing multiple times.

---

## 18. Find Product Sales Percentage

Calculate how much each product contributes to total sales.

```sql
SELECT
    p.product_name,
    SUM(f.sales_amount) AS product_sales,
    ROUND(
        SUM(f.sales_amount) * 100.0 /
        SUM(SUM(f.sales_amount)) OVER (),
        2
    ) AS sales_percentage
FROM fact_sales f
JOIN dim_product p
    ON f.product_id = p.product_id
GROUP BY p.product_name;
```

The window function calculates the overall sales total and helps calculate each product's percentage.

---

## 19. Find Previous Sale Using LAG

```sql
SELECT
    sale_id,
    sales_amount,
    LAG(sales_amount) OVER (
        ORDER BY sale_id
    ) AS previous_sale
FROM fact_sales;
```

`LAG()` returns the value from the previous row.

This is useful when comparing current and previous records.

---

## 20. Calculate Running Total of Sales

```sql
SELECT
    sale_id,
    sales_amount,
    SUM(sales_amount) OVER (
        ORDER BY sale_id
    ) AS running_total
FROM fact_sales;
```

A running total continuously adds each sale to the previous total.

Example:

```text
Sale 1 → 60000
Sale 2 → 62000
Sale 3 → 67000
Sale 4 → 70000
```

---

# Concepts Practiced

| Query | Concept |
|---|---|
| 1–5 | JOIN + GROUP BY |
| 6–7 | Aggregate Functions |
| 8–9 | Window Functions |
| 10 | ORDER BY + LIMIT |
| 11 | CASE |
| 12–13 | Date Analysis |
| 14 | CTE |
| 15 | Subquery |
| 16–17 | JOIN + Filtering |
| 18 | Window Function |
| 19 | LAG |
| 20 | Running Total |

---

# Result

After completing this exercise, you will have practiced advanced SQL using a small **Sales Data Warehouse** and worked with the most important SQL techniques used in Data Engineering.