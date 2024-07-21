#!/bin/bash

echo 'bringing up containers'
docker-compose up -d > orchestration.logs
echo 'sleeping for 60 seconds'
sleep 60

echo 'setting up hdfs'
./hdfs/hdfs-init.sh > hdfs-init.logs
sleep 60

echo 'starting the spark job'
docker exec -it spark-master spark-submit --master spark://spark-master:7077 --deploy-mode client --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 /opt/spark-apps/ingestion.py > ingestion.logs
