from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import csv



def extract_data():
    with open("/data/sales.csv", "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            print(row)


def transform_data():
    sales = [
        {
            "order_id": 1,
            "customer": "Rahul",
            "product": "Laptop",
            "quantity": 1,
            "price": 55000
        }
    ]

    for sale in sales:
        sale["total_amount"] = (
            sale["quantity"] * sale["price"]
        )

    print(sales)


def load_data():
    print("Loading data into PostgreSQL")


with DAG(
    dag_id="daily_sales_etl",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={
        "retries": 2
    }
) as dag:

    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_data
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=transform_data
    )

    load = PythonOperator(
        task_id="load",
        python_callable=load_data
    )

    extract >> transform >> load