# Hands-on Exercise 3: Clean Messy Customer Dataset

## Goal

Work with a larger, realistic-looking customer dataset and practice data cleaning.

This exercise contains **50,500 rows** after adding duplicate records. The dataset intentionally contains messy values.

## Files

- `messy_customers.csv` - Large raw customer dataset
- `clean_customers.py` - Python solution
- `README.md` - Exercise instructions

## Messy Data Included

The dataset contains examples of:

- Extra spaces
- Uppercase/lowercase inconsistencies
- Missing emails
- Missing phone numbers
- Missing ages
- Missing income
- Invalid ages
- Invalid income values
- Duplicate customers
- Inconsistent formatting

## Tasks

### 1. Load the Dataset

```python
df = pd.read_csv("messy_customers.csv")
```

Check:

```python
df.shape
df.head()
df.info()
```

### 2. Find Missing Values

```python
df.isnull().sum()
```

Identify which columns contain missing data.

### 3. Clean Text

Remove unnecessary spaces from text columns.

```python
df["customer_name"] = df["customer_name"].str.strip()
```

### 4. Standardize Values

Make names and emails consistent.

Examples:

```python
df["customer_name"] = df["customer_name"].str.title()
df["email"] = df["email"].str.lower()
```

### 5. Handle Invalid Values

Find invalid ages and incomes.

Example:

```python
df.loc[(df["age"] < 18) | (df["age"] > 100), "age"] = pd.NA
```

### 6. Handle Missing Values

Use a suitable strategy for numeric columns.

Example:

```python
df["age"] = df["age"].fillna(df["age"].median())
```

### 7. Remove Duplicates

Remove duplicate customers using `customer_id`.

```python
df = df.drop_duplicates(subset=["customer_id"])
```

### 8. Feature Engineering

Create an `income_category` column:

- Low
- Medium
- High
- Very High

### 9. Save the Clean Dataset

```python
df.to_csv("cleaned_customers.csv", index=False)
```

## Run

Install Pandas if required:

```powershell
pip install pandas
```

Run:

```powershell
py .\clean_customers.py
```

## Expected Result

Input:

```text
messy_customers.csv
```

Output:

```text
cleaned_customers.csv
```

The output should have:

- Clean customer names
- Standardized emails
- Valid ages
- Valid incomes
- Missing numeric values handled
- Duplicate customers removed
- New `income_category` feature

## Challenge

After completing the basic exercise, try these yourself:

1. Find customers from each city.
2. Calculate average income by city.
3. Count customers by segment.
4. Find the top 10 customers by income.
5. Calculate the number of customers in each income category.

## Learning Outcome

You should become comfortable cleaning a relatively large CSV before moving the same type of cleaning logic to PySpark.

The main workflow is:

```text
Large Raw Dataset
       |
       v
Inspect
       |
       v
Clean Text
       |
       v
Handle Missing Values
       |
       v
Fix Invalid Values
       |
       v
Remove Duplicates
       |
       v
Feature Engineering
       |
       v
Clean Customer Dataset
```
