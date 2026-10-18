import pandas as pd


def validate_data(df):

    errors = []

    # Check 1: NULL athlete_id
    if df["athlete_id"].isnull().any():
        errors.append("athlete_id contains NULL values")

    # Check 2: Duplicate athlete_id
    if df["athlete_id"].duplicated().any():
        errors.append("athlete_id contains duplicate values")

    # Check 3: Invalid age
    if (df["age"] < 0).any():
        errors.append("age contains negative values")

    # Check 4: Invalid score
    if ((df["score"] < 0) | (df["score"] > 100)).any():
        errors.append("score must be between 0 and 100")

    return errors


def main():

    print("Reading athlete data...")

    df = pd.read_csv("data/athletes.csv")

    print(f"Total records: {len(df)}")

    errors = validate_data(df)

    print("\nData Quality Result")
    print("-------------------")

    if errors:
        print("❌ Data validation FAILED\n")

        for error in errors:
            print(f"- {error}")

    else:
        print("✅ Data validation PASSED")


if __name__ == "__main__":
    main()