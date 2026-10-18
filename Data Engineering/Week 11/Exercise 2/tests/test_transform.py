import pandas as pd

from src.transform import transform_data


def test_transform_data():
    df = pd.DataFrame({
        "athlete_id": [1, 2, 3],
        "name": ["A", "B", "C"],
        "score": [95, 90, 70]
    })

    result = transform_data(df)

    assert "performance_level" in result.columns

    assert result.loc[0, "performance_level"] == "Excellent"
    assert result.loc[1, "performance_level"] == "Good"
    assert result.loc[2, "performance_level"] == "Average"