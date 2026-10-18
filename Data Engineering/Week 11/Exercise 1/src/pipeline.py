import pandas as pd
import os


INPUT_FILE = "data/athletes.csv"
OUTPUT_FILE = "data/processed_athletes.csv"


def load_data():
    print("Loading athlete data...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Records loaded: {len(df)}")

    return df


def validate_data(df):
    print("Validating data...")

    # Remove records with missing athlete_id
    df = df.dropna(subset=["athlete_id"])

    # Remove invalid ages
    df = df[df["age"] >= 0]

    # Remove invalid scores
    df = df[(df["score"] >= 0) & (df["score"] <= 100)]

    print(f"Records after validation: {len(df)}")

    return df


def transform_data(df):
    print("Transforming data...")

    df["performance_level"] = df["score"].apply(
        lambda score:
        "Excellent" if score >= 95
        else "Good" if score >= 85
        else "Average"
    )

    return df


def save_data(df):
    print("Saving processed data...")

    os.makedirs("data", exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Output saved to: {OUTPUT_FILE}")


def main():
    print("================================")
    print("Athlete ETL Pipeline Started")
    print("================================")

    df = load_data()

    df = validate_data(df)

    df = transform_data(df)

    save_data(df)

    print("================================")
    print("Pipeline completed successfully")
    print("================================")


if __name__ == "__main__":
    main()