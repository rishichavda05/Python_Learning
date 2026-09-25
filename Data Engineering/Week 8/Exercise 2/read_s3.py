from pyspark.sql import SparkSession


# --------------------------------------------------
# Configuration
# --------------------------------------------------

AWS_REGION = "ap-south-1"

S3_PATH = "s3a://YOUR_BUCKET_NAME/raw-data/sales.csv"


# --------------------------------------------------
# Create Spark Session
# --------------------------------------------------

spark = (
    SparkSession.builder
    .appName("ReadS3UsingSpark")
    .config(
        "spark.hadoop.fs.s3a.aws.credentials.provider",
        "com.amazonaws.auth.DefaultAWSCredentialsProviderChain"
    )
    .getOrCreate()
)


# --------------------------------------------------
# Read CSV from S3
# --------------------------------------------------

df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(S3_PATH)
)


# --------------------------------------------------
# Display Data
# --------------------------------------------------

print("\n===== S3 DATA =====")

df.show()


# --------------------------------------------------
# Display Schema
# --------------------------------------------------

print("\n===== SCHEMA =====")

df.printSchema()


# --------------------------------------------------
# Basic Analysis
# --------------------------------------------------

print("\n===== TOTAL RECORDS =====")

print(df.count())


# --------------------------------------------------
# Stop Spark
# --------------------------------------------------

spark.stop()