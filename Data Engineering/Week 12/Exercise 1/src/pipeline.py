import os
import logging
import pandas as pd


# -----------------------------
# Logging Configuration
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# -----------------------------
# Configuration
# -----------------------------
INPUT_FILE = os.getenv(
    "INPUT_FILE",
    "/app/data/sales.csv"
)

OUTPUT_FILE = os.getenv(
    "OUTPUT_FILE",
    "/app/output/processed_sales.csv"
)


# -----------------------------
# Extract
# -----------------------------
def extract_data():
    logger.info("Reading input data")

    df = pd.read_csv(INPUT_FILE)

    logger.info("Records loaded: %s", len(df))

    return df


# -----------------------------
# Transform
# -----------------------------
def transform_data(df):
    logger.info("Starting transformation")

    df["total_amount"] = df["quantity"] * df["price"]

    df = df.dropna()

    logger.info("Transformation completed")

    return df


# -----------------------------
# Load
# -----------------------------
def load_data(df):
    logger.info("Writing processed data")

    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    logger.info(
        "Output file created: %s",
        OUTPUT_FILE
    )


# -----------------------------
# Main Pipeline
# -----------------------------
def main():

    logger.info("Pipeline started")

    df = extract_data()

    df = transform_data(df)

    load_data(df)

    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    main()