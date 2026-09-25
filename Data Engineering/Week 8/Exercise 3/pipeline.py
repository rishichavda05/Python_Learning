import os
import json
import boto3
import requests
import psycopg2

from dotenv import load_dotenv


# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()


API_URL = os.getenv("API_URL")

AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_KEY = os.getenv("S3_KEY")

REDSHIFT_HOST = os.getenv("REDSHIFT_HOST")
REDSHIFT_PORT = os.getenv("REDSHIFT_PORT")
REDSHIFT_DATABASE = os.getenv("REDSHIFT_DATABASE")
REDSHIFT_USER = os.getenv("REDSHIFT_USER")
REDSHIFT_PASSWORD = os.getenv("REDSHIFT_PASSWORD")
REDSHIFT_IAM_ROLE = os.getenv("REDSHIFT_IAM_ROLE")


# --------------------------------------------------
# 1. Extract Data from API
# --------------------------------------------------

def extract_from_api():

    print("Extracting data from API...")

    response = requests.get(API_URL, timeout=30)

    response.raise_for_status()

    data = response.json()

    print(f"Records received: {len(data)}")

    return data


# --------------------------------------------------
# 2. Upload Data to S3
# --------------------------------------------------

def upload_to_s3(data):

    print("Uploading data to S3...")

    s3 = boto3.client(
        "s3",
        region_name=AWS_REGION
    )

    json_data = json.dumps(data)

    s3.put_object(
        Bucket=S3_BUCKET,
        Key=S3_KEY,
        Body=json_data.encode("utf-8"),
        ContentType="application/json"
    )

    print(
        f"Uploaded to: s3://{S3_BUCKET}/{S3_KEY}"
    )


# --------------------------------------------------
# 3. Create Redshift Table
# --------------------------------------------------

def create_table():

    print("Creating Redshift table...")

    connection = psycopg2.connect(
        host=REDSHIFT_HOST,
        port=REDSHIFT_PORT,
        database=REDSHIFT_DATABASE,
        user=REDSHIFT_USER,
        password=REDSHIFT_PASSWORD
    )

    cursor = connection.cursor()

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER,
        name VARCHAR(100),
        username VARCHAR(100),
        email VARCHAR(150),
        city VARCHAR(100),
        phone VARCHAR(50),
        website VARCHAR(150)
    );
    """

    cursor.execute(create_table_sql)

    connection.commit()

    cursor.close()
    connection.close()

    print("Redshift table ready.")


# --------------------------------------------------
# 4. Load S3 Data into Redshift
# --------------------------------------------------

def load_into_redshift():

    print("Loading data from S3 into Redshift...")

    connection = psycopg2.connect(
        host=REDSHIFT_HOST,
        port=REDSHIFT_PORT,
        database=REDSHIFT_DATABASE,
        user=REDSHIFT_USER,
        password=REDSHIFT_PASSWORD
    )

    cursor = connection.cursor()

    s3_path = f"s3://{S3_BUCKET}/{S3_KEY}"

    copy_sql = f"""
    COPY users
    FROM '{s3_path}'
    IAM_ROLE '{REDSHIFT_IAM_ROLE}'
    FORMAT AS JSON 'auto'
    REGION '{AWS_REGION}';
    """

    cursor.execute(copy_sql)

    connection.commit()

    cursor.close()
    connection.close()

    print("Data loaded into Redshift.")


# --------------------------------------------------
# 5. Verify Data
# --------------------------------------------------

def verify_data():

    print("Checking Redshift data...")

    connection = psycopg2.connect(
        host=REDSHIFT_HOST,
        port=REDSHIFT_PORT,
        database=REDSHIFT_DATABASE,
        user=REDSHIFT_USER,
        password=REDSHIFT_PASSWORD
    )

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM users;"
    )

    count = cursor.fetchone()[0]

    print(f"Total records in Redshift: {count}")

    cursor.execute(
        """
        SELECT
            id,
            name,
            email,
            city
        FROM users
        LIMIT 10;
        """
    )

    rows = cursor.fetchall()

    print("\n===== SAMPLE DATA =====")

    for row in rows:
        print(row)

    cursor.close()
    connection.close()


# --------------------------------------------------
# Main Pipeline
# --------------------------------------------------

def main():

    print("\n==============================")
    print("API → S3 → REDSHIFT PIPELINE")
    print("==============================\n")

    try:

        # Extract
        data = extract_from_api()

        # Load raw data into S3
        upload_to_s3(data)

        # Create destination table
        create_table()

        # Load S3 → Redshift
        load_into_redshift()

        # Verify
        verify_data()

        print("\nPipeline completed successfully!")

    except Exception as e:

        print("\nPipeline failed.")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()