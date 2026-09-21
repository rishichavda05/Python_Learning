import requests
import json

url = "https://api.github.com/repos/rishichavda05/Python_Learning/contents"

response = requests.get(url)

if response.status_code == 200:

    data = response.json()

    print("API request successful")
    print("Files/Folders:\n")

    for item in data:
        print(
            item["name"],
            "-",
            item["type"]
        )

    with open("github_files.json", "w") as file:
        json.dump(data, file, indent=4)

    print("\nData saved to github_files.json")

else:
    print("API request failed")
    print("Status code:", response.status_code)
