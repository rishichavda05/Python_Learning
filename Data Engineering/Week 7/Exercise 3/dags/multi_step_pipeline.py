from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def start_pipeline():
    print("Starting multi-step ETL pipeline")


def extract_customers():
    print("Extracting customers.csv")

    with open(
        r"/path/to/Exercise 3/data/customers.csv",
        "r"
    ) as file:
        data = file.read()

    print(data)


def extract_orders():
    print("Extracting orders.csv")

    with open(
        r"/path/to/Exercise 3/data/orders.csv",
        "r"
    ) as file:
        data = file.read()

    print(data)


def transform_customers():
    print("Transforming customer data")

    print("Customer data cleaned successfully")


def transform_orders():
    print("Transforming order data")

    print("Order data cleaned successfully")


def validate_data():
    print("Validating customer and order data")

    print("Validation completed successfully")


def load_data():
    print("Loading data into database")

    print("Data loaded successfully")


def generate_report():
    print("Generating final ETL report")

    print("ETL pipeline completed successfully")


with DAG(
    dag_id="multi_step_dependency_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["etl", "dependencies"],
) as dag:

    start = PythonOperator(
        task_id="start_pipeline",
        python_callable=start_pipeline,
    )

    extract_customers_task = PythonOperator(
        task_id="extract_customers",
        python_callable=extract_customers,
    )

    extract_orders_task = PythonOperator(
        task_id="extract_orders",
        python_callable=extract_orders,
    )

    transform_customers_task = PythonOperator(
        task_id="transform_customers",
        python_callable=transform_customers,
    )

    transform_orders_task = PythonOperator(
        task_id="transform_orders",
        python_callable=transform_orders,
    )

    validate = PythonOperator(
        task_id="validate_data",
        python_callable=validate_data,
    )

    load = PythonOperator(
        task_id="load_data",
        python_callable=load_data,
    )

    report = PythonOperator(
        task_id="generate_report",
        python_callable=generate_report,
    )

    # Dependencies

    start >> [extract_customers_task, extract_orders_task]

    extract_customers_task >> transform_customers_task
    extract_orders_task >> transform_orders_task

    [transform_customers_task, transform_orders_task] >> validate

    validate >> load >> report