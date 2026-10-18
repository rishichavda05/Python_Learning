import pandas as pd

from src.validate import validate_data


def test_valid_data():
    df = pd.DataFrame({
        "athlete_id": [1, 2, 3],
        "age": [25, 30, 35],
        "score": [90, 95, 88]
    })

    assert validate_data(df) is True