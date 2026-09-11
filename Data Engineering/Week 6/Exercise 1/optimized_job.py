from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, broadcast

spark = SparkSession.builder \
    .appName("OptimizedSparkJob") \
    .master("local[*]") \
    .getOrCreate()

# Read only required columns
orders = spark.read.csv(
    "data/orders.csv",
    header=True,
    inferSchema=True
).select(
    "customer_id",
    "amount",
    "status"
)

# Filter early
orders = orders.filter(
    orders.status == "Completed"
)

# Read only required customer columns
customers = spark.read.csv(
    "data/customers.csv",
    header=True,
    inferSchema=True
).select(
    "customer_id",
    "country"
)

# Broadcast small customer table
joined = orders.join(
    broadcast(customers),
    "customer_id"
)

# Aggregate
result = joined.groupBy(
    "country"
).agg(
    sum("amount").alias("total_sales")
)

# Show execution plan
result.explain(True)

# Display result
result.show()

spark.stop()