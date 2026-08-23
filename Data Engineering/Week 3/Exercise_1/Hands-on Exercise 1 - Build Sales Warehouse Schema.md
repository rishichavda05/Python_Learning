# Hands-on Exercise 1: Build Sales Warehouse Schema

## Goal

Build a simple **Sales Data Warehouse** using a **Star Schema**.

The warehouse will contain:

- 1 Fact Table
- 4 Dimension Tables

### Schema

```text
              dim_customer
                   |
                   |
dim_product — fact_sales — dim_date
                   |
                   |
               dim_store
```

---

## 1. Create Database

```sql
CREATE DATABASE sales_warehouse;
```

Connect to the `sales_warehouse` database before creating the tables.

---

## 2. Create Dimension Tables

### Customer Dimension

Stores customer information.

```sql
CREATE TABLE dim_customer (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(100)
);
```

### Product Dimension

Stores product information.

```sql
CREATE TABLE dim_product (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(100),
    price DECIMAL(10,2)
);
```

### Date Dimension

Stores date-related information.

```sql
CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    full_date DATE,
    month INT,
    year INT
);
```

### Store Dimension

Stores store information.

```sql
CREATE TABLE dim_store (
    store_id INT PRIMARY KEY,
    store_name VARCHAR(100),
    city VARCHAR(100)
);
```

---

## 3. Create Fact Table

The `fact_sales` table stores actual sales transactions.

```sql
CREATE TABLE fact_sales (
    sale_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    date_id INT,
    store_id INT,
    quantity INT,
    sales_amount DECIMAL(10,2),

    FOREIGN KEY (customer_id)
        REFERENCES dim_customer(customer_id),

    FOREIGN KEY (product_id)
        REFERENCES dim_product(product_id),

    FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id),

    FOREIGN KEY (store_id)
        REFERENCES dim_store(store_id)
);
```

The foreign keys connect the fact table to the dimension tables.

---

## 4. Insert Sample Data

### Customers

```sql
INSERT INTO dim_customer VALUES
(1, 'Rahul', 'Ahmedabad', 'India'),
(2, 'Priya', 'Mumbai', 'India'),
(3, 'Amit', 'Delhi', 'India');
```

### Products

```sql
INSERT INTO dim_product VALUES
(1, 'Laptop', 'Electronics', 60000),
(2, 'Mouse', 'Electronics', 1000),
(3, 'Chair', 'Furniture', 5000);
```

### Dates

```sql
INSERT INTO dim_date VALUES
(1, '2026-01-10', 1, 2026),
(2, '2026-01-15', 1, 2026),
(3, '2026-02-05', 2, 2026);
```

### Stores

```sql
INSERT INTO dim_store VALUES
(1, 'Ahmedabad Store', 'Ahmedabad'),
(2, 'Mumbai Store', 'Mumbai');
```

### Sales

```sql
INSERT INTO fact_sales VALUES
(1, 1, 1, 1, 1, 1, 60000),
(2, 2, 2, 1, 2, 2, 2000),
(3, 3, 3, 2, 1, 1, 5000),
(4, 1, 2, 3, 1, 3, 3000);
```

---

## 5. Test the Warehouse

### View all sales

```sql
SELECT *
FROM fact_sales;
```

### Get Customer and Product Details

```sql
SELECT
    c.customer_name,
    p.product_name,
    f.quantity,
    f.sales_amount
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
JOIN dim_product p
    ON f.product_id = p.product_id;
```

### Calculate Total Sales

```sql
SELECT
    SUM(sales_amount) AS total_sales
FROM fact_sales;
```

### Sales by Product

```sql
SELECT
    p.product_name,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_product p
    ON f.product_id = p.product_id
GROUP BY p.product_name;
```

---

## 6. Expected Result

The total sales should be:

```text
70000
```

Sales by product:

```text
Laptop    → 60000
Mouse     → 5000
Chair     → 5000
```

---

## 7. What This Exercise Covers

This exercise demonstrates:

- **Star Schema** — Fact table connected to dimension tables
- **Fact Table** — Stores sales transactions
- **Dimension Tables** — Store descriptive information
- **Primary Keys** — Uniquely identify records
- **Foreign Keys** — Connect tables
- **JOINs** — Combine warehouse data
- **Aggregation** — Calculate total sales

## Final Structure

```text
sales_warehouse
│
├── dim_customer
├── dim_product
├── dim_date
├── dim_store
└── fact_sales
```

The result is a simple **Sales Data Warehouse** that can be used for reporting and analytics.