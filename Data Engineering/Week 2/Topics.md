# Python for Data Engineering Pipelines

# 1. File Handling --- CSV, JSON, XML

Data engineers constantly read and write files. CSV, JSON, and XML are
common formats for raw data, API responses, exports, and intermediate
pipeline files.

## 1.1 CSV

CSV means Comma-Separated Values. It is commonly used for tabular data.

Example file:

``` csv
id,name,age
1,Alice,25
2,Bob,30
3,Charlie,28
```

### Reading CSV

``` python
import csv

with open("users.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        print(row["name"], row["age"])
```

Output:

``` text
Alice 25
Bob 30
Charlie 28
```

### Writing CSV

``` python
import csv

users = [
    {"id": 1, "name": "Alice", "age": 25},
    {"id": 2, "name": "Bob", "age": 30},
]

with open("output.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["id", "name", "age"]
    )

    writer.writeheader()
    writer.writerows(users)
```

### Data engineering use

A pipeline might:

``` text
CSV from vendor
    ↓
Python ingestion
    ↓
Validation
    ↓
Transformation
    ↓
Database / Data Warehouse
```

------------------------------------------------------------------------

## 1.2 JSON

JSON is extremely common for APIs and configuration files.

Example:

``` json
{
  "id": 101,
  "name": "Alice",
  "skills": ["Python", "SQL"]
}
```

### Reading JSON

``` python
import json

with open("user.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print(data["name"])
print(data["skills"])
```

### Writing JSON

``` python
import json

data = {
    "id": 101,
    "name": "Alice",
    "skills": ["Python", "SQL"]
}

with open("output.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2)
```


## 1.3 XML

XML is older than JSON but is still used in enterprise systems, banking,
government systems, and legacy applications.

Example:

``` xml
<users>
    <user>
        <id>1</id>
        <name>Alice</name>
    </user>
    <user>
        <id>2</id>
        <name>Bob</name>
    </user>
</users>
```

### Reading XML

``` python
import xml.etree.ElementTree as ET

tree = ET.parse("users.xml")
root = tree.getroot()

for user in root.findall("user"):
    user_id = user.find("id").text
    name = user.find("name").text

    print(user_id, name)
```

### Data engineering idea

You should become comfortable converting:

``` text
CSV → Python objects
JSON → Python objects
XML → Python objects
```

and eventually:

``` text
Python objects → CSV
Python objects → JSON
Python objects → Database
```

------------------------------------------------------------------------

# 2. Logging

`print()` is useful while learning, but production pipelines should use
logging.

Logging helps you understand:

-   What the pipeline is doing
-   When a step started
-   When a step completed
-   How many records were processed
-   What failed
-   Why something failed

## Basic logging

``` python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Pipeline started")
logging.warning("Input file contains missing values")
logging.error("Database connection failed")
```

Example output:

``` text
2026-08-14 10:30:00 - INFO - Pipeline started
2026-08-14 10:30:01 - WARNING - Input file contains missing values
2026-08-14 10:30:02 - ERROR - Database connection failed
```

## Log levels

The common levels are:

``` text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

Typical pipeline usage:

``` python
logging.debug("API response received")
logging.info("Downloaded 5000 records")
logging.warning("10 records have missing emails")
logging.error("Failed to write output file")
logging.critical("Pipeline cannot continue")
```

## Logging to a file

``` python
logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("ETL job started")
```

### Data engineering example

``` python
def extract():
    logging.info("Starting extraction")

    # extraction code

    logging.info("Extraction completed")


def transform():
    logging.info("Starting transformation")

    # transformation code

    logging.info("Transformation completed")


def load():
    logging.info("Starting load")

    # loading code

    logging.info("Load completed")
```

This makes debugging scheduled jobs much easier.


------------------------------------------------------------------------

# 3. Error Handling

Pipelines fail for many reasons:

-   File does not exist
-   API is unavailable
-   Invalid data
-   Database connection fails
-   Permission problems
-   Unexpected data types

Python uses `try`, `except`, `else`, and `finally`.

## Basic example

``` python
try:
    number = int("abc")
except ValueError:
    print("Invalid number")
```

## Handling a file error

``` python
try:
    with open("users.csv", "r") as file:
        data = file.read()

except FileNotFoundError:
    print("Input file was not found")
```

## Multiple exceptions

``` python
try:
    value = int("abc")
except ValueError:
    print("Invalid integer")
except TypeError:
    print("Invalid type")
```

## `else`

`else` executes when no exception occurs.

``` python
try:
    number = int("100")
except ValueError:
    print("Invalid number")
else:
    print("Conversion successful")
```

## `finally`

`finally` runs regardless of whether an error occurred.

``` python
try:
    print("Processing")
except Exception as error:
    print(error)
finally:
    print("Cleanup completed")
```

## Log exceptions

In production code, prefer logging over only printing.

``` python
import logging

try:
    process_data()
except Exception:
    logging.exception("Data processing failed")
```

`logging.exception()` automatically includes traceback information.

## Avoid this

``` python
try:
    process_data()
except:
    pass
```

This hides failures and makes pipelines extremely difficult to debug.

Prefer:

``` python
try:
    process_data()
except Exception:
    logging.exception("Processing failed")
    raise
```

------------------------------------------------------------------------

# 4. Virtual Environment & Requirements

Different projects may require different versions of packages.

For example:

``` text
Project A → requests 2.x
Project B → another version
```

A virtual environment keeps project dependencies isolated.

## Create a virtual environment

``` bash
python -m venv .venv
```

## Activate on Windows

``` bash
.venv\Scripts\activate
```

## Activate on Linux/macOS

``` bash
source .venv/bin/activate
```

## Install a package

``` bash
pip install requests
```

## Check installed packages

``` bash
pip list
```

## Create requirements.txt

``` bash
pip freeze > requirements.txt
```

Example:

``` text
requests==2.x.x
```

## Install dependencies from requirements.txt

``` bash
pip install -r requirements.txt
```

### Typical project structure

``` text
data-pipeline/
│
├── .venv/
├── src/
│   └── pipeline.py
├── data/
├── logs/
├── requirements.txt
└── README.md
```

Do not normally commit `.venv/` to Git.


------------------------------------------------------------------------

# 5. Typing

Type hints make code easier to understand and maintain.

They are especially useful in larger data pipelines.

## Basic typing

``` python
def add(a: int, b: int) -> int:
    return a + b
```

This tells readers and development tools:

``` text
a → int
b → int
return → int
```

## String example

``` python
def clean_name(name: str) -> str:
    return name.strip().title()
```

## Lists

``` python
def total(values: list[int]) -> int:
    return sum(values)
```

## Dictionary

``` python
def get_user() -> dict[str, str]:
    return {
        "name": "Alice",
        "city": "Ahmedabad"
    }
```

## Optional values

``` python
def find_user(user_id: int) -> str | None:
    if user_id == 1:
        return "Alice"

    return None
```

## Why typing matters in pipelines

Consider:

``` python
def transform(data):
    ...
```

It is unclear what `data` contains.

Compare:

``` python
def transform(data: list[dict[str, object]]) -> list[dict[str, object]]:
    ...
```

The second version communicates much more information.


------------------------------------------------------------------------

# 6. Datetime

Data pipelines frequently work with:

-   Event timestamps
-   File timestamps
-   Partition dates
-   Job start/end times
-   Incremental loading
-   Data freshness

Use Python's `datetime` module.

## Current datetime

``` python
from datetime import datetime

now = datetime.now()

print(now)
```

## Current UTC time

For many distributed systems, UTC is preferable.

``` python
from datetime import datetime, timezone

now = datetime.now(timezone.utc)

print(now)
```

## Create a datetime

``` python
from datetime import datetime

dt = datetime(2026, 8, 14, 10, 30, 0)

print(dt)
```

## Formatting

``` python
formatted = dt.strftime("%Y-%m-%d %H:%M:%S")

print(formatted)
```

Output:

``` text
2026-08-14 10:30:00
```

Useful format codes:

``` text
%Y → year
%m → month
%d → day
%H → hour
%M → minute
%S → second
```

## Parsing a string

``` python
from datetime import datetime

text = "2026-08-14 10:30:00"

dt = datetime.strptime(
    text,
    "%Y-%m-%d %H:%M:%S"
)

print(dt)
```

## Date arithmetic

``` python
from datetime import datetime, timedelta

today = datetime.now()

yesterday = today - timedelta(days=1)

print(yesterday)
```

## Pipeline example

Suppose a pipeline loads yesterday's data:

``` python
from datetime import datetime, timedelta

today = datetime.now().date()
yesterday = today - timedelta(days=1)

print(f"Loading data for {yesterday}")
```


------------------------------------------------------------------------

# 7. Generators

Generators are very useful when processing large datasets.

A normal function may create a large list in memory.

A generator produces values one at a time.

## Normal list

``` python
def get_numbers():
    return [1, 2, 3, 4, 5]
```

The entire list exists in memory.

## Generator

``` python
def get_numbers():
    for number in range(1, 6):
        yield number
```

Use it:

``` python
for number in get_numbers():
    print(number)
```

## Why generators matter in data engineering

Imagine a file contains:

``` text
10 million rows
```

This can be memory-heavy:

``` python
rows = list(read_all_rows())
```

A generator can process one row at a time:

``` python
for row in read_rows():
    process(row)
```

## Reading a large file

``` python
def read_file(path: str):
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            yield line.strip()
```

Then:

``` python
for line in read_file("large_file.txt"):
    print(line)
```

Only the current line needs to be processed.

## Generator expression

``` python
squares = (x * x for x in range(1_000_000))
```

Values are generated as needed.


------------------------------------------------------------------------

# 8. Context Managers

You have already seen this:

``` python
with open("data.txt") as file:
    data = file.read()
```

The `with` statement is using a context manager.

A context manager handles setup and cleanup automatically.

## Why it matters

Without a context manager:

``` python
file = open("data.txt")
data = file.read()
file.close()
```

If an exception occurs before `file.close()`, the file may not be
cleaned up correctly.

With:

``` python
with open("data.txt") as file:
    data = file.read()
```

Python handles cleanup.

## Database-style example

Conceptually:

``` python
with database_connection() as connection:
    connection.execute(...)
```

The connection can be cleaned up automatically.

## Creating your own context manager

``` python
from contextlib import contextmanager

@contextmanager
def pipeline_step(name: str):
    print(f"Starting {name}")

    try:
        yield
    finally:
        print(f"Finished {name}")
```

Use it:

``` python
with pipeline_step("transform"):
    print("Transforming data")
```

### Pipeline use

Context managers are useful for resources such as:

-   Files
-   Database connections
-   Locks
-   Temporary resources
-   Network resources

------------------------------------------------------------------------

# 9. Requests Library

The `requests` library is commonly used to call HTTP APIs.

Install it:

``` bash
pip install requests
```

## GET request

``` python
import requests

response = requests.get(
    "https://api.example.com/users",
    timeout=10
)

print(response.status_code)
print(response.text)
```

## JSON response

``` python
response = requests.get(
    "https://api.example.com/users",
    timeout=10
)

data = response.json()

print(data)
```

## Check for HTTP errors

``` python
response = requests.get(
    "https://api.example.com/users",
    timeout=10
)

response.raise_for_status()

data = response.json()
```

If the server returns an HTTP error, `raise_for_status()` raises an
exception.

## Query parameters

Instead of manually creating a URL:

``` python
params = {
    "page": 1,
    "limit": 100
}

response = requests.get(
    "https://api.example.com/users",
    params=params,
    timeout=10
)
```

## Headers

``` python
headers = {
    "Authorization": "Bearer TOKEN"
}

response = requests.get(
    "https://api.example.com/users",
    headers=headers,
    timeout=10
)
```

Do not hard-code real API secrets in source code.

Use environment variables instead.

## POST request

``` python
payload = {
    "name": "Alice",
    "age": 25
}

response = requests.post(
    "https://api.example.com/users",
    json=payload,
    timeout=10
)

response.raise_for_status()
```

## API ingestion pattern

A typical pipeline:

``` text
API
 ↓
requests.get()
 ↓
JSON response
 ↓
Validation
 ↓
Transformation
 ↓
Storage
```


------------------------------------------------------------------------

# 10. Pathlib

`pathlib` provides a cleaner way to work with filesystem paths.

Instead of:

``` python
import os

path = os.path.join("data", "raw", "users.csv")
```

Use:

``` python
from pathlib import Path

path = Path("data") / "raw" / "users.csv"
```

## Check whether a file exists

``` python
from pathlib import Path

path = Path("data/users.csv")

if path.exists():
    print("File exists")
```

## Check whether it is a file

``` python
if path.is_file():
    print("This is a file")
```

## Read a file

``` python
content = path.read_text(encoding="utf-8")
```

## Write a file

``` python
path.write_text(
    "hello",
    encoding="utf-8"
)
```

## Create directories

``` python
output_dir = Path("data/output")

output_dir.mkdir(
    parents=True,
    exist_ok=True
)
```

## Find files

``` python
data_dir = Path("data")

for file in data_dir.glob("*.csv"):
    print(file)
```

## Pipeline example

``` python
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True
)

for file in RAW_DIR.glob("*.csv"):
    print(f"Processing {file}")
```

# 11. Config Files

A pipeline often needs configuration such as:

``` text
API URL
database host
batch size
input directory
output directory
```

Instead of hard-coding everything:

``` python
API_URL = "https://api.example.com"
BATCH_SIZE = 100
```

you can use a configuration file.

## JSON configuration

Example `config.json`:

``` json
{
  "api_url": "https://api.example.com",
  "batch_size": 100,
  "input_dir": "data/raw",
  "output_dir": "data/processed"
}
```

Read it:

``` python
import json

with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

print(config["api_url"])
print(config["batch_size"])
```

## Config object

You can make configuration easier to use:

``` python
from dataclasses import dataclass

@dataclass
class Config:
    api_url: str
    batch_size: int
    input_dir: str
    output_dir: str
```

Then:

``` python
config = Config(
    api_url="https://api.example.com",
    batch_size=100,
    input_dir="data/raw",
    output_dir="data/processed"
)
```

### Configuration principle

Keep **configuration separate from code**.

Code:

``` python
def extract(config):
    response = requests.get(
        config.api_url,
        timeout=10
    )
```

Configuration:

``` text
api_url = ...
```

This makes the same code easier to run in:

``` text
Development
Testing
Production
```

------------------------------------------------------------------------

# 12. Environment Variables

Environment variables are especially important for secrets and
environment-specific settings.

Examples:

``` text
API_KEY
DATABASE_HOST
DATABASE_USER
DATABASE_PASSWORD
ENVIRONMENT
```

Do not put passwords or API keys directly into source code.

Bad:

``` python
API_KEY = "my-secret-key"
```

Better:

``` python
import os

API_KEY = os.getenv("API_KEY")
```

## Set an environment variable

Linux/macOS:

``` bash
export API_KEY="my-secret-key"
```

Windows PowerShell:

``` powershell
$env:API_KEY="my-secret-key"
```

Then:

``` python
import os

api_key = os.getenv("API_KEY")

print(api_key)
```

## Required environment variable

Sometimes you want the program to fail immediately if a variable is
missing.

``` python
import os

api_key = os.environ["API_KEY"]
```

If `API_KEY` does not exist, Python raises a `KeyError`.

## Default value

``` python
environment = os.getenv(
    "ENVIRONMENT",
    "development"
)

print(environment)
```

## `.env` files

During local development, you may use a `.env` file with a library such
as `python-dotenv`.

Example:

``` text
API_KEY=my-secret-key
DATABASE_HOST=localhost
DATABASE_USER=data_user
```

Install:

``` bash
pip install python-dotenv
```

Load:

``` python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")
```

Do not commit secrets to Git. Add `.env` to `.gitignore`.


------------------------------------------------------------------------

# 13. Putting Everything Together

Now combine the concepts into one small data pipeline.

## Project structure

``` text
python-pipeline/
│
├── .venv/
├── data/
│   ├── raw/
│   └── processed/
│
├── logs/
│   └── pipeline.log
│
├── config.json
├── .env
├── requirements.txt
└── pipeline.py
```

## Example pipeline

``` python
import csv
import json
import logging
import os
from pathlib import Path
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv


# -------------------------
# Configuration
# -------------------------

load_dotenv()

API_KEY = os.getenv("API_KEY")
INPUT_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/processed")

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# -------------------------
# Logging
# -------------------------

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# -------------------------
# Extract
# -------------------------

def extract_from_csv(path: Path):
    logging.info("Reading file: %s", path)

    with path.open(
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            yield row


# -------------------------
# Transform
# -------------------------

def transform(rows):
    for row in rows:
        row["name"] = row["name"].strip().title()
        row["age"] = int(row["age"])

        yield row


# -------------------------
# Load
# -------------------------

def load_to_json(rows, output_path: Path):
    logging.info("Writing output: %s", output_path)

    data = list(rows)

    with output_path.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=2
        )


# -------------------------
# Pipeline
# -------------------------

def run_pipeline():
    start_time = datetime.now(timezone.utc)

    logging.info(
        "Pipeline started at %s",
        start_time
    )

    try:
        input_file = INPUT_DIR / "users.csv"

        rows = extract_from_csv(input_file)

        transformed_rows = transform(rows)

        output_file = OUTPUT_DIR / "users.json"

        load_to_json(
            transformed_rows,
            output_file
        )

        logging.info("Pipeline completed successfully")

    except Exception:
        logging.exception("Pipeline failed")
        raise


if __name__ == "__main__":
    run_pipeline()
```


------------------------------------------------------------------------

# Questions to Practice

After learning these topics, you should be able to answer:

### File handling

-   How do you read a large CSV without loading everything into memory?
-   What is the difference between `json.load()` and `json.loads()`?
-   When might XML still be used?

### Logging

-   Why is logging better than `print()` in production?
-   What are the common logging levels?
-   How would you log an exception traceback?

### Error handling

-   What is the difference between `except Exception` and a specific
    exception?
-   When would you use `finally`?
-   Why is `except: pass` dangerous?

### Virtual environments

-   Why do we use virtual environments?
-   What is `requirements.txt`?
-   How do you recreate another developer's environment?

### Typing

-   Why use type hints?
-   What does `-> list[int]` mean?
-   How do you represent a value that can be `None`?

### Datetime

-   Why is UTC commonly used in data systems?
-   How do you parse a timestamp string?
-   How do you calculate yesterday's date?

### Generators

-   What is `yield`?
-   Why are generators useful for large datasets?
-   What is the memory difference between a list and a generator?

### Context managers

-   Why do we use `with open(...)`?
-   What problem does a context manager solve?
-   How can you create a custom context manager?

### Requests

-   How do you call a REST API?
-   Why should you use a timeout?
-   What does `raise_for_status()` do?
-   How should API secrets be stored?

### Pathlib

-   Why use `Path` instead of manually building strings?
-   How do you find all CSV files in a directory?
-   How do you create a directory safely?

### Configuration

-   Why separate configuration from application code?
-   What belongs in a config file?
-   What should not be stored directly in source code?

### Environment variables

-   What are environment variables used for?
-   Why should secrets not be committed to Git?
-   What is the difference between `os.getenv()` and `os.environ[]`?

------------------------------------------------------------------------
