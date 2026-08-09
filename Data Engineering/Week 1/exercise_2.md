# Exercise 2: Identify OLTP vs OLAP Systems


Differentiate between **transactional (OLTP)** and **analytical (OLAP)** workloads using a real-world application.


# 1. OLTP — Online Transaction Processing

## Definition

**OLTP (Online Transaction Processing)** systems are used to handle the day-to-day transactions required to run an application.

Main characteristics:

- Fast transactions
- Frequent inserts and updates
- High consistency and reliability
- Usually focused on current operational data
- Small and targeted queries

> **OLTP = Run the business**

## Five Examples of OLTP Operations

| # | OLTP Operation | Example | Why is it OLTP? |
|---|---|---|---|
| 1 | Create an order | Customer places an order | Creates a new transaction that must be processed immediately |
| 2 | Update order status | Restaurant changes status to "Preparing" | Updates the current state of a transaction |
| 3 | Process payment | Customer pays ₹500 | Payment is a real-time transactional operation |
| 4 | Update delivery status | Delivery partner marks an order as "Delivered" | Updates the current transaction |
| 5 | Update customer information | Customer changes phone number or address | Modifies a specific customer record |

## 1.1 Create an Order

Example:

```text
Order ID       : 10001
Customer ID    : 501
Restaurant ID  : 201
Amount         : ₹450
Status         : PLACED
```

```sql
INSERT INTO orders
(order_id, customer_id, restaurant_id, amount, status)
VALUES
(10001, 501, 201, 450, 'PLACED');
```

**Why OLTP?** It is a single business transaction that needs to be processed quickly and reliably.

## 1.2 Update Order Status

```sql
UPDATE orders
SET status = 'ACCEPTED'
WHERE order_id = 10001;
```

**Why OLTP?** It updates the current state of one transaction.

## 1.3 Process Payment

A payment record may contain:

```text
payment_id
order_id
customer_id
amount
payment_status
payment_time
```

Example:

```sql
UPDATE payments
SET payment_status = 'SUCCESS'
WHERE payment_id = 50001;
```

**Why OLTP?** Payment processing is a transactional operation that must be accurate, consistent, and fast.

## 1.4 Update Delivery Status

```sql
UPDATE orders
SET status = 'DELIVERED'
WHERE order_id = 10001;
```

**Why OLTP?** It updates the current state of a specific order.

## 1.5 Update Customer Information

```sql
UPDATE customers
SET phone_number = '9876543210'
WHERE customer_id = 501;
```

**Why OLTP?** It updates a specific customer record as part of normal application activity.

---

# 2. OLAP — Online Analytical Processing

## Definition

**OLAP (Online Analytical Processing)** systems are designed for analyzing large amounts of data.

OLAP is commonly used for:

- Business reporting
- Historical analysis
- Aggregations
- Trend analysis
- Dashboards
- Business intelligence
- Decision-making

> **OLAP = Analyze the business**

## Five Examples of OLAP Queries

| # | OLAP Query / Analysis | Business Question | Why is it OLAP? |
|---|---|---|---|
| 1 | Monthly revenue by city | Which cities generate the most revenue? | Aggregates large amounts of historical data |
| 2 | Average delivery time by restaurant | Which restaurants have the slowest delivery? | Analyzes many historical orders |
| 3 | Top 10 restaurants by orders | Which restaurants receive the most orders? | Uses aggregation and ranking |
| 4 | Customer order frequency | How often do customers place orders? | Analyzes historical customer behavior |
| 5 | Cancellation rate by month | How has the cancellation rate changed over time? | Requires historical aggregation |

## 2.1 Revenue by City

```sql
SELECT
    city,
    SUM(order_amount) AS total_revenue
FROM orders
WHERE order_date >= '2026-01-01'
GROUP BY city;
```

**Why OLAP?** It analyzes a large number of historical orders and calculates revenue for each city.

## 2.2 Average Delivery Time

```sql
SELECT
    restaurant_id,
    AVG(delivery_time_minutes) AS avg_delivery_time
FROM orders
GROUP BY restaurant_id;
```

**Why OLAP?** It analyzes many historical orders and calculates an average for each restaurant.

## 2.3 Top 10 Restaurants

```sql
SELECT
    restaurant_id,
    COUNT(*) AS total_orders
FROM orders
GROUP BY restaurant_id
ORDER BY total_orders DESC
LIMIT 10;
```

**Why OLAP?** It aggregates many orders, groups them by restaurant, sorts the results, and identifies the top-performing restaurants.

## 2.4 Customer Order Frequency

```sql
SELECT
    customer_id,
    COUNT(*) AS total_orders
FROM orders
GROUP BY customer_id;
```

**Why OLAP?** It analyzes historical order behavior for many customers.

## 2.5 Monthly Cancellation Rate

```sql
SELECT
    DATE_TRUNC('month', order_date) AS order_month,
    COUNT(CASE WHEN status = 'CANCELLED' THEN 1 END) * 100.0
        / COUNT(*) AS cancellation_rate
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY order_month;
```

**Why OLAP?** It analyzes historical orders, groups them by month, and calculates an analytical metric.

---

# 3. OLTP vs OLAP Comparison

| Feature | OLTP | OLAP |
|---|---|---|
| Full Form | Online Transaction Processing | Online Analytical Processing |
| Main Purpose | Run the business | Analyze the business |
| Main Users | Applications / Customers | Analysts / Managers / Data Scientists |
| Data | Current operational data | Historical / Analytical data |
| Query Type | Small and simple | Large and complex |
| Transactions | Frequent | Usually fewer but heavier |
| Common Operations | INSERT / UPDATE / DELETE | SELECT / GROUP BY / JOIN |
| Example | Place an order | Analyze monthly revenue |
| Speed Requirement | Very fast transaction response | Fast analytical query response |
| Typical Database | PostgreSQL / MySQL | Snowflake / BigQuery / Redshift |

---

# 4. Important Data Engineering Concept

OLTP and OLAP are **not competing systems**. They solve different problems.

```text
                 COMPANY
                    │
          ┌─────────┴─────────┐
          ↓                   ↓
       OLTP                OLAP
          ↓                   ↑
   Run the business      Analyze business
          ↓                   ↑
    Application DB       Data Warehouse
```

A production data platform often needs both.

---

# 5. Conclusion

OLTP systems are designed to handle the **day-to-day transactions** required to run an application. Examples include creating an order, processing a payment, updating an order status, and updating customer information.

OLAP systems are designed to **analyze large amounts of historical data**. Examples include calculating revenue by city, finding top restaurants, analyzing customer behavior, and measuring cancellation rates.

The main difference can be remembered as:

> **OLTP = Run the business**

> **OLAP = Analyze the business**

