# Data Ingestion

## 1. REST APIs

A REST API allows one application to get data from another application over the internet.

For example, a sports application may provide player data through an API.

Example API request:

```text
GET https://example.com/api/players
```

The API may return data like:

```json
{
    "player_id": 101,
    "name": "Rahul",
    "sport": "Cricket"
}
```

In Python, we can use the `requests` library:

```python
import requests

url = "https://example.com/api/players"

response = requests.get(url)

print(response.status_code)
print(response.json())
```

### Key Point

REST API is a common source from which data engineers collect data.

---

## 2. Pagination

Sometimes an API has a large amount of data.

Instead of returning everything at once, the API divides the data into multiple pages.

Example:

```text
Page 1 → Players 1-100
Page 2 → Players 101-200
Page 3 → Players 201-300
```

This is called **pagination**.

A simple API request may look like:

```text
https://example.com/api/players?page=1
```

Then:

```text
https://example.com/api/players?page=2
```

Python example:

```python
import requests

for page in range(1, 4):

    url = f"https://example.com/api/players?page={page}"

    response = requests.get(url)

    print(response.json())
```

### Key Point

Pagination helps us collect large amounts of API data without requesting everything in one request.

---

## 3. Authentication

Some APIs are public, while others require permission.

**Authentication** is the process of proving that we are allowed to access the API.

Common authentication methods are:

- API Key
- Bearer Token
- Username and Password
- OAuth

Example using a Bearer Token:

```python
import requests

url = "https://example.com/api/players"

headers = {
    "Authorization": "Bearer YOUR_TOKEN"
}

response = requests.get(
    url,
    headers=headers
)

print(response.json())
```

### Important

Never expose real API keys or tokens in your source code.

A better approach is to store secrets in environment variables.

```python
import os

token = os.getenv("API_TOKEN")
```

### Key Point

Authentication protects APIs and controls who can access the data.

---

## 4. CSV Ingestion

CSV stands for **Comma-Separated Values**.

CSV is a simple file format used to store tabular data.

Example `players.csv`:

```csv
player_id,name,sport,country
101,Rahul,Cricket,India
102,Arjun,Football,India
103,John,Tennis,USA
```

We can read a CSV file using pandas:

```python
import pandas as pd

df = pd.read_csv("players.csv")

print(df)
```

Output:

```text
   player_id    name     sport  country
0        101   Rahul   Cricket    India
1        102   Arjun  Football    India
2        103    John    Tennis      USA
```

We can check the number of records:

```python
print(len(df))
```

### Key Point

CSV ingestion means reading data from a CSV file and bringing it into our data pipeline.

---

## 5. Excel Ingestion

Excel files are commonly used to store business and other structured data.

Example file:

```text
players.xlsx
```

The data may look like:

| player_id | name | sport | country |
|---|---|---|---|
| 101 | Rahul | Cricket | India |
| 102 | Arjun | Football | India |
| 103 | John | Tennis | USA |

Using pandas:

```python
import pandas as pd

df = pd.read_excel("players.xlsx")

print(df)
```

If required, install the Excel library:

```bash
pip install openpyxl
```

### Key Point

Excel ingestion means reading data from an Excel file and bringing it into our data pipeline.

---

## 6. Database Ingestion

Data can also come from a database such as:

- PostgreSQL
- MySQL
- SQL Server
- Oracle

For example, a PostgreSQL table may contain:

```text
players

player_id | name   | sport    | country
----------|--------|----------|--------
101       | Rahul  | Cricket  | India
102       | Arjun  | Football | India
103       | John   | Tennis   | USA
```

We can use SQL to read the data:

```sql
SELECT *
FROM players;
```

Python can also read database data.

Example using pandas and SQLAlchemy:

```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://username:password@localhost:5432/sports_db"
)

query = "SELECT * FROM players"

df = pd.read_sql(query, engine)

print(df)
```

### Key Point

Database ingestion means reading data from a database and bringing it into the data pipeline.

---

## 7. Incremental Loading

**Incremental Loading** means loading only the new or changed data instead of loading everything.

Example:

Yesterday:

```text
Player 1
Player 2
Player 3
```

Today:

```text
Player 1
Player 2
Player 3
Player 4
Player 5
```

With incremental loading, we load only:

```text
Player 4
Player 5
```

A common way to identify new or changed records is using an `updated_at` column.

Example:

```text
player_id | name   | updated_at
----------|--------|-------------------
101       | Rahul  | 2026-08-28 10:00
102       | Arjun  | 2026-08-28 11:00
103       | John   | 2026-08-29 09:00
```

If the last successful load was:

```text
2026-08-28 11:00
```

we can select:

```sql
SELECT *
FROM players
WHERE updated_at > '2026-08-28 11:00:00';
```

This returns only the records that changed after the last load.

### Key Point

Incremental loading saves time and resources because we process only new or changed data.

---

## 8. Full Load

**Full Load** means loading all available data from the source.

Example:

```text
Source:

Player 1
Player 2
Player 3
Player 4
```

A full load copies:

```text
Player 1
Player 2
Player 3
Player 4
```

Every time a full load runs, it reads the complete dataset.

### When is Full Load Useful?

Full load is useful when:

- The dataset is small
- Data is being loaded for the first time
- We need a complete refresh
- Incremental loading is not available

### Full Load vs Incremental Loading

```text
Full Load

Source
  |
  |--- All Data
  |
  v
Target
```

```text
Incremental Load

Source
  |
  |--- New / Changed Data
  |
  v
Target
```

### Key Point

Full load means **load everything**.

---

## 9. CDC Concepts

CDC stands for **Change Data Capture**.

CDC is used to capture changes made to data.

The main types of changes are:

```text
INSERT
UPDATE
DELETE
```

Example:

Initial data:

```text
101 | Rahul | Cricket
102 | Arjun | Football
```

Later:

```text
INSERT → 103 | John | Tennis

UPDATE → 101 | Rahul | Cricket

DELETE → 102 | Arjun | Football
```

CDC identifies these changes so that they can be sent to another system.

Simple CDC flow:

```text
Source Database
       |
       v
   Detect Changes
       |
       +---- INSERT
       |
       +---- UPDATE
       |
       +---- DELETE
       |
       v
   Target System
```

### Key Point

CDC means **capturing changes in source data**.

---

## 10. JSON Parsing

JSON stands for **JavaScript Object Notation**.

JSON is commonly used by REST APIs.

Example:

```json
{
    "player_id": 101,
    "name": "Rahul",
    "sport": "Cricket"
}
```

In Python, we can access JSON values using keys:

```python
data = {
    "player_id": 101,
    "name": "Rahul",
    "sport": "Cricket"
}

print(data["player_id"])
print(data["name"])
print(data["sport"])
```

Output:

```text
101
Rahul
Cricket
```

JSON can also contain multiple records:

```json
[
    {
        "player_id": 101,
        "name": "Rahul"
    },
    {
        "player_id": 102,
        "name": "Arjun"
    }
]
```

We can loop through the records:

```python
players = [
    {
        "player_id": 101,
        "name": "Rahul"
    },
    {
        "player_id": 102,
        "name": "Arjun"
    }
]

for player in players:
    print(player["name"])
```

Output:

```text
Rahul
Arjun
```

### Key Point

JSON parsing means reading JSON data and extracting the information we need.

---

## 11. Schema Evolution

A **schema** describes the structure of data.

For example:

```text
player_id
name
sport
country
```

A schema also defines things such as data types:

```text
player_id → Integer
name      → String
sport     → String
country   → String
```

### What is Schema Evolution?

**Schema Evolution** means the structure of the data changes over time.

Initial data:

```json
{
    "player_id": 101,
    "name": "Rahul",
    "sport": "Cricket"
}
```

Later, the source adds a new field:

```json
{
    "player_id": 101,
    "name": "Rahul",
    "sport": "Cricket",
    "country": "India"
}
```

The schema has changed because:

```text
country
```

was added.

Another example:

Initial schema:

```text
player_id
name
sport
```

New schema:

```text
player_id
name
sport
country
age
```

A data pipeline needs to handle these changes safely.

### Key Point

Schema evolution means **the structure of source data changes over time**.
