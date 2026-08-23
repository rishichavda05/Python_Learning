# Hands-on Exercise 3: Create Star Schema from an OLTP Database

## Goal

Create a simple OLTP database and transform it into a **Star Schema** for analytics.

The complete flow is:

```text
OLTP Database
      ↓
Transform Data
      ↓
Star Schema
      ↓
Analytics Queries
```

We will use **one PostgreSQL database** so that the OLTP and warehouse tables can be used together.

---

# 1. Create Database

Create the database:

```sql
CREATE DATABASE sales_project;
```

In pgAdmin, connect to the `sales_project` database before running the remaining queries.

---

# 2. Create OLTP Tables

The OLTP system stores transactional data.

### Customers

```sql
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(100)
);
```

### Categories

```sql
CREATE TABLE categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(100)
);
```

### Products

```sql
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category_id INT,
    price DECIMAL(10,2),

    FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
);
```

### Stores

```sql
CREATE TABLE stores (
    store_id INT PRIMARY KEY,
    store_name VARCHAR(100),
    city VARCHAR(100)
);
```

### Orders

```sql
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    store_id INT,
    order_date DATE,

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    FOREIGN KEY (store_id)
        REFERENCES stores(store_id)
);
```

### Order Items

```sql
CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);
```

---

# 3. Insert OLTP Sample Data

### Customers

```sql
INSERT INTO customers VALUES
(1, 'Rahul', 'Ahmedabad', 'India'),
(2, 'Priya', 'Mumbai', 'India'),
(3, 'Amit', 'Delhi', 'India'),
(4, 'Neha', 'Pune', 'India');
```

### Categories

```sql
INSERT INTO categories VALUES
(1, 'Electronics'),
(2, 'Furniture'),
(3, 'Accessories');
```

### Products

```sql
INSERT INTO products VALUES
(1, 'Laptop', 1, 60000),
(2, 'Mobile', 1, 30000),
(3, 'Chair', 2, 5000),
(4, 'Mouse', 3, 1000),
(5, 'Keyboard', 3, 2000);
```

### Stores

```sql
INSERT INTO stores VALUES
(1, 'Ahmedabad Store', 'Ahmedabad'),
(2, 'Mumbai Store', 'Mumbai'),
(3, 'Delhi Store', 'Delhi');
```

### Orders

```sql
INSERT INTO orders VALUES
(101, 1, 1, '2026-01-10'),
(102, 2, 2, '2026-01-15'),
(103, 3, 3, '2026-02-05'),
(104, 1, 1, '2026-02-10'),
(105, 4, 2, '2026-02-15');
```

### Order Items

```sql
INSERT INTO order_items VALUES
(1, 101, 1, 1, 60000),
(2, 101, 4, 2, 1000),
(3, 102, 2, 1, 30000),
(4, 102, 5, 1, 2000),
(5, 103, 3, 2, 5000),
(6, 104, 4, 3, 1000),
(7, 105, 1, 1, 60000);
```

---

# 4. OLTP Structure

The original transactional database looks like this:

```text
customers
    |
    ↓
orders
    |
    ↓
order_items
    |
    ↓
products
    |
    ↓
categories

stores → orders
```

This structure is designed for transactional operations such as creating and updating orders.

---

# 5. Create Star Schema

The warehouse will contain:

```text
              dim_customer
                   |
                   |
dim_product -- fact_sales -- dim_store
                   |
                   |
                dim_date
```

There is one central fact table and multiple dimension tables.

---

# 6. Create Dimension Tables

### Customer Dimension

```sql
CREATE TABLE dim_customer (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(100)
);
```

### Product Dimension

Category information is combined with the product dimension.

```sql
CREATE TABLE dim_product (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category_name VARCHAR(100),
    price DECIMAL(10,2)
);
```

### Store Dimension

```sql
CREATE TABLE dim_store (
    store_id INT PRIMARY KEY,
    store_name VARCHAR(100),
    city VARCHAR(100)
);
```

### Date Dimension

```sql
CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    full_date DATE,
    day INT,
    month INT,
    year INT
);
```

---

# 7. Define Fact Table Grain

Before creating the fact table, define its grain.

> **One row in `fact_sales` represents one product sold in one order.**

The grain tells us exactly what each row represents.

---

# 8. Create Fact Table

```sql
CREATE TABLE fact_sales (
    sales_id INT PRIMARY KEY,
    order_id INT,
    customer_id INT,
    product_id INT,
    store_id INT,
    date_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    sales_amount DECIMAL(10,2),

    FOREIGN KEY (customer_id)
        REFERENCES dim_customer(customer_id),

    FOREIGN KEY (product_id)
        REFERENCES dim_product(product_id),

    FOREIGN KEY (store_id)
        REFERENCES dim_store(store_id),

    FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id)
);
```

---

# 9. Load Dimension Data

## Customer Dimension

```sql
INSERT INTO dim_customer
SELECT
    customer_id,
    customer_name,
    city,
    country
FROM customers;
```

## Product Dimension

Here we combine product and category information.

```sql
INSERT INTO dim_product
SELECT
    p.product_id,
    p.product_name,
    c.category_name,
    p.price
FROM products p
JOIN categories c
    ON p.category_id = c.category_id;
```

## Store Dimension

```sql
INSERT INTO dim_store
SELECT
    store_id,
    store_name,
    city
FROM stores;
```

## Date Dimension

Get unique order dates from the OLTP database.

```sql
INSERT INTO dim_date
SELECT
    ROW_NUMBER() OVER (ORDER BY order_date) AS date_id,
    order_date AS full_date,
    EXTRACT(DAY FROM order_date)::INT AS day,
    EXTRACT(MONTH FROM order_date)::INT AS month,
    EXTRACT(YEAR FROM order_date)::INT AS year
FROM (
    SELECT DISTINCT order_date
    FROM orders
) d;
```

Check the data:

```sql
SELECT *
FROM dim_date
ORDER BY full_date;
```

---

# 10. Load Fact Table

Now combine the OLTP `orders` and `order_items` tables with the warehouse date dimension.

```sql
INSERT INTO fact_sales
SELECT
    oi.order_item_id AS sales_id,
    o.order_id,
    o.customer_id,
    oi.product_id,
    o.store_id,
    d.date_id,
    oi.quantity,
    oi.unit_price,
    oi.quantity * oi.unit_price AS sales_amount
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN dim_date d
    ON o.order_date = d.full_date;
```

The sales amount is calculated as:

```text
sales_amount = quantity × unit_price
```

For example:

```text
2 Mouse × ₹1,000 = ₹2,000
```

---

# 11. Check the Fact Table

```sql
SELECT *
FROM fact_sales
ORDER BY sales_id;
```

Expected sales amounts:

```text
60000
2000
30000
2000
10000
3000
60000
```

Total sales:

```text
167000
```

---

# 12. Analytical Queries

## Total Sales

```sql
SELECT
    SUM(sales_amount) AS total_sales
FROM fact_sales;
```

Expected:

```text
167000
```

---

## Sales by Product

```sql
SELECT
    p.product_name,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_product p
    ON f.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_sales DESC;
```

---

## Sales by Customer

```sql
SELECT
    c.customer_name,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
GROUP BY c.customer_name
ORDER BY total_sales DESC;
```

---

## Sales by Category

```sql
SELECT
    p.category_name,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_product p
    ON f.product_id = p.product_id
GROUP BY p.category_name
ORDER BY total_sales DESC;
```

---

## Sales by Store

```sql
SELECT
    s.store_name,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_store s
    ON f.store_id = s.store_id
GROUP BY s.store_name
ORDER BY total_sales DESC;
```

---

## Sales by Month

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

# 13. Final Database Structure

Everything is inside one PostgreSQL database:

```text
sales_project
│
├── OLTP TABLES
│   ├── customers
│   ├── categories
│   ├── products
│   ├── stores
│   ├── orders
│   └── order_items
│
└── STAR SCHEMA
    ├── dim_customer
    ├── dim_product
    ├── dim_store
    ├── dim_date
    └── fact_sales
```

## Final Architecture

```text
                    dim_customer
                         |
                         |
dim_product -------- fact_sales -------- dim_store
                         |
                         |
                      dim_date
```

The overall process is:

```text
OLTP Tables
     ↓
Join and Transform Data
     ↓
Dimension Tables
     +
Fact Table
     ↓
Star Schema
     ↓
Analytics
```

## What This Exercise Demonstrates

This exercise demonstrates how a Data Engineer can take **normalized OLTP data** and transform it into a **Star Schema** designed for analytics.

You practiced:

- OLTP database design
- Primary and foreign keys
- Data transformation using SQL
- Fact table creation
- Dimension table creation
- Defining fact table grain
- Star Schema
- JOINs
- Aggregations
- Analytical queries