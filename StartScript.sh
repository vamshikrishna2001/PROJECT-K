#!/bin/bash


docker-compose up -d > orchestration.logs 
sleep 60

./hdfs/hdfs-init.sh > hdfs-init.logs
sleep 60

docker exec -it spark-master spark-submit --master spark://spark-master:7077 --deploy-mode client --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 /opt/spark-apps/ingestion.py > ingestion.logs
