from src.extract import extract_data
from src.transform import transform_data
from src.validate import validate_data
from src.load import load_data


INPUT_FILE = "data/athletes.csv"
OUTPUT_FILE = "data/processed_athletes.csv"


def run_pipeline():
    print("Pipeline started")

    # Extract
    df = extract_data(INPUT_FILE)

    print(f"Records extracted: {len(df)}")

    # Validate
    validate_data(df)

    print("Validation successful")

    # Transform
    df = transform_data(df)

    print("Transformation successful")

    # Load
    load_data(df, OUTPUT_FILE)

    print("Data loaded successfully")

    print("Pipeline completed")


if __name__ == "__main__":
    run_pipeline()