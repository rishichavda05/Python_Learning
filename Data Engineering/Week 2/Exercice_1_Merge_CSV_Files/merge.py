import csv
from pathlib import Path


# Folder containing the CSV files
data_folder = Path("data")

# List to store all athlete records
all_athletes = []


# Find all CSV files
csv_files = data_folder.glob("*.csv")


# Read each CSV file
for file in csv_files:
    print(f"Reading: {file.name}")

    with open(file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            all_athletes.append(row)


# Create the merged CSV file
output_file = Path("merged_athletes.csv")

with open(output_file, "w", newline="", encoding="utf-8") as f:

    fieldnames = [
        "player_id",
        "player_name",
        "sport",
        "country",
        "performance_score"
    ]

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    # Write column names
    writer.writeheader()

    # Write all athlete records
    writer.writerows(all_athletes)


print(f"Total athletes: {len(all_athletes)}")
print("All CSV files merged successfully!")