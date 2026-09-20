from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.smtp.operators.smtp import EmailOperator


def process_data():
    print("Starting data processing...")

    with open("D:\Data Engineering\Week 7\Exercise 2\data\input.txt", "r") as file:
        data = file.read()

    print("Data:")
    print(data)

    print("Data processing completed successfully.")


with DAG(
    dag_id="email_notification",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["email", "notification"],
) as dag:

    process = PythonOperator(
        task_id="process_data",
        python_callable=process_data,
    )

    send_email = EmailOperator(
        task_id="send_email",
        to="rishichavda0501@gmail.com",
        subject="Airflow ETL Completed",
        html_content="""
        <h2>ETL Pipeline Completed</h2>

        <p>Hello,</p>

        <p>The daily ETL pipeline completed successfully.</p>

        <p>
            <b>DAG:</b> email_notification
        </p>

        <p>
            <b>Status:</b> Success
        </p>

        <p>Regards,<br>Airflow</p>
        """,
        conn_id="smtp_default",
    )

    process >> send_email