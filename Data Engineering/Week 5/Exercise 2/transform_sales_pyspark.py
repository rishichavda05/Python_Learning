from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, sum

# 1. Create Spark session
spark = SparkSession.builder \
    .appName("SalesTransformation") \
    .getOrCreate()

# 2. Read CSV files
orders = spark.read.csv(
    "orders.csv",
    header=True,
    inferSchema=True
)

products = spark.read.csv(
    "products.csv",
    header=True,
    inferSchema=True
)

print("Orders:")
orders.show()

print("Products:")
products.show()

# 3. Clean customer names
orders = orders.withColumn(
    "customer_name",
    trim(col("customer_name"))
)

# 4. Handle missing quantity
orders = orders.fillna({"quantity": 1})

# 5. Remove duplicate orders
orders = orders.dropDuplicates()

# 6. Join orders with products
sales = orders.join(
    products,
    on="product_id",
    how="left"
)

# 7. Create total_amount
sales = sales.withColumn(
    "total_amount",
    col("quantity") * col("unit_price")
)

print("Transformed Sales:")
sales.show()

# 8. Total sales by product
product_sales = (
    sales.groupBy("product_id", "product_name")
    .agg(sum("total_amount").alias("total_sales"))
)

print("Total Sales by Product:")
product_sales.show()

# 9. Total sales by category
category_sales = (
    sales.groupBy("category")
    .agg(sum("total_amount").alias("total_sales"))
)

print("Total Sales by Category:")
category_sales.show()

# 10. Save transformed data
sales.write.mode("overwrite").option("header", True).csv(
    "transformed_sales_pyspark"
)

print("Transformation completed!")
print("Output folder: transformed_sales_pyspark")

# Stop Spark
spark.stop()
