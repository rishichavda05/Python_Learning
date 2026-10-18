def transform_data(df):
    """
    Add performance level based on score.
    """

    df = df.copy()

    df["performance_level"] = df["score"].apply(
        lambda score:
        "Excellent" if score >= 95
        else "Good" if score >= 85
        else "Average"
    )

    return df