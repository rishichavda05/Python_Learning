from src.extract import extract_data


def test_extract_data():
    df = extract_data("data/athletes.csv")

    assert len(df) == 10
    assert "athlete_id" in df.columns
    assert "name" in df.columns
    assert "sport" in df.columns
    assert "age" in df.columns
    assert "score" in df.columns