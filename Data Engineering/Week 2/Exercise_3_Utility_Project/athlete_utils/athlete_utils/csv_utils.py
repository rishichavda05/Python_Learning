import csv


def read_csv(file_path):
    """Read a CSV file and return its rows."""
    
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        return list(reader)