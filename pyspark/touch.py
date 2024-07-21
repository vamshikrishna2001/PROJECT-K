from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StringType, StructType, StructField

# Create a Spark session
spark = SparkSession.builder \
    .appName("KafkaToHadoop") \
    .getOrCreate()

# Define Kafka parameters
kafka_bootstrap_servers = "kafka:9093"
kafka_topic = "your_topic"

# Define the schema for the JSON data
schema = StructType([
    StructField("field1", StringType()),
    StructField("field2", StringType())
])

# Read data from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .load()

# Convert the value column to a string and parse the JSON
json_df = df.selectExpr("CAST(value AS STRING) as value")
parsed_df = json_df.select(from_json(col("value"), schema).alias("data")).select("data.*")

# Define Hadoop parameters
hadoop_output_path = "hdfs://hadoop-namenode:8020/user/hadoop/output"

# Write the parsed data to Hadoop
query = parsed_df.writeStream \
    .outputMode("append") \
    .format("csv") \
    .option("path", hadoop_output_path) \
    .start()

query.awaitTermination()

