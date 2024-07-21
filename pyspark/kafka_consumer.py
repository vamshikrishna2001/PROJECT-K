from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType



print('creating soark job')
# Initialize Spark session
spark = SparkSession.builder \
    .appName("KafkaSparkConsumer") \
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1') \
    .config("spark.sql.streaming.kafka.bootstrap.servers", "kafka:9093") \
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
    .option("subscribe", "sample_topic") \
    .option("startingOffsets", "earliest") \
    .option("kafkaConsumer.pollTimeoutMs", "120000") \
    .load()

# Parse the value column to JSON
df = df.selectExpr("CAST(value AS STRING)")
json_df = df.select(from_json(col("value"), schema).alias("data")).select("data.*")
#output_df = json_df.selectExpr("to_json(struct(*)) AS value")
# Write the streaming data to the console
#query = output_df.writeStream \
#    .format("kafka") \
#    .option("kafka.bootstrap.servers", "172.18.0.3:9092") \
#    .option("topic", "outputTopic") \
#    .option("checkpointLocation", "/dir") \
#    .start()
#query.awaitTermination()

query = json_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
