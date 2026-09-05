# Data Transformation & PySpark Basics

## Goal

Learn basic transformation logic before moving to distributed data processing systems.

---

# 1. Cleaning Data

## What is Data Cleaning?

Data cleaning means finding and fixing incorrect, missing, or unwanted data.

For example, a player dataset may contain:

- Extra spaces in names
- Incorrect data types
- Missing values
- Duplicate records
- Invalid values

### Example

```python
df["player_name"] = df["player_name"].str.strip()
df["age"] = df["age"].astype(int)
```

Here:

- `strip()` removes extra spaces.
- `astype(int)` converts a column to integer.

**Simple idea:** Clean the data before using it for analysis or reporting.

---

# 2. Handling Nulls

## What is a Null?

A null means a value is missing.

Example:

| player_name | age | team |
|---|---:|---|
| Virat | 36 | India |
| Rohit | 37 | India |
| Rahul | NULL | India |

The `age` value for Rahul is missing.

### Find Null Values

```python
df.isnull().sum()
```

### Remove Null Rows

```python
df.dropna()
```

### Replace Null Values

```python
df["age"] = df["age"].fillna(0)
```

**Simple idea:** Decide whether to remove missing data or replace it with a suitable value.

---

# 3. Duplicate Removal

## What is a Duplicate?

A duplicate is the same record appearing more than once.

Example:

| player_id | player_name |
|---:|---|
| 101 | Virat |
| 102 | Rohit |
| 101 | Virat |

Player `101` appears twice.

### Find Duplicates

```python
df.duplicated()
```

### Remove Duplicates

```python
df = df.drop_duplicates()
```

### Remove Duplicates Based on One Column

```python
df = df.drop_duplicates(subset=["player_id"])
```

**Simple idea:** Remove duplicate records when they represent the same real-world data.

---

# 4. Aggregations

## What is Aggregation?

Aggregation means combining multiple rows to calculate a summary.

Common aggregation functions:

- `sum()`
- `count()`
- `mean()`
- `min()`
- `max()`

### Example

Suppose we have:

| player_name | runs |
|---|---:|
| Virat | 80 |
| Rohit | 60 |
| Virat | 50 |

Find total runs by player:

```python
df.groupby("player_name")["runs"].sum()
```

Result:

| player_name | runs |
|---|---:|
| Virat | 130 |
| Rohit | 60 |

### Multiple Aggregations

```python
df.groupby("player_name")["runs"].agg(
    ["sum", "mean", "max"]
)
```

**Simple idea:** Aggregation converts detailed records into useful summaries.

---

# 5. Joins

## What is a Join?

A join combines data from two tables using a common column.

Example:

### Players

| player_id | player_name | team_id |
|---:|---|---:|
| 101 | Virat | 1 |
| 102 | Rohit | 1 |

### Teams

| team_id | team_name |
|---:|---|
| 1 | India |

We can join these tables using `team_id`.

### Pandas Example

```python
result = players.merge(
    teams,
    on="team_id",
    how="inner"
)
```

### Common Join Types

- **Inner Join** - Returns matching records from both tables.
- **Left Join** - Returns all records from the left table and matching records from the right table.
- **Right Join** - Returns all records from the right table and matching records from the left table.

**Simple idea:** Joins are used when required information is stored in different tables.

---

# 6. Window Operations

## What is a Window Operation?

A window operation performs calculations across related rows without combining those rows into one row.

For example, we may want to rank players based on their runs.

### Example

| player_name | runs |
|---|---:|
| Virat | 800 |
| Rohit | 650 |
| Rahul | 500 |

In PySpark, a window can be used for ranking:

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import rank

window = Window.orderBy(df["runs"].desc())

df = df.withColumn(
    "rank",
    rank().over(window)
)
```

Result:

| player_name | runs | rank |
|---|---:|---:|
| Virat | 800 | 1 |
| Rohit | 650 | 2 |
| Rahul | 500 | 3 |

**Simple idea:** Window operations are useful for ranking, running totals, and calculations across related rows.

---

# 7. Feature Engineering

## What is Feature Engineering?

Feature engineering means creating new useful columns from existing data.

It is commonly used in analytics and machine learning.

### Example

Suppose we have:

| player_name | runs | matches |
|---|---:|---:|
| Virat | 800 | 10 |

We can create a new feature called `runs_per_match`.

```python
df["runs_per_match"] = df["runs"] / df["matches"]
```

Result:

| player_name | runs | matches | runs_per_match |
|---|---:|---:|---:|
| Virat | 800 | 10 | 80 |

Another example:

```python
df["is_high_scorer"] = df["runs"] > 500
```

**Simple idea:** Feature engineering creates meaningful information from existing data.

---

# 8. Introduction to PySpark

## What is PySpark?

PySpark is the Python API for Apache Spark.

Apache Spark is a distributed data processing framework designed to process large amounts of data.

Python developers can use PySpark to work with Spark.

### Why PySpark?

Pandas is excellent for small and medium-sized datasets.

PySpark is useful when:

- Data is very large.
- Data needs to be processed across multiple machines.
- Distributed processing is required.

### Simple PySpark Example

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder     .appName("PlayerAnalysis")     .getOrCreate()

df = spark.read.csv(
    "players.csv",
    header=True,
    inferSchema=True
)

df.show()
```

**Simple idea:** PySpark allows Python developers to use Apache Spark for large-scale data processing.

---

# 9. Spark Architecture

Spark uses a distributed architecture.

The main components are:

### Driver

The Driver is the main process that:

- Runs the application.
- Creates the Spark session.
- Creates the execution plan.
- Coordinates the work.

### Executor

Executors perform the actual data processing.

They:

- Execute tasks.
- Process data.
- Return results to the Driver.

### Cluster Manager

The Cluster Manager manages the resources required by Spark.

Examples include:

- Standalone
- YARN
- Kubernetes

### Simple Flow

```text
User Application
       |
       v
    Driver
       |
       v
 Cluster Manager
       |
   +---+---+
   |       |
   v       v
Executor Executor
   |       |
   +---+---+
       |
    Results
       |
       v
    Driver
```

**Simple idea:** The Driver coordinates the work, while Executors perform the work.

---

# 10. DataFrame

## What is a DataFrame?

A DataFrame is a distributed collection of data organized into rows and columns.

It is similar to a table in a database or a DataFrame in Pandas.

### Create a DataFrame

```python
data = [
    (101, "Virat", 800),
    (102, "Rohit", 650),
    (103, "Rahul", 500)
]

columns = ["player_id", "player_name", "runs"]

df = spark.createDataFrame(data, columns)

df.show()
```

### Select Columns

```python
df.select("player_name", "runs").show()
```

### Filter Data

```python
df.filter(df["runs"] > 600).show()
```

### Add a New Column

```python
from pyspark.sql.functions import col

df = df.withColumn(
    "runs_per_match",
    col("runs") / 10
)
```

### Group Data

```python
df.groupBy("player_name").sum("runs").show()
```

**Simple idea:** Spark DataFrames provide an easy way to work with structured data using distributed processing.

---

# Quick Summary

| Topic | Main Idea |
|---|---|
| Cleaning Data | Fix incorrect or unwanted data |
| Handling Nulls | Deal with missing values |
| Duplicate Removal | Remove repeated records |
| Aggregations | Calculate summaries |
| Joins | Combine data from tables |
| Window Operations | Calculate across related rows |
| Feature Engineering | Create useful new columns |
| PySpark | Python API for Apache Spark |
| Spark Architecture | Driver coordinates, Executors process |
| DataFrame | Table-like distributed data structure |

## Learning Flow

```text
Raw Data
   |
   v
Clean Data
   |
   v
Handle Nulls
   |
   v
Remove Duplicates
   |
   v
Joins / Aggregations
   |
   v
Window Operations
   |
   v
Feature Engineering
   |
   v
PySpark
   |
   v
Spark Architecture
   |
   v
Spark DataFrame
```
