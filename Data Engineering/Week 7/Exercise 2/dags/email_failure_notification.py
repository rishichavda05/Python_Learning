from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.smtp.operators.smtp import EmailOperator


def successful_task():
    print("Task completed successfully.")


def failed_task():
    raise Exception("Something went wrong!")


with DAG(
    dag_id="email_failure_notification",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["email", "failure"],
) as dag:

    success = PythonOperator(
        task_id="successful_task",
        python_callable=successful_task,
    )

    failure_email = EmailOperator(
        task_id="send_failure_email",
        to="rishichavda0501@gmail.com",
        subject="Airflow Task Failed",
        html_content="""
        <h2>Airflow Task Failed</h2>

        <p>Hello,</p>

        <p>An Airflow task has failed.</p>

        <p>
            <b>DAG:</b> email_failure_notification
        </p>

        <p>
            <b>Status:</b> Failed
        </p>

        <p>Please check the Airflow logs.</p>
        """,
        conn_id="smtp_default",
    )

    failed = PythonOperator(
        task_id="failed_task",
        python_callable=failed_task,
    )

    success >> failed >> failure_email