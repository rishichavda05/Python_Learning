# Enterprise Storage Systems

## Goal

Learn the basic concepts behind modern enterprise storage systems used
in data engineering.

------------------------------------------------------------------------

## 1. Warehouse Concepts

A **Data Warehouse** is a system designed to store structured data for
**analytics and reporting**.

### Main Characteristics

-   Stores structured and cleaned data
-   Optimized for analytical queries
-   Supports SQL
-   Combines data from multiple sources
-   Commonly used by BI and reporting tools

### Example

``` text
Application / Database
        ↓
    ETL / ELT
        ↓
 Data Warehouse
        ↓
Reports / Dashboards
```

### Common Data Warehouses

-   Snowflake
-   Google BigQuery
-   Amazon Redshift

------------------------------------------------------------------------

## 2. Snowflake Architecture

**Snowflake** is a cloud-based data warehouse.

Its architecture separates **storage** and **compute**.

### Simple Architecture

``` text
          Snowflake
              |
      ┌───────┴───────┐
      ↓               ↓
   Storage          Compute
      |               |
  Data stored     Query processing
```

### Key Points

-   Cloud-native
-   Separate storage and compute
-   Compute is provided through **Virtual Warehouses**
-   Multiple workloads can run independently
-   Automatically handles many infrastructure tasks

### Example

One team can run reporting queries while another team runs ETL jobs
using separate compute resources.

------------------------------------------------------------------------

## 3. BigQuery Basics

**Google BigQuery** is a serverless cloud data warehouse from Google
Cloud.

### Key Points

-   Serverless
-   Uses SQL
-   No server management
-   Designed for large-scale analytics
-   Separates storage and compute
-   Supports columnar storage

### Example Query

``` sql
SELECT
    product_id,
    SUM(sales_amount) AS total_sales
FROM sales
GROUP BY product_id;
```

### When to Use

BigQuery is useful when you need to analyze very large datasets without
managing database servers.

------------------------------------------------------------------------

## 4. Redshift Basics

**Amazon Redshift** is a cloud data warehouse from AWS.

### Key Points

-   Designed for analytical workloads
-   Uses SQL
-   Integrates with AWS services
-   Uses column-oriented storage
-   Supports large datasets
-   Can be used as part of an AWS data platform

### Typical Flow

``` text
S3
 ↓
ETL / ELT
 ↓
Redshift
 ↓
BI / Analytics
```

------------------------------------------------------------------------

## 5. Lakehouse

A **Lakehouse** combines ideas from a **Data Lake** and a **Data
Warehouse**.

### Data Lake

Stores large amounts of raw data.

``` text
Raw CSV
JSON
Parquet
Logs
Images
```

### Data Warehouse

Stores structured data optimized for analytics.

### Lakehouse

Provides:

-   Low-cost data lake storage
-   Data warehouse-style analytics
-   Structured and semi-structured data support
-   Better data management

### Simple Architecture

``` text
             Lakehouse
                 |
        ┌────────┴────────┐
        ↓                 ↓
   Data Storage       Analytics
        |                 |
   Raw / Clean       SQL / BI
```

------------------------------------------------------------------------

## 6. Delta Lake

**Delta Lake** is a storage layer that adds reliability and
database-like features to data lakes.

It commonly works with Spark and cloud object storage.

### Important Features

-   ACID transactions
-   Schema enforcement
-   Schema evolution
-   Time travel
-   Reliable updates and deletes

### Example

``` text
S3 / ADLS / Cloud Storage
          ↓
      Delta Lake
          ↓
       Spark
```

### Why Use Delta Lake?

A normal collection of files can be difficult to update safely.

Delta Lake adds transaction management so data changes are more
reliable.

------------------------------------------------------------------------

## 7. Iceberg

**Apache Iceberg** is an open table format designed for large analytic
datasets.

It works with data stored in cloud object storage.

### Key Features

-   Schema evolution
-   Partition evolution
-   Time travel
-   ACID-style table operations
-   Works with multiple data processing engines

### Example

``` text
Cloud Storage
     ↓
Iceberg Table
     ↓
Spark / Trino / Flink / Other Engines
```

### Delta Lake vs Iceberg

  Feature             Delta Lake   Iceberg
  ------------------- ------------ ------------------
  Open table format   Yes          Yes
  ACID transactions   Yes          Yes
  Time travel         Yes          Yes
  Schema evolution    Yes          Yes
  Common ecosystem    Spark        Multiple engines

------------------------------------------------------------------------

## 8. Partition Strategy

**Partitioning** divides a large dataset into smaller sections based on
a column.

This helps reduce the amount of data that needs to be scanned.

### Example

Suppose a sales table contains 5 years of data.

Instead of:

``` text
sales/
    all_data
```

Partition by year:

``` text
sales/
    year=2024/
    year=2025/
    year=2026/
```

A query for 2026 can scan only the relevant partition.

### Good Partition Columns

Common choices include:

-   Date
-   Year
-   Month
-   Region

### Important

Do not create too many tiny partitions. This can increase metadata and
file-management overhead.

------------------------------------------------------------------------

## 9. Clustering

**Clustering** organizes data so that related values are stored closer
together.

It can improve query performance when queries frequently filter or group
by certain columns.

### Example

Suppose queries frequently use:

``` sql
WHERE customer_id = 1001
```

Clustering data around `customer_id` can help improve query performance.

### Partitioning vs Clustering

  Partitioning                        Clustering
  ----------------------------------- --------------------------------------------
  Divides data into larger sections   Organizes data within storage
  Often based on date                 Often based on frequently filtered columns
  Helps eliminate partitions          Helps reduce scanned data

------------------------------------------------------------------------

## 10. Compression

**Compression** reduces the physical size of stored data.

### Benefits

-   Less storage required
-   Lower storage cost
-   Less data transferred
-   Faster I/O in many cases

### Common Formats

For analytics, columnar formats such as **Parquet** are commonly used.

``` text
CSV
 ↓
Large file size

Parquet + Compression
 ↓
Smaller storage
 ↓
Efficient analytical queries
```

### Example

A large CSV dataset can often become significantly smaller when stored
as compressed Parquet.

------------------------------------------------------------------------

## 11. Time Travel

**Time Travel** allows you to access an earlier version of data.

It is useful when:

-   Data was accidentally deleted
-   Incorrect data was loaded
-   You need to compare historical versions
-   You want to recover previous data

### Simple Example

``` text
10:00 → Correct data
11:00 → Incorrect update
12:00 → Need previous version
```

With time travel, the system can provide access to the earlier state of
the data, depending on the platform's retention settings.

### Systems Supporting Time Travel

Examples include:

-   Snowflake
-   Delta Lake
-   Apache Iceberg
-   BigQuery

------------------------------------------------------------------------

# Quick Comparison

  Technology       Main Purpose
  ---------------- ------------------------------------
  Data Warehouse   Analytical SQL workloads
  Snowflake        Cloud data warehouse
  BigQuery         Serverless cloud data warehouse
  Redshift         AWS cloud data warehouse
  Lakehouse        Data lake + warehouse approach
  Delta Lake       Reliable lakehouse tables
  Iceberg          Open table format for analytics
  Partitioning     Reduce data scanned
  Clustering       Organize data for query efficiency
  Compression      Reduce storage and I/O
  Time Travel      Access previous data versions

------------------------------------------------------------------------

# Key Takeaways

-   **Warehouse** → Optimized for analytics.
-   **Snowflake** → Separates storage and compute.
-   **BigQuery** → Serverless analytics warehouse.
-   **Redshift** → AWS analytical data warehouse.
-   **Lakehouse** → Combines data lake flexibility with warehouse
    capabilities.
-   **Delta Lake** → Adds reliability and transactions to data lakes.
-   **Iceberg** → Open table format for large analytical datasets.
-   **Partitioning** → Divides data to reduce scanning.
-   **Clustering** → Organizes data for efficient queries.
-   **Compression** → Reduces storage and I/O.
-   **Time Travel** → Accesses previous versions of data.

# Learning Flow

``` text
Warehouse Concepts
        ↓
Snowflake
        ↓
BigQuery
        ↓
Redshift
        ↓
Lakehouse
        ↓
Delta Lake
        ↓
Iceberg
        ↓
Partitioning
        ↓
Clustering
        ↓
Compression
        ↓
Time Travel
```
