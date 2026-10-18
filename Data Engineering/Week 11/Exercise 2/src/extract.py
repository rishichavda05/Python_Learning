import pandas as pd


def extract_data(file_path):
    """
    Read athlete data from a CSV file.
    """
    df = pd.read_csv(file_path)

    return df