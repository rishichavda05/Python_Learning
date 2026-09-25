# AWS Cloud Data Engineering

## Goal

Understand the basic AWS services used to build real-world cloud data pipelines.

---

# 1. AWS IAM

## What is IAM?

IAM (Identity and Access Management) controls **who can access AWS resources and what they can do**.

In simple words:

> IAM = Users + Permissions + Access Control

## Key Concepts

### User

Represents a person or application that needs AWS access.

Example:

```text
Data Engineer
```

### Group

A collection of users with similar permissions.

Example:

```text
Data Engineers
```

### Role

A role provides temporary permissions to AWS services or users.

Example:

```text
Lambda → Access S3
Glue → Access S3
```

### Policy

A policy defines what actions are allowed or denied.

Example:

```text
Allow reading files from S3
```

## Data Engineering Example

A Glue job needs to read CSV files from S3.

```text
Glue Job
   |
   | IAM Role
   ↓
S3 Bucket
   |
   ↓
CSV Files
```

The IAM role gives Glue permission to access S3.

## Remember

```text
IAM = Who can access what?
```

---

# 2. Amazon S3

## What is S3?

Amazon S3 (Simple Storage Service) is AWS object storage.

It is commonly used to store:

- CSV
- JSON
- Parquet
- Images
- Logs
- Backup files
- Data Lake files

## Basic Structure

```text
S3
 └── Bucket
      ├── raw/
      ├── processed/
      └── archive/
```

Example:

```text
s3://company-data/raw/sales.csv
```

## Bucket

A bucket is a container for storing objects.

## Object

An object is a file stored inside S3.

Example:

```text
sales.csv
customers.json
orders.parquet
```

## Data Engineering Example

```text
API
 ↓
S3 Raw Data
 ↓
Glue
 ↓
S3 Processed Data
 ↓
Athena
```

## Important Points

- S3 is highly scalable.
- S3 is commonly used for Data Lakes.
- Files are stored as objects.
- S3 is not a traditional database.

## Remember

```text
S3 = Cloud storage
```

---

# 3. AWS Lambda

## What is Lambda?

AWS Lambda is a **serverless compute service**.

You upload code and AWS runs it when needed.

You don't need to manage servers.

## Example

A new file is uploaded to S3.

```text
File uploaded
     ↓
     S3
     ↓
  Lambda
     ↓
Process file
```

Lambda can:

- Process small files
- Trigger pipelines
- Validate data
- Start Glue jobs
- Send notifications

## Example Use Case

When a CSV file arrives in:

```text
s3://company-data/raw/
```

Lambda can automatically trigger a Glue job.

```text
S3 Upload
    ↓
 Lambda
    ↓
Glue Job
```

## Remember

```text
Lambda = Run code without managing servers
```

---

# 4. AWS Glue

## What is Glue?

AWS Glue is a **serverless data integration and ETL service**.

It can be used to:

- Extract data
- Transform data
- Load data
- Discover schemas
- Run ETL jobs

## Main Components

### Glue Crawler

Automatically discovers the structure/schema of data.

Example:

```text
S3 CSV
 ↓
Glue Crawler
 ↓
Table Schema
```

### Glue Data Catalog

Stores metadata about datasets.

Example:

```text
Database: sales_db

Table: sales

Columns:
- order_id
- customer_id
- amount
- order_date
```

### Glue Job

Performs ETL transformations.

Example:

```text
S3 Raw Data
     ↓
Glue Job
     ↓
Clean Data
     ↓
S3 Processed
```

## Data Engineering Example

```text
S3
 ↓
Glue Crawler
 ↓
Data Catalog
 ↓
Glue ETL Job
 ↓
S3 Processed Data
```

## Remember

```text
Glue = Serverless ETL
```

---

# 5. Amazon Athena

## What is Athena?

Amazon Athena is a **serverless SQL query service**.

It allows you to query data directly from S3 using SQL.

Example:

```sql
SELECT *
FROM sales
WHERE amount > 1000;
```

## Basic Architecture

```text
S3
 ↓
Athena
 ↓
SQL Query
 ↓
Result
```

You don't need to load the data into a database first.

## Example

Data stored in:

```text
S3
 └── sales/
      └── sales.parquet
```

Athena can query the data using SQL.

```sql
SELECT
    customer_id,
    SUM(amount) AS total_sales
FROM sales
GROUP BY customer_id;
```

## Remember

```text
Athena = SQL directly on S3 data
```

---

# 6. Amazon RDS

## What is RDS?

Amazon RDS (Relational Database Service) is a managed relational database service.

It supports databases such as:

- PostgreSQL
- MySQL
- MariaDB
- Oracle
- SQL Server

## Why use RDS?

AWS manages many database administration tasks such as:

- Backups
- Patching
- Infrastructure
- Monitoring

## Example

An application stores transactional data in PostgreSQL.

```text
Application
     ↓
RDS PostgreSQL
     ↓
Orders
Customers
Products
```

A data pipeline can extract data from RDS and load it into S3.

```text
RDS
 ↓
ETL
 ↓
S3
```

## Remember

```text
RDS = Managed relational database
```

---

# 7. Amazon Redshift

## What is Redshift?

Amazon Redshift is a **cloud data warehouse** designed for analytics.

It is useful for querying large amounts of structured data.

## Example

```text
Application
     ↓
RDS
     ↓
ETL
     ↓
Redshift
     ↓
BI / Analytics
```

Example tables:

```text
fact_sales
dim_customer
dim_product
dim_date
```

## Redshift vs RDS

| RDS | Redshift |
|---|---|
| Transactional workloads | Analytical workloads |
| OLTP | OLAP |
| Application database | Data warehouse |
| Frequent small transactions | Large analytical queries |

## Remember

```text
RDS = Application database
Redshift = Analytics warehouse
```

---

# 8. Amazon CloudWatch

## What is CloudWatch?

CloudWatch is used for **monitoring AWS resources and applications**.

It can collect:

- Metrics
- Logs
- Events
- Alarms

## Example

A Lambda function fails.

CloudWatch can store its logs.

```text
Lambda
   ↓
CloudWatch Logs
```

You can also create an alarm.

```text
High Error Rate
      ↓
CloudWatch Alarm
      ↓
Notification
```

## Data Engineering Example

Monitor:

- Glue job failures
- Lambda errors
- RDS CPU usage
- Application logs

## Remember

```text
CloudWatch = Monitor and observe AWS resources
```

---

# 9. AWS Secrets Manager

## What is Secrets Manager?

AWS Secrets Manager securely stores sensitive information.

Examples:

- Database passwords
- API keys
- Credentials
- Tokens

## Bad Practice

Don't write passwords directly in code.

```python
password = "mypassword123"
```

## Better Practice

Store the password in Secrets Manager.

```text
Application
     ↓
Secrets Manager
     ↓
Database Credentials
```

## Example

A Python ETL job needs to connect to PostgreSQL.

Instead of storing:

```text
username
password
```

inside the code, retrieve them from Secrets Manager.

## Remember

```text
Secrets Manager = Secure storage for secrets
```

---

# 10. VPC Basics

## What is VPC?

VPC (Virtual Private Cloud) is a logically isolated network in AWS.

It allows you to control:

- IP addresses
- Subnets
- Routing
- Network access
- Security

## Basic Structure

```text
VPC
│
├── Public Subnet
│
└── Private Subnet
```

## Public Subnet

Resources can have a route to the internet through an Internet Gateway.

## Private Subnet

Resources are normally isolated from direct internet access.

Databases are commonly placed in private subnets.

## Example

```text
Internet
   ↓
Application
   ↓
Private Network
   ↓
RDS
```

## Important Terms

### Subnet

A smaller network inside a VPC.

### Internet Gateway

Allows internet connectivity for resources that have appropriate routing.

### Route Table

Controls where network traffic goes.

### Security Group

Acts as a virtual firewall for AWS resources.

## Remember

```text
VPC = Your private AWS network
```

---

# 11. Cost Optimization

## What is Cost Optimization?

Cost optimization means using AWS resources efficiently while avoiding unnecessary expenses.

## Common Techniques

### 1. Delete unused resources

Remove:

- Unused EC2 instances
- Old databases
- Unused snapshots
- Unused load balancers

### 2. Use appropriate storage

Don't use expensive storage when cheaper storage is sufficient.

### 3. Compress data

For data lakes, formats such as:

```text
Parquet
```

can reduce storage and query costs.

### 4. Partition data

Example:

```text
sales/
 ├── year=2025/
 ├── year=2026/
```

Queries can scan only required partitions.

### 5. Monitor costs

Use AWS billing and monitoring tools to identify unexpected usage.

## Data Engineering Example

Instead of storing:

```text
100 GB CSV
```

use compressed Parquet files where appropriate.

```text
CSV
 ↓
Parquet
 ↓
Smaller storage
 ↓
Less data scanned
```

## Remember

```text
Cost Optimization = Use only the resources you need
```

---

# 12. S3 Storage Classes

S3 provides different storage classes for different access patterns.

## S3 Standard

Used for frequently accessed data.

Example:

```text
Current sales data
```

## S3 Standard-IA

IA = Infrequent Access.

Used when data is accessed less frequently.

Example:

```text
Monthly reports
```

## S3 One Zone-IA

Used for infrequently accessed data stored in a single Availability Zone.

Use it when data can be recreated and does not require the same resilience as multi-AZ storage.

## S3 Glacier Instant Retrieval

Used for archive data that still needs fast retrieval.

## S3 Glacier Flexible Retrieval

Used for long-term archival where retrieval can take longer.

## S3 Glacier Deep Archive

Designed for very long-term archival and very infrequent access.

Example:

```text
Old compliance records
```

## Simple Comparison

| Storage Class | Typical Use |
|---|---|
| S3 Standard | Frequently accessed data |
| Standard-IA | Infrequently accessed data |
| One Zone-IA | Infrequent, recreatable data |
| Glacier Instant Retrieval | Archive + fast retrieval |
| Glacier Flexible Retrieval | Long-term archive |
| Glacier Deep Archive | Very long-term archive |

## Remember

```text
Frequently used → Standard

Less frequently used → IA

Archive → Glacier
```

---

# Simple AWS Data Engineering Pipeline

The services above can work together to build a real cloud data pipeline.

```text
             Application
                  |
                  ↓
             RDS PostgreSQL
                  |
                  ↓
             ETL / Glue
                  |
                  ↓
            S3 Raw Data
                  |
                  ↓
             Glue Job
                  |
                  ↓
         S3 Processed Data
                  |
                  ↓
               Athena
                  |
                  ↓
              Analytics
```

Supporting services:

```text
IAM
 ↓
Controls permissions

Secrets Manager
 ↓
Stores credentials

CloudWatch
 ↓
Monitoring + Logs

VPC
 ↓
Network security

S3 Storage Classes
 ↓
Storage management

Cost Optimization
 ↓
Controls AWS spending
```

---

# Quick Revision

| Service | Simple Meaning |
|---|---|
| IAM | Access control |
| S3 | Cloud object storage |
| Lambda | Serverless code execution |
| Glue | Serverless ETL |
| Athena | SQL on S3 |
| RDS | Managed relational database |
| Redshift | Cloud data warehouse |
| CloudWatch | Monitoring and logs |
| Secrets Manager | Secure secret storage |
| VPC | Private AWS network |
| Cost Optimization | Reduce unnecessary AWS costs |
| Storage Classes | Choose storage based on access pattern |

---

# Key Data Engineering Flow

Remember this basic flow:

```text
RDS
 ↓
Glue
 ↓
S3
 ↓
Athena
 ↓
Analytics
```

And remember the supporting services:

```text
IAM          → Access
Secrets      → Credentials
VPC          → Network
CloudWatch   → Monitoring
Storage      → Data lifecycle
Cost         → Spending control
```
