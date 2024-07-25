from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

print('creating spark job')
# Initialize Spark session
spark = SparkSession.builder \
    .appName("KafkaSparkConsumer") \
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1') \
    .config("spark.sql.streaming.kafka.bootstrap.servers", "kafka:9093") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://hadoop-namenode:8020") \
    .master("spark://spark-master:7077") \
    .getOrCreate()
print('after creating spark job')
# Define the schema for the incoming data
schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])

# Read from Kafka topic
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9093") \
    .option("subscribe", "classifiedMessages") \
    .option("failOnDataLoss", "false") \
    .option("startingOffsets", "earliest") \
    .option("kafkaConsumer.pollTimeoutMs", "120000") \
    .load()

# Parse the value column to JSON
df = df.selectExpr("CAST(value AS STRING)")
json_df = df.select(from_json(col("value"), schema).alias("data")).select("data.*")

# Write the streaming data to HDFS
query = json_df.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "hdfs://hadoop-namenode:8020/user/spark/kafka-data") \
    .option("checkpointLocation", "hdfs://hadoop-namenode:8020/user/spark/checkpoints/kafka") \
    .start()

query.awaitTermination()

