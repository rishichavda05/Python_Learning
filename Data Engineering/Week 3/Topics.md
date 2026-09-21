# Week 3 - SQL for Data Engineering

This week covers important SQL concepts used in Data Engineering, databases, and data warehouses.

---

## 1. Advanced Joins

### What is it?

A JOIN is used to combine data from two or more tables using a related column.

For example, an `athletes` table may contain `sport_id`, while a `sports` table contains the sport name.

### Why is it used?

Data is usually stored in multiple tables. JOINs allow us to bring related data together when querying it.

### Example

**athletes**

| athlete_id | name | sport_id |
|---|---|---|
| 1 | Virat | 1 |
| 2 | Neeraj | 2 |

**sports**

| sport_id | sport_name |
|---|---|
| 1 | Cricket |
| 2 | Athletics |

### SQL

```sql
SELECT a.name, s.sport_name
FROM athletes a
INNER JOIN sports s
    ON a.sport_id = s.sport_id;
```

### Result

| name | sport_name |
|---|---|
| Virat | Cricket |
| Neeraj | Athletics |

Common JOIN types are:

- `INNER JOIN` – returns matching rows from both tables.
- `LEFT JOIN` – returns all rows from the left table and matching rows from the right.
- `RIGHT JOIN` – returns all rows from the right table and matching rows from the left.
- `FULL OUTER JOIN` – returns all rows from both tables.
- `SELF JOIN` – joins a table with itself.
- `CROSS JOIN` – creates combinations of rows from both tables.

---

## 2. Window Functions

### What is it?

A window function performs a calculation across related rows while keeping the original rows.

Unlike `GROUP BY`, it does not combine multiple rows into one row.

### Why is it used?

Window functions are useful for:

- Ranking
- Comparing rows
- Running totals
- Finding previous or next values
- Calculating values within groups

### Example

Suppose we have:

| athlete | score |
|---|---:|
| A | 95 |
| B | 90 |
| C | 85 |

We want to give each athlete a rank.

### SQL

```sql
SELECT
    athlete,
    score,
    RANK() OVER (ORDER BY score DESC) AS ranking
FROM performance;
```

### Result

| athlete | score | ranking |
|---|---:|---:|
| A | 95 | 1 |
| B | 90 | 2 |
| C | 85 | 3 |

Common window functions include:

```text
ROW_NUMBER()
RANK()
DENSE_RANK()
LAG()
LEAD()
SUM()
AVG()
```

`PARTITION BY` can be used to perform calculations separately for each group.

```sql
SELECT
    athlete,
    country,
    score,
    RANK() OVER (
        PARTITION BY country
        ORDER BY score DESC
    ) AS country_rank
FROM performance;
```

This ranks athletes separately within each country.

---

## 3. CTEs

### What is it?

CTE stands for **Common Table Expression**.

A CTE creates a temporary result that can be used inside another SQL query.

It starts with the `WITH` keyword.

### Why is it used?

CTEs make large and complicated queries easier to read and understand.

### Example

Suppose we first want athletes with scores greater than 80 and then query them.

```sql
WITH top_athletes AS (
    SELECT *
    FROM performance
    WHERE score > 80
)
SELECT *
FROM top_athletes;
```

The query inside the CTE runs first and creates a temporary result called `top_athletes`.

We can also use multiple CTEs:

```sql
WITH high_scores AS (
    SELECT *
    FROM performance
    WHERE score > 80
),
ranked_athletes AS (
    SELECT *,
           RANK() OVER (ORDER BY score DESC) AS ranking
    FROM high_scores
)
SELECT *
FROM ranked_athletes;
```

CTEs are commonly used to break a complex transformation into multiple simple steps.

---

## 4. Recursive Queries

### What is it?

A recursive query is a query that repeatedly works with its own previous result.

It is mainly used for **hierarchical data**.

For example:

```text
CEO
 └── Manager
      └── Employee
           └── Intern
```

### Why is it used?

Recursive queries are useful when data has a parent-child relationship.

Examples:

- Employee and manager hierarchy
- Folder and subfolder structure
- Product categories
- Organization structures

### SQL

```sql
WITH RECURSIVE employee_tree AS (

    SELECT employee_id, name, manager_id
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.employee_id, e.name, e.manager_id
    FROM employees e
    JOIN employee_tree t
        ON e.manager_id = t.employee_id
)

SELECT *
FROM employee_tree;
```

The first query finds the top-level employee. The recursive part repeatedly finds employees who report to the previous level.

---

## 5. Indexes

### What is it?

An index is a database structure that helps the database find data faster.

It is similar to an index in a book. Instead of reading the entire book, you can use the index to quickly find the required page.

### Why is it used?

Indexes are mainly used to improve the speed of:

- `SELECT` queries
- Searches
- JOINs
- Filtering

### Example

Suppose we frequently search athletes by name.

```sql
SELECT *
FROM athletes
WHERE name = 'Virat';
```

We can create an index:

```sql
CREATE INDEX idx_athlete_name
ON athletes(name);
```

The database can use this index to find the required rows faster.

Indexes are useful, but they also require storage and can make `INSERT`, `UPDATE`, and `DELETE` operations slower because the index also needs to be updated.

---

## 6. Execution Plan

### What is it?

An execution plan shows how the database plans to execute a SQL query.

It helps us understand what the database is actually doing behind the scenes.

### Why is it used?

Execution plans are mainly used to find slow or inefficient queries.

For example, we may want to know:

- Is the database scanning the entire table?
- Is it using an index?
- Which JOIN is expensive?
- Which operation takes the most time?

### SQL

In PostgreSQL, we can use:

```sql
EXPLAIN
SELECT *
FROM athletes
WHERE country = 'India';
```

For actual execution information:

```sql
EXPLAIN ANALYZE
SELECT *
FROM athletes
WHERE country = 'India';
```

The database will show the operations it plans to perform or actually performed.

Execution plans are especially useful when optimizing queries on large tables.

---

## 7. Partitioning

### What is it?

Partitioning divides a large table into smaller logical pieces called partitions.

For example, a performance table may contain millions of records.

Instead of keeping all data in one partition, we can divide it by year:

```text
performance_2024
performance_2025
performance_2026
```

### Why is it used?

Partitioning can improve query performance and make large tables easier to manage.

For example, if a query only needs 2026 data, the database may only need to read the 2026 partition.

This is called **partition pruning**.

### Example

Conceptually:

```sql
CREATE TABLE performance (
    athlete_id INT,
    score INT,
    event_date DATE
)
PARTITION BY RANGE (event_date);
```

Partitions can then be created for different date ranges.

Partitioning is commonly used for large Data Warehouse tables, especially when data is naturally divided by date.

---

## 8. Normalization

### What is it?

Normalization is the process of organizing data into multiple related tables to reduce duplicate data.

### Why is it used?

It helps:

- Reduce data duplication
- Keep data consistent
- Make updates easier
- Avoid unnecessary repeated information

### Example

Instead of storing customer information repeatedly:

```text
orders
--------------------------------
order_id | customer_name | city
1        | Rahul         | Delhi
2        | Rahul         | Delhi
```

We can separate the data.

**customers**

```text
customer_id | customer_name | city
1            | Rahul         | Delhi
```

**orders**

```text
order_id | customer_id
1        | 1
2        | 1
```

Now customer information is stored only once.

### Normal Forms

The commonly discussed normal forms are:

- **1NF** – Values should be atomic.
- **2NF** – Should be in 1NF and have no partial dependency.
- **3NF** – Should be in 2NF and have no unnecessary transitive dependency.

Normalization is commonly associated with transactional database systems.

---

## 9. Denormalization

### What is it?

Denormalization is the process of intentionally keeping some duplicate data to make reading data faster or simpler.

It is basically the opposite approach to normalization.

### Why is it used?

Data warehouses and analytics systems often perform many read operations.

Reducing the number of JOINs can make analytical queries easier and sometimes faster.

### Example

Instead of:

```text
orders → customers → countries
```

we might store some customer and country information directly in an analytical table:

```text
orders
---------------------------------------
order_id | customer | city | country
1        | Rahul    | Delhi| India
```

This creates some duplication, but analytical queries may become simpler.

---

## 10. Star Schema

### What is it?

A Star Schema is a common Data Warehouse design.

It contains:

- One central **Fact Table**
- Multiple **Dimension Tables**

It looks like a star:

```text
              Dim_Athlete
                   |
Dim_Date ---- Fact_Performance ---- Dim_Sport
                   |
              Dim_Country
```

### Why is it used?

Star Schema makes analytical queries easier because the fact table connects directly to the dimensions.

### Example

**Fact_Performance**

```text
athlete_id
sport_id
date_id
score
rank
```

**Dim_Athlete**

```text
athlete_id
athlete_name
country
```

**Dim_Sport**

```text
sport_id
sport_name
```

**Dim_Date**

```text
date_id
date
month
year
```

This structure is widely used in Data Warehouses and BI systems.

---

## 11. Snowflake Schema

### What is it?

Snowflake Schema is similar to Star Schema, but dimension tables are further divided into smaller related tables.

### Why is it used?

It reduces duplicate data inside dimensions by normalizing them.

### Example

In a Star Schema:

```text
Fact_Performance
       |
  Dim_Athlete
```

In a Snowflake Schema:

```text
Fact_Performance
       |
  Dim_Athlete
       |
  Dim_Country
```

For example, instead of storing country information repeatedly inside the athlete dimension, we can create a separate country dimension.

### Star vs Snowflake

```text
Star:
Fact → Dimension

Snowflake:
Fact → Dimension → Sub-dimension
```

Star Schema is generally simpler, while Snowflake Schema has more normalized dimensions.

---

## 12. Fact Table

### What is it?

A Fact Table stores **business events, measurements, or numbers**.

In a sports system, a fact table could store athlete performance.

### Why is it used?

Fact tables allow us to analyze measurable business events.

### Example

```text
Fact_Performance
----------------
athlete_id
sport_id
date_id
score
rank
```

Here:

- `athlete_id` identifies the athlete.
- `sport_id` identifies the sport.
- `date_id` identifies the date.
- `score` and `rank` are measurements.

### Grain

The **grain** describes what one row represents.

For example:

> One row represents one athlete's performance in one event.

Defining the grain is very important when designing a fact table.

---

## 13. Dimension Table

### What is it?

A Dimension Table contains descriptive information about the data stored in a fact table.

### Why is it used?

Dimensions allow users to filter, group, and understand facts.

For example, we can analyze performance by:

- Athlete
- Sport
- Country
- Date

### Example

```text
Dim_Athlete
----------------
athlete_id
athlete_name
country
age
sport
```

Another common dimension is a Date Dimension:

```text
Dim_Date
----------------
date_id
date
day
month
quarter
year
```

Dimension tables usually contain descriptive attributes rather than measurements.

---

## 14. Slowly Changing Dimensions (SCD)

### What is it?

Slowly Changing Dimensions are techniques used to manage changes in dimension data over time.

For example, suppose an athlete changes their country.

Initially:

```text
Athlete: Rahul
Country: India
```

Later:

```text
Athlete: Rahul
Country: USA
```

We need to decide whether to keep the old value or update it.

### Why is it used?

SCD allows a Data Warehouse to correctly manage changes in dimension information.

### SCD Type 1

Type 1 simply **overwrites the old value**.

Before:

```text
Rahul | India
```

After:

```text
Rahul | USA
```

The old value is lost.

Type 1 is useful when historical changes are not important.

---

### SCD Type 2

Type 2 **keeps the history** by creating a new record.

Example:

```text
athlete_id | country | start_date | end_date
1          | India   | 2024-01-01 | 2025-01-01
1          | USA     | 2025-01-01 | NULL
```

Now we know that the athlete was associated with India before 2025 and USA after 2025.

Type 2 commonly uses columns such as:

```text
start_date
end_date
is_current
```

This is one of the most common SCD techniques in Data Warehousing.

---

### SCD Type 3

Type 3 stores the current value and a limited previous value.

Example:

```text
athlete | current_country | previous_country
Rahul   | USA             | India
```

Unlike Type 2, it does not keep unlimited historical records.

---

# Final Week 3 Summary

```text
Advanced Joins
      ↓
Combine data from multiple tables

Window Functions
      ↓
Calculate across rows

CTEs
      ↓
Break complex queries into smaller parts

Recursive Queries
      ↓
Work with hierarchical data

Indexes
      ↓
Improve data lookup speed

Execution Plans
      ↓
Understand and optimize query execution

Partitioning
      ↓
Divide large tables into smaller partitions

Normalization
      ↓
Reduce duplicate data

Denormalization
      ↓
Improve read/query simplicity

Star Schema
      ↓
Fact table + Dimension tables

Snowflake Schema
      ↓
Normalized Dimension tables

Fact Table
      ↓
Stores events and measurements

Dimension Table
      ↓
Stores descriptive information

SCD
      ↓
Manage changes in dimension data over time
```