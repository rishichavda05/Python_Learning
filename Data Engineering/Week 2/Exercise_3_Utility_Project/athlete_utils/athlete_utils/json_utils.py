import json


def write_json(data, file_path):
    """Write Python data to a JSON file."""

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)