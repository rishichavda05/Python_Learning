import requests
import json


# API URL
url = "https://jsonplaceholder.typicode.com/users"


# Send GET request
response = requests.get(url)


# Check if request was successful
response.raise_for_status()


# Convert response to Python data
data = response.json()


# Save data as JSON file
with open("athletes.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)


print("API data saved successfully!")