#!/bin/bash

# Wait for HDFS to be ready
sleep 10

# Create necessary directories and set permissions
hdfs dfs -mkdir -p /user/spark/kafka-data
hdfs dfs -chown -R spark:spark /user/spark
hdfs dfs -chmod -R 777 /user/spark/kafka-data

# Continue with the default entrypoint


