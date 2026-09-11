# Spark Fundamentals

## Goal

Most enterprise data pipelines use **Apache Spark** to process large amounts of data.

This document covers the important Spark concepts needed to understand and build efficient data pipelines.

---

# 1. Spark Execution Model

Spark processes data using a distributed architecture.

### Main Components

```text
Driver
  |
  |-- Creates Spark Job
  |
  |-- Creates Stages
  |
  |-- Sends Tasks
  |
  v
Executors
  |
  |-- Execute Tasks
  |-- Process Partitions
  |-- Store Cached Data
```

### Driver

The **Driver** is the main program that:

- Creates the SparkSession
- Builds the execution plan
- Creates jobs and stages
- Assigns tasks to executors

### Executor

Executors run the actual data-processing tasks.

They:

- Process data
- Store intermediate data
- Return results to the Driver

### Simple Example

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("SparkDemo") \
    .getOrCreate()

df = spark.read.csv("sales.csv", header=True)

df.show()
```

Here:

- Python program = Driver
- Spark executors = Workers
- `df.show()` = triggers execution

### Remember

> **Driver plans the work. Executors perform the work.**

---

# 2. Partitions

A **partition** is a chunk of data processed independently by Spark.

Suppose we have:

```text
10 GB Dataset

Partition 1 → 2 GB
Partition 2 → 2 GB
Partition 3 → 2 GB
Partition 4 → 2 GB
Partition 5 → 2 GB
```

Spark can process these partitions in parallel.

### Check Partitions

```python
df.rdd.getNumPartitions()
```

### Repartition

Used to increase or redistribute partitions.

```python
df = df.repartition(10)
```

### Coalesce

Used mainly to reduce the number of partitions.

```python
df = df.coalesce(5)
```

### Remember

> **Partitions allow Spark to process large datasets in parallel.**

---

# 3. Shuffle

A **shuffle** happens when Spark needs to move data between partitions.

For example:

```python
df.groupBy("customer_id").count()
```

Spark needs all records for the same customer together.

Data may move between executors:

```text
Executor 1 ─────┐
Executor 2 ─────┼──> Shuffle ──> New Partitions
Executor 3 ─────┤
Executor 4 ─────┘
```

### Operations that commonly cause Shuffle

- `groupBy`
- `join`
- `distinct`
- `orderBy`
- `repartition`

### Why Shuffle is Expensive

Shuffle involves:

- Network communication
- Disk I/O
- Serialization

Therefore, excessive shuffle can make a Spark job slow.

### Remember

> **Shuffle = moving data between partitions/executors.**

---

# 4. Lazy Evaluation

Spark does not immediately execute transformations.

Instead, Spark builds an **execution plan** and waits for an action.

Example:

```python
df = spark.read.csv("sales.csv", header=True)

filtered_df = df.filter(df.amount > 1000)

selected_df = filtered_df.select("customer_id", "amount")
```

Nothing has actually been executed yet.

When we run:

```python
selected_df.show()
```

Spark executes the required operations.

### Why Lazy Evaluation?

Spark can optimize the complete execution plan before running it.

```text
Transformations
      ↓
Execution Plan
      ↓
Optimization
      ↓
Action
      ↓
Execution
```

### Remember

> **Transformations build the plan. Actions trigger execution.**

---

# 5. Actions & Transformations

## Transformations

Transformations create a new DataFrame/RDD.

Examples:

```python
df.filter(df.amount > 1000)

df.select("customer_id", "amount")

df.groupBy("customer_id")

df.withColumn("tax", df.amount * 0.18)
```

They are generally **lazy**.

---

## Actions

Actions actually trigger Spark execution.

Examples:

```python
df.show()

df.count()

df.collect()

df.write.parquet("output/")
```

### Example

```python
filtered_df = df.filter(df.amount > 1000)   # Transformation

filtered_df.show()                         # Action
```

### Remember

| Type | Example | Executes Immediately? |
|---|---|---|
| Transformation | `filter()` | No |
| Transformation | `select()` | No |
| Transformation | `groupBy()` | No |
| Action | `show()` | Yes |
| Action | `count()` | Yes |
| Action | `write()` | Yes |

---

# 6. Broadcast Join

A **broadcast join** is useful when one table is small and the other table is large.

Example:

```text
Large Orders Table
       +
Small Customer Table
       ↓
Broadcast Customer Table
       ↓
Join
```

Instead of shuffling the large table, Spark sends the small table to each executor.

### Example

```python
from pyspark.sql.functions import broadcast

result = orders.join(
    broadcast(customers),
    "customer_id"
)
```

### Good Use Case

```text
Orders       → 500 GB
Customers    → 10 MB
```

Broadcasting the 10 MB customer table can avoid a large shuffle.

### Be Careful

Do not broadcast a large table.

Bad example:

```text
Orders       → 500 GB
Customers    → 100 GB
```

### Remember

> **Small table + Large table = Broadcast Join can be useful.**

---

# 7. Caching & Persist

Caching allows Spark to keep a DataFrame in memory for reuse.

Example:

```python
df.cache()

df.count()

df.show()
```

After the first action, Spark can reuse the cached data for later operations.

### When to Cache?

Cache a DataFrame when it is used multiple times.

Example:

```python
clean_df = df.filter(df.amount > 0)

clean_df.cache()

clean_df.count()
clean_df.groupBy("customer_id").count()
```

Without caching, Spark may recompute the same DataFrame.

### Persist

`persist()` allows different storage levels.

```python
from pyspark import StorageLevel

df.persist(StorageLevel.MEMORY_AND_DISK)
```

### Cache vs Persist

```text
cache()
   ↓
Default storage level

persist()
   ↓
Choose storage level
```

### Remember

> **Cache data that is expensive to compute and reused multiple times.**

Do not cache everything.

---

# 8. Performance Optimization

Spark performance mainly depends on:

- Partitioning
- Shuffle
- Joins
- File sizes
- Memory
- Data volume

## Important Optimization Techniques

### 1. Avoid unnecessary columns

Instead of:

```python
df.select("*")
```

Select only required columns:

```python
df.select(
    "customer_id",
    "product_id",
    "amount"
)
```

---

### 2. Filter early

Instead of processing unnecessary data:

```python
df.filter(df.amount > 1000)
```

Filter data as early as practical.

---

### 3. Avoid unnecessary shuffle

Operations such as:

```python
groupBy()
join()
distinct()
orderBy()
repartition()
```

can cause shuffle.

Use them carefully.

---

### 4. Use Broadcast Join

For a small lookup table:

```python
orders.join(
    broadcast(customers),
    "customer_id"
)
```

---

### 5. Choose Partitions Carefully

Too few partitions:

```text
Few partitions
     ↓
Not enough parallelism
     ↓
Slow processing
```

Too many partitions:

```text
Too many tiny partitions
     ↓
Scheduling overhead
     ↓
Slow processing
```

---

### 6. Use Efficient File Formats

Prefer:

```text
Parquet
ORC
Delta
```

instead of repeatedly processing large CSV files.

---

### 7. Check the Execution Plan

Use:

```python
df.explain()
```

This helps identify:

- Shuffles
- Joins
- Scans
- Execution strategies

### Remember

> **Good Spark performance = less unnecessary data + less unnecessary shuffle + appropriate partitions.**

---

# 9. File Formats — Parquet, ORC

## CSV

CSV is simple and human-readable.

```text
customer_id,amount
101,500
102,700
```

But CSV is usually not ideal for large Spark pipelines.

Problems:

- Larger file size
- Slower reading
- No efficient column-level storage
- Schema information is limited

---

## Parquet

Parquet is a **columnar file format**.

Example:

```python
df.write.parquet("sales_parquet/")
```

Read:

```python
df = spark.read.parquet("sales_parquet/")
```

Advantages:

- Columnar storage
- Compression
- Faster analytical queries
- Stores schema
- Works very well with Spark

---

## ORC

ORC is also a columnar storage format.

Example:

```python
df.write.orc("sales_orc/")
```

Read:

```python
df = spark.read.orc("sales_orc/")
```

Advantages:

- Compression
- Columnar storage
- Efficient for analytical workloads
- Supports schema information

---

## Simple Comparison

| Format | Best For |
|---|---|
| CSV | Simple data exchange |
| Parquet | General Spark analytics |
| ORC | Large-scale analytical workloads |
| Delta | Data lakes with table management |

### Remember

> **For Spark data pipelines, Parquet is a very common default choice.**

---

# 10. Delta Lake Basics

Delta Lake adds reliability and table-management features on top of data lake storage.

Instead of only having:

```text
Parquet Files
```

Delta provides:

```text
Delta Table
   |
   ├── Data Files
   └── Transaction Log
```

The transaction log tracks changes made to the table.

### Basic Example

```python
df.write.format("delta").save("sales_delta")
```

Read:

```python
df = spark.read.format("delta").load("sales_delta")
```

---

## Why Delta Lake?

Delta Lake provides features such as:

- ACID transactions
- Schema enforcement
- Schema evolution
- Time travel
- Reliable updates and deletes

### Example: Time Travel

You can access an older version of a Delta table.

Conceptually:

```text
Current Table
     ↓
Version 5
Version 4
Version 3
Version 2
Version 1
```

This is useful when you need to inspect or recover previous table states.

### Delta vs Parquet

| Feature | Parquet | Delta |
|---|---|---|
| Columnar format | Yes | Uses Parquet |
| Compression | Yes | Yes |
| ACID transactions | No | Yes |
| Schema enforcement | Limited | Yes |
| Time travel | No | Yes |
| Updates/Deletes | Limited | Supported |

### Remember

> **Delta Lake = Data Lake storage + reliability + transaction management.**

---

# Quick Revision

```text
Spark
 |
 ├── Execution Model
 │     ├── Driver
 │     └── Executors
 |
 ├── Partitions
 │     └── Parallel processing
 |
 ├── Shuffle
 │     └── Data movement between partitions
 |
 ├── Lazy Evaluation
 │     └── Execution waits for Action
 |
 ├── Transformations
 │     └── filter, select, groupBy
 |
 ├── Actions
 │     └── show, count, write
 |
 ├── Broadcast Join
 │     └── Small table + Large table
 |
 ├── Cache / Persist
 │     └── Reuse expensive data
 |
 ├── Performance
 │     ├── Reduce shuffle
 │     ├── Filter early
 │     ├── Select required columns
 │     └── Choose partitions carefully
 |
 ├── File Formats
 │     ├── Parquet
 │     └── ORC
 |
 └── Delta Lake
       ├── ACID
       ├── Schema management
       └── Time travel
```

# Key Things to Remember

1. **Driver plans the work; Executors execute it.**
2. **Partitions enable parallel processing.**
3. **Shuffle moves data between partitions and can be expensive.**
4. **Spark transformations are lazy.**
5. **Actions trigger execution.**
6. **Broadcast joins are useful when one table is small.**
7. **Cache/Persist when expensive data is reused.**
8. **Reduce unnecessary data and shuffle for better performance.**
9. **Parquet and ORC are efficient columnar formats.**
10. **Delta Lake adds reliability and transaction features to data lakes.**