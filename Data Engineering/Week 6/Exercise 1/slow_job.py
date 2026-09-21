from pyspark.sql import SparkSession
from pyspark.sql.functions import sum

spark = SparkSession.builder \
    .appName("SlowSparkJob") \
    .master("local[*]") \
    .getOrCreate()

# Read orders
orders = spark.read.csv(
    "data/orders.csv",
    header=True,
    inferSchema=True
)

# Read customers
customers = spark.read.csv(
    "data/customers.csv",
    header=True,
    inferSchema=True
)

# Join large orders with customers
joined = orders.join(
    customers,
    orders.customer_id == customers.customer_id
)

# Filter after the join
filtered = joined.filter(
    joined.status == "Completed"
)

# Group and calculate total sales
result = filtered.groupBy(
    "country"
).agg(
    sum("amount").alias("total_sales")
)

result.show()

spark.stop()