# Production-Ready Data Pipelines

## Goal

Learn what makes data pipelines **production-ready**.

A pipeline that works on a developer's laptop is not automatically ready for production. A production pipeline should be reliable, testable, secure, observable, and easy to maintain.

---

# 1. Docker & Docker Compose

## What is Docker?

Docker is a platform used to package an application together with its dependencies into a **container**.

A container provides a consistent environment, so the application behaves similarly on a developer machine, testing server, and production server.

For a data engineering project, a Docker container might contain:

```text
Python
Pandas / PySpark
Application Code
Required Libraries
Configuration
```

### Why use Docker?

Without Docker:

```text
Developer Machine
Python 3.12
Library Version A

Production Server
Python 3.10
Library Version B

Result → Application may fail
```

With Docker:

```text
Docker Image
    ↓
Same environment
    ↓
Development
Testing
Production
```

### Important Docker Concepts

| Concept | Meaning |
|---|---|
| Image | Template used to create containers |
| Container | Running instance of an image |
| Dockerfile | Instructions for building an image |
| Volume | Stores data outside the container |
| Port | Allows communication with a container |
| Registry | Stores Docker images |

### Simple Dockerfile

```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Build and run:

```bash
docker build -t etl-pipeline .
docker run etl-pipeline
```

---

## Docker Compose

Docker Compose is useful when an application requires **multiple services**.

For example:

```text
        ETL Application
              |
       ----------------
       |              |
   PostgreSQL      Redis
```

A `docker-compose.yml` file can define these services.

Example:

```yaml
services:
  app:
    build: .
    depends_on:
      - postgres

  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: sales
      POSTGRES_USER: etl_user
      POSTGRES_PASSWORD: password
```

Run:

```bash
docker compose up
```

Stop:

```bash
docker compose down
```

### Key Idea

**Docker packages the application. Docker Compose helps run multiple containers together.**

---

# 2. CI/CD

CI/CD means **Continuous Integration and Continuous Delivery/Deployment**.

It automates activities such as:

```text
Code Push
   ↓
Install Dependencies
   ↓
Run Tests
   ↓
Run Quality Checks
   ↓
Build Application
   ↓
Deploy
```

## Continuous Integration — CI

CI checks code whenever developers push changes.

Typical CI tasks:

- Install Python dependencies
- Run Pytest
- Check code quality
- Build Docker image
- Check configuration

Example:

```text
Developer
    ↓
git push
    ↓
CI starts
    ↓
pytest
    ↓
Tests pass?
   /  Yes  No
  ↓    ↓
Build  Stop
```

## Continuous Delivery / Deployment — CD

CD takes successfully tested code and delivers or deploys it.

Example:

```text
GitHub
   ↓
CI Tests
   ↓
Docker Build
   ↓
Deployment
   ↓
Production
```

### Common CI/CD Tools

- GitHub Actions
- GitLab CI/CD
- Jenkins
- Azure DevOps

### Simple GitHub Actions Example

```yaml
name: ETL Tests

on:
  push:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - run: pip install -r requirements.txt
      - run: pytest
```

### Key Idea

CI/CD reduces manual work and helps catch problems **before code reaches production**.

---

# 3. Testing ETL

ETL means:

```text
Extract → Transform → Load
```

Testing verifies that every part of this process works correctly.

## Why Test ETL?

Imagine an ETL pipeline processes:

```text
1,000,000 sales records
```

If a transformation accidentally removes 100,000 records, the pipeline may technically finish successfully but produce incorrect business data.

Testing helps detect these problems.

## Types of ETL Tests

### 1. Unit Testing

Tests one small function.

Example:

```python
def calculate_total(price, quantity):
    return price * quantity
```

Test:

```python
def test_calculate_total():
    assert calculate_total(100, 5) == 500
```

### 2. Transformation Testing

Checks whether transformation logic produces the expected result.

```text
Input
100 + 200
   ↓
Transformation
   ↓
Expected Output
300
```

### 3. Data Quality Testing

Checks the quality of the data.

Examples:

```text
customer_id cannot be NULL
order_id must be unique
amount must be >= 0
```

### 4. Integration Testing

Checks whether multiple components work together.

Example:

```text
API → Python → PostgreSQL
```

The test verifies the complete interaction.

### Key Idea

Do not test only whether the pipeline **runs**. Test whether it produces the **correct data**.

---

# 4. Pytest

Pytest is a popular Python testing framework.

It makes it easy to create and run automated tests.

Install:

```bash
pip install pytest
```

## Simple Example

Application code:

```python
def add(a, b):
    return a + b
```

Test:

```python
def test_add():
    assert add(2, 3) == 5
```

Run:

```bash
pytest
```

Expected result:

```text
1 passed
```

## Testing ETL Functions

Example transformation:

```python
def clean_name(name):
    return name.strip().title()
```

Test:

```python
def test_clean_name():
    assert clean_name(" john ") == "John"
```

## Project Structure

```text
etl_project/
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
│
├── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
│
├── requirements.txt
└── README.md
```

### Useful Pytest Commands

Run all tests:

```bash
pytest
```

Run a specific file:

```bash
pytest tests/test_transform.py
```

Show detailed output:

```bash
pytest -v
```

### Key Idea

Pytest allows ETL developers to automatically verify that changes do not break existing logic.

---

# 5. Data Validation

Data validation checks whether data follows expected rules before it is processed or loaded.

Consider this customer data:

```text
customer_id | name  | age
-------------|-------|----
101          | John  | 25
102          | Sarah | 30
103          | Mike  | -5
```

The third record contains an invalid age.

## Common Validation Rules

### Not Null

```text
customer_id must not be NULL
```

### Unique

```text
customer_id must be unique
```

### Range

```text
age must be between 0 and 120
```

### Data Type

```text
customer_id → integer
amount      → decimal
order_date  → date
```

### Allowed Values

```text
status ∈ {pending, completed, cancelled}
```

## Simple Pandas Validation

```python
assert df["customer_id"].notna().all()

assert df["customer_id"].is_unique

assert (df["age"] >= 0).all()

assert df["status"].isin(
    ["pending", "completed", "cancelled"]
).all()
```

## Validation Flow

```text
Raw Data
   ↓
Validation
   ↓
Valid?
 /   Yes   No
 ↓     ↓
ETL   Reject
       ↓
      Alert
```

### Why Validation Matters

Without validation:

```text
Bad Data
   ↓
Transformation
   ↓
Database
   ↓
Reports
   ↓
Wrong Business Decisions
```

With validation:

```text
Bad Data
   ↓
Validation
   ↓
Rejected
   ↓
Alert
```

### Key Idea

**Validate data as early as possible.**

---

# 6. Great Expectations

Great Expectations is a framework for defining and running **data quality expectations**.

Instead of writing many custom validation statements, you can define reusable expectations for datasets.

Examples:

```text
customer_id should not be null
order_id should be unique
amount should be greater than 0
order_date should be a valid date
```

## Example Concept

```text
Incoming Dataset
       ↓
Great Expectations
       ↓
Run Expectations
       ↓
-------------------
|                 |
Pass              Fail
 ↓                 ↓
Continue          Stop/Alert
```

## Example Expectations

Conceptually:

```python
expect_column_values_to_not_be_null(
    "customer_id"
)
```

```python
expect_column_values_to_be_unique(
    "order_id"
)
```

```python
expect_column_values_to_be_between(
    "age",
    min_value=0,
    max_value=120
)
```

The exact API can vary between Great Expectations versions, so check the documentation for the version used in your project.

## When to Use It

Great Expectations is useful when:

- Data quality rules are numerous
- Validation needs to be repeatable
- Teams want documented expectations
- Data quality results need to be tracked

### Simple Difference

```text
Python assert
    ↓
Small/simple validation

Great Expectations
    ↓
Structured/reusable data-quality framework
```

### Key Idea

Great Expectations helps turn data quality rules into **formal, repeatable checks**.

---

# 7. Monitoring

Monitoring tells us what is happening inside a production pipeline.

A pipeline can complete without errors and still have a problem.

Example:

```text
Expected records: 1,000,000
Actual records:     100,000
```

The pipeline status may say `SUCCESS`, but the data is probably incomplete.

## What Should We Monitor?

### Pipeline Status

```text
SUCCESS
FAILED
RUNNING
```

### Runtime

Example:

```text
Normal runtime: 5 minutes
Current runtime: 45 minutes
```

### Record Count

```text
Expected: 500,000
Processed: 498,000
```

### Failed Records

```text
Processed: 500,000
Failed: 2,500
```

### Data Freshness

Checks how old the latest data is.

```text
Expected latest data: 10:00 AM
Actual latest data:   8:00 AM

Problem → Data is stale
```

## Monitoring Example

```text
Daily Sales Pipeline

Status: SUCCESS
Runtime: 4m 20s
Records: 250,000
Failed Records: 35
Data Freshness: 8 minutes
```

### Key Idea

Monitoring answers:

> **Is my pipeline healthy?**

---

# 8. Logging

Logging records what happens during pipeline execution.

A good production pipeline should provide useful logs.

## Example

```python
import logging

logging.basicConfig(level=logging.INFO)

logging.info("Pipeline started")
logging.info("Reading sales data")
logging.info("Records loaded: 100000")
logging.info("Transformation completed")
logging.info("Pipeline completed")
```

For errors:

```python
logging.error("Database connection failed")
```

## Log Levels

| Level | Purpose |
|---|---|
| DEBUG | Detailed troubleshooting information |
| INFO | Normal application events |
| WARNING | Something unexpected but not necessarily fatal |
| ERROR | An operation failed |
| CRITICAL | Serious failure |

## Good Logging

Instead of:

```text
Error
```

Prefer:

```text
ERROR: Failed to load sales data into PostgreSQL
```

Even better logs can include:

```text
timestamp
pipeline name
task name
record count
duration
error message
```

## What Not to Log

Never log sensitive information such as:

```text
Passwords
API Keys
Access Tokens
Database Secrets
```

### Key Idea

Monitoring tells you **that** something is wrong.

Logging helps explain **what happened and why**.

---

# 9. Alerting

Alerting sends a notification when a pipeline requires attention.

## Example

```text
Pipeline
   ↓
Monitoring
   ↓
Problem detected
   ↓
Alert
   ↓
Engineer
```

Possible alert channels:

- Email
- Slack
- Microsoft Teams
- PagerDuty
- Incident management systems

## What Should Trigger an Alert?

### Pipeline Failure

```text
ETL failed
```

### Data Quality Failure

```text
customer_id contains NULL values
```

### Data Freshness Problem

```text
Expected data < 1 hour old
Actual data = 5 hours old
```

### Performance Problem

```text
Expected runtime: 10 minutes
Actual runtime: 60 minutes
```

## Avoid Alert Overload

Not every warning should create a critical alert.

Example:

```text
WARNING → Log only

ERROR → Team notification

CRITICAL → Immediate incident alert
```

### Key Idea

An alert should be **actionable**. The person receiving it should know that something needs attention.

---

# 10. Performance

Performance means making the pipeline process data efficiently while using reasonable resources.

Important performance areas include:

- Execution time
- Memory usage
- CPU usage
- Database queries
- Network transfer
- Number of records processed

## Read Only Required Columns

Instead of loading:

```text
customer_id
name
email
age
address
phone
country
...
```

If you only need two columns:

```python
df = df[["customer_id", "amount"]]
```

This reduces unnecessary data processing.

## Process Data in Batches

Instead of:

```text
10 million records
       ↓
Process everything at once
```

Use:

```text
10 million records
       ↓
1 million per batch
       ↓
10 batches
```

This can reduce memory pressure.

## Use Efficient File Formats

For analytical workloads, Parquet is generally more efficient than CSV because it is columnar and supports compression.

Example:

```text
CSV
↓
Large text file

Parquet
↓
Columnar + compressed
```

## Database Performance

Avoid queries such as:

```sql
SELECT *
FROM sales;
```

when only a few columns are required.

Prefer:

```sql
SELECT order_id, customer_id, amount
FROM sales;
```

Use appropriate:

- Indexes
- Partitions
- Query filters
- Batch inserts

### Key Idea

Do not optimize blindly. **Measure first, identify the bottleneck, then optimize.**

---

# 11. Code Structure

Production code should be organized so that another developer can easily understand and maintain it.

Avoid putting the entire ETL process into one large file.

Bad:

```text
main.py
 └── 1000 lines of code
```

Better:

```text
etl_project/
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── validate.py
│   ├── load.py
│   └── config.py
│
├── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_validate.py
│
├── config/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Responsibility of Each File

### `extract.py`

Gets data from sources.

```text
API
CSV
Database
S3
```

### `transform.py`

Cleans and transforms data.

```text
Raw Data
 ↓
Clean
 ↓
Transform
```

### `validate.py`

Checks data quality.

### `load.py`

Writes data to the destination.

```text
PostgreSQL
Warehouse
Data Lake
```

### `config.py`

Loads configuration values.

## Example Flow

```python
data = extract_data()

data = transform_data(data)

validate_data(data)

load_data(data)
```

### Key Idea

Follow the principle:

> **One component should have one clear responsibility.**

---

# 12. Secrets & Configuration

Production pipelines often need:

```text
Database username
Database password
API keys
Cloud credentials
Database host
Bucket names
Environment settings
```

These values should not be hard-coded in application code.

## Bad Example

```python
DB_PASSWORD = "mypassword123"
```

This is dangerous because the secret can accidentally be committed to Git.

## Better Approach

Use environment variables:

```python
import os

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
```

Example `.env`:

```text
DB_HOST=localhost
DB_USER=etl_user
DB_PASSWORD=secret
DB_NAME=sales
```

And in Python:

```python
from dotenv import load_dotenv
import os

load_dotenv()

db_host = os.getenv("DB_HOST")
```

## Important Rule

Do not commit real secrets to Git.

Add `.env` to `.gitignore`:

```text
.env
```

## Production Secret Management

For real production environments, use a secret manager instead of storing secrets directly in source code.

Examples include:

- AWS Secrets Manager
- Azure Key Vault
- Google Cloud Secret Manager
- HashiCorp Vault

## Configuration vs Secret

Configuration:

```text
DB_HOST=production-db
DB_NAME=sales
BATCH_SIZE=10000
```

Secret:

```text
DB_PASSWORD=********
API_KEY=********
```

Both should be managed outside the application code, but secrets require stronger protection.

### Key Idea

**Code should be reusable across environments without changing the source code.**

---

# Production-Ready ETL Pipeline

All the concepts work together.

```text
                    Git Repository
                          |
                          ↓
                       CI/CD
                          |
                     Run Tests
                          |
                    Build Docker
                          |
                          ↓
                    ETL Pipeline
                          |
                    ┌─────┴─────┐
                    ↓           ↓
                 Extract     Logging
                    |
                    ↓
               Data Validation
                    |
              Valid? ───── No ───→ Alert
                |
               Yes
                ↓
             Transform
                |
                ↓
          Data Validation
                |
              Valid?
             /                 No        Yes
           ↓          ↓
         Alert       Load
                       |
                       ↓
                   Monitoring
                       |
                       ↓
                  Success / Alert
```

---

# Production Checklist

Before considering an ETL pipeline production-ready, check:

### Code

- [ ] Code is organized into reusable modules
- [ ] Functions have clear responsibilities
- [ ] Configuration is separated from code

### Testing

- [ ] Unit tests exist
- [ ] ETL transformations are tested
- [ ] Data quality checks exist
- [ ] Tests run automatically in CI

### Data Quality

- [ ] Required columns are validated
- [ ] NULL values are checked
- [ ] Duplicate records are checked
- [ ] Data types are validated
- [ ] Business rules are checked

### Reliability

- [ ] Pipeline failures are detected
- [ ] Failed tasks can be retried where appropriate
- [ ] Alerts are configured

### Monitoring

- [ ] Pipeline status is monitored
- [ ] Runtime is monitored
- [ ] Record counts are monitored
- [ ] Data freshness is monitored

### Security

- [ ] Passwords are not hard-coded
- [ ] API keys are not committed to Git
- [ ] `.env` is ignored
- [ ] Production secrets use a secret manager

### Deployment

- [ ] Docker image can be built
- [ ] Docker Compose works for local development
- [ ] CI/CD pipeline runs successfully

---

# Quick Summary

| Topic | Main Purpose |
|---|---|
| Docker | Package the application and dependencies |
| Docker Compose | Run multiple services together |
| CI/CD | Automate testing and deployment |
| Testing ETL | Verify pipeline correctness |
| Pytest | Test Python code automatically |
| Data Validation | Detect invalid data |
| Great Expectations | Create structured data-quality checks |
| Monitoring | Track pipeline health |
| Logging | Record pipeline activity |
| Alerting | Notify when action is required |
| Performance | Process data efficiently |
| Code Structure | Make code maintainable |
| Secrets & Configuration | Keep configuration and credentials secure |

---

# Final Concept

A production-ready data pipeline is more than:

```text
Extract → Transform → Load
```

It is:

```text
        Reliable Code
             +
          Testing
             +
       Data Validation
             +
          Security
             +
          Logging
             +
         Monitoring
             +
          Alerting
             +
        Performance
             +
          CI/CD
             +
           Docker
```

The goal is to build a pipeline that can **run repeatedly, handle problems, detect bad data, explain failures, protect secrets, and be safely deployed and maintained**.
