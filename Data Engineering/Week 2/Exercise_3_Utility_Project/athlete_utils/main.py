from athlete_utils import (
    read_csv,
    write_json,
    get_current_datetime,
    file_exists,
)


# Check if CSV file exists
file_path = "athletes.csv"

if file_exists(file_path):
    print("CSV file exists!")

    # Read CSV
    athletes = read_csv(file_path)

    print(f"Total athletes: {len(athletes)}")

    # Save as JSON
    write_json(athletes, "athletes.json")

    print("JSON file created!")

else:
    print(f"File does not exist: {file_path}")


# Get current date/time
current_time = get_current_datetime()

print(f"Current time: {current_time}")