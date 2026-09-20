# Apache Airflow – Production ETL Workflows

## Goal

Build production ETL workflows using Apache Airflow.

## Topics

1. DAG
2. Tasks
3. Operators
4. Scheduling
5. Dependencies
6. Retry
7. XCom
8. Variables
9. Connections
10. Sensors
11. Task Groups
12. Dynamic DAGs

---

# 1. DAG

**DAG (Directed Acyclic Graph)** is the main structure used in Airflow to define a workflow.

A DAG contains:

- Tasks
- Dependencies
- Schedule
- Retry settings

### Example

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extract_data():
    print("Extracting data")

with DAG(
    dag_id="simple_etl",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False
) as dag:

    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_data
    )
```

Think of a DAG as the **complete ETL workflow**.

---

# 2. Tasks

A **Task** is one individual unit of work inside a DAG.

For example:

```text
Extract Data
     ↓
Transform Data
     ↓
Load Data
```

Each step can be a separate task.

### Example

```python
extract = PythonOperator(
    task_id="extract",
    python_callable=extract_data
)
```

Here:

- `extract` → Python variable
- `task_id="extract"` → Airflow task name
- `python_callable=extract_data` → function executed by the task

---

# 3. Operators

An **Operator** defines what a task should do.

Common operators include:

| Operator | Purpose |
|---|---|
| `PythonOperator` | Run Python code |
| `BashOperator` | Run shell commands |
| `EmailOperator` | Send email |
| `SQLExecuteQueryOperator` | Execute SQL |
| `HttpOperator` | Call an API |

### PythonOperator

```python
from airflow.operators.python import PythonOperator

def transform_data():
    print("Transforming data")

transform = PythonOperator(
    task_id="transform",
    python_callable=transform_data
)
```

### BashOperator

```python
from airflow.operators.bash import BashOperator

task = BashOperator(
    task_id="run_command",
    bash_command="echo 'Hello Airflow'"
)
```

Operators are used to **create tasks**.

---

# 4. Scheduling

Scheduling determines **when a DAG should run**.

Common schedules:

```python
schedule="@daily"
```

```python
schedule="@hourly"
```

```python
schedule="@weekly"
```

You can also use cron expressions.

### Example

```python
schedule="0 6 * * *"
```

This means:

```text
Every day at 06:00
```

### Common Presets

| Schedule | Meaning |
|---|---|
| `@hourly` | Every hour |
| `@daily` | Every day |
| `@weekly` | Every week |
| `@monthly` | Every month |

---

# 5. Dependencies

Dependencies define the **order in which tasks run**.

Example:

```text
Extract → Transform → Load
```

In Airflow:

```python
extract >> transform >> load
```

This means:

```text
extract must finish
        ↓
transform runs
        ↓
load runs
```

You can also use:

```python
transform.set_upstream(extract)
```

The `>>` syntax is the most commonly used approach.

---

# 6. Retry

Sometimes a task fails because of a temporary problem.

For example:

- Database temporarily unavailable
- API timeout
- Network problem

Airflow can automatically retry the task.

### Example

```python
from datetime import timedelta

task = PythonOperator(
    task_id="load_data",
    python_callable=load_data,
    retries=3,
    retry_delay=timedelta(minutes=5)
)
```

This means:

```text
Task fails
   ↓
Wait 5 minutes
   ↓
Retry
   ↓
If it fails again → retry
   ↓
Maximum 3 retries
```

Retries are useful for handling **temporary failures**.

---

# 7. XCom

**XCom (Cross-Communication)** allows tasks to exchange small pieces of information.

Example:

```text
Task A
  ↓
customer_count = 100
  ↓
Task B
```

### Push value

```python
def extract_data(**context):
    context["ti"].xcom_push(
        key="customer_count",
        value=100
    )
```

### Pull value

```python
def process_data(**context):
    count = context["ti"].xcom_pull(
        task_ids="extract",
        key="customer_count"
    )

    print(count)
```

XCom is useful for passing **small values between tasks**.

Do not use XCom for large datasets or files.

---

# 8. Variables

Airflow Variables store **configuration values** that may change without modifying DAG code.

For example:

```text
API_URL
ENVIRONMENT
FILE_PATH
```

### Get a Variable

```python
from airflow.models import Variable

api_url = Variable.get("api_url")

print(api_url)
```

You can create a variable in the Airflow UI.

Example:

```text
Key: api_url
Value: https://example.com/api
```

Variables are useful for **configuration**, not for storing large data.

---

# 9. Connections

Connections store information required to connect to external systems.

Examples:

- PostgreSQL
- MySQL
- AWS
- APIs
- FTP
- Other databases

A connection can contain:

```text
Connection ID
Host
Username
Password
Port
Database
```

For example:

```text
Connection ID: postgres_default
Host: localhost
Port: 5432
Database: sales_db
```

Airflow operators/hooks can use the connection.

Example:

```python
from airflow.providers.postgres.hooks.postgres import PostgresHook

hook = PostgresHook(
    postgres_conn_id="postgres_default"
)

connection = hook.get_conn()
```

Connections help keep **credentials outside the DAG code**.

---

# 10. Sensors

A **Sensor** waits for something to happen before allowing a task to continue.

Examples:

```text
Wait for a file
Wait for another DAG
Wait for a database record
Wait for a specific time
```

Example:

```python
from airflow.providers.standard.sensors.filesystem import FileSensor

wait_for_file = FileSensor(
    task_id="wait_for_file",
    filepath="/data/sales.csv",
    poke_interval=60,
    timeout=3600
)
```

The sensor checks for the file.

```text
File does not exist
        ↓
      Wait
        ↓
     Check again
        ↓
File exists
        ↓
Continue workflow
```

Sensors are useful when your pipeline depends on an **external event**.

---

# 11. Task Groups

Task Groups allow you to organize related tasks together in the Airflow UI.

For example:

```text
ETL DAG
│
├── Extract
│   ├── Extract Customers
│   └── Extract Orders
│
├── Transform
│   ├── Clean Customers
│   └── Clean Orders
│
└── Load
    ├── Load Customers
    └── Load Orders
```

### Example

```python
from airflow.utils.task_group import TaskGroup

with TaskGroup("extract_group") as extract_group:

    extract_customers = PythonOperator(
        task_id="customers",
        python_callable=extract_customers_data
    )

    extract_orders = PythonOperator(
        task_id="orders",
        python_callable=extract_orders_data
    )
```

Task Groups are mainly used to make **large DAGs easier to understand and manage**.

---

# 12. Dynamic DAGs

Dynamic DAGs allow you to create tasks based on changing information.

For example, suppose you have:

```text
customers
orders
products
payments
```

Instead of manually creating four tasks, you can generate tasks dynamically.

### Example

```python
tables = [
    "customers",
    "orders",
    "products",
    "payments"
]

for table in tables:

    task = PythonOperator(
        task_id=f"process_{table}",
        python_callable=process_table,
        op_kwargs={"table": table}
    )
```

Airflow creates:

```text
process_customers
process_orders
process_products
process_payments
```

Dynamic task creation is useful when the number of similar tasks can change.

---

# Simple Production ETL Example

The concepts above can be combined into one workflow:

```text
                 DAG
                  │
                  ▼
           Wait for File
              Sensor
                  │
                  ▼
             Extract
               Task
                  │
                  ▼
            Transform
               Task
                  │
                  ▼
               Load
               Task
                  │
                  ▼
          PostgreSQL
```

Example dependency:

```python
wait_for_file >> extract >> transform >> load
```

The workflow can also include:

- **Scheduling** → Run every day
- **Retry** → Retry failed tasks
- **XCom** → Pass small values between tasks
- **Variables** → Store configuration
- **Connections** → Store database/API connection details
- **Task Groups** → Organize tasks
- **Dynamic DAGs** → Create tasks dynamically

---

# Quick Revision

| Topic | What it does |
|---|---|
| DAG | Defines the complete workflow |
| Task | Individual unit of work |
| Operator | Defines what a task does |
| Scheduling | Determines when the DAG runs |
| Dependencies | Defines task execution order |
| Retry | Re-runs failed tasks |
| XCom | Passes small values between tasks |
| Variables | Stores configuration |
| Connections | Stores connection information |
| Sensors | Waits for an external condition |
| Task Groups | Organizes related tasks |
| Dynamic DAGs | Creates tasks dynamically |

---

# Key Idea

Think of Airflow like this:

```text
DAG
 │
 ├── Tasks
 │    └── Operators
 │
 ├── Scheduling
 │
 ├── Dependencies
 │
 ├── Retry
 │
 ├── XCom
 │
 ├── Variables
 │
 ├── Connections
 │
 ├── Sensors
 │
 ├── Task Groups
 │
 └── Dynamic DAGs
```

The main goal of Airflow is to **define, schedule, monitor, and manage data workflows reliably**.
