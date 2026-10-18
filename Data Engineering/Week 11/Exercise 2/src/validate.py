def validate_data(df):
    """
    Validate athlete data.
    """

    if df["athlete_id"].isnull().any():
        raise ValueError("athlete_id contains NULL values")

    if df["athlete_id"].duplicated().any():
        raise ValueError("athlete_id contains duplicate values")

    if (df["age"] < 0).any():
        raise ValueError("age cannot be negative")

    if ((df["score"] < 0) | (df["score"] > 100)).any():
        raise ValueError("score must be between 0 and 100")

    return True