from pyspark.sql import SparkSession
import os
import time

spark = SparkSession.builder \
    .appName("CSVvsParquet") \
    .master("local[*]") \
    .getOrCreate()

csv_path = "data/athletes.csv"
parquet_path = "output/athletes_parquet"

# --------------------------------------------------
# 1. Read CSV
# --------------------------------------------------

start_time = time.time()

df_csv = spark.read.csv(
    csv_path,
    header=True,
    inferSchema=True
)

df_csv.count()

csv_read_time = time.time() - start_time

print("CSV Read Time:", csv_read_time, "seconds")


# --------------------------------------------------
# 2. Write Parquet
# --------------------------------------------------

start_time = time.time()

df_csv.write \
    .mode("overwrite") \
    .parquet(parquet_path)

parquet_write_time = time.time() - start_time

print("Parquet Write Time:", parquet_write_time, "seconds")


# --------------------------------------------------
# 3. Read Parquet
# --------------------------------------------------

start_time = time.time()

df_parquet = spark.read.parquet(parquet_path)

df_parquet.count()

parquet_read_time = time.time() - start_time

print("Parquet Read Time:", parquet_read_time, "seconds")


# --------------------------------------------------
# 4. Compare Schema
# --------------------------------------------------

print("\nCSV Schema:")
df_csv.printSchema()

print("\nParquet Schema:")
df_parquet.printSchema()


# --------------------------------------------------
# 5. Select Required Columns
# --------------------------------------------------

print("\nPlayers from India:")

df_parquet \
    .filter(df_parquet.country == "India") \
    .select(
        "player_name",
        "sport",
        "score"
    ) \
    .show()


# --------------------------------------------------
# 6. File Size
# --------------------------------------------------

def get_folder_size(path):
    total_size = 0

    for root, directories, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            total_size += os.path.getsize(filepath)

    return total_size


csv_size = os.path.getsize(csv_path)
parquet_size = get_folder_size(parquet_path)

print("\nFile Size Comparison")
print("--------------------")

print("CSV Size:", csv_size, "bytes")
print("Parquet Size:", parquet_size, "bytes")


spark.stop()