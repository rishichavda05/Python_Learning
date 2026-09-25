import boto3
from pathlib import Path


BUCKET_NAME = "my-data-engineering-s3-2026"
S3_FOLDER = "raw-data"
LOCAL_FOLDER = Path("data")


def upload_files():

    s3 = boto3.client("s3")

    for file_path in LOCAL_FOLDER.iterdir():

        if not file_path.is_file():
            continue

        s3_key = f"{S3_FOLDER}/{file_path.name}"

        try:

            s3.upload_file(
                str(file_path),
                BUCKET_NAME,
                s3_key
            )

            print(f"SUCCESS: {file_path.name}")

        except Exception as e:

            print(f"FAILED: {file_path.name}")
            print(f"Error: {e}")


if __name__ == "__main__":
    upload_files()