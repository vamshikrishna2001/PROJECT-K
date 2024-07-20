#!/bin/bash


docker exec -it hadoop-namenode groupadd -r spark && useradd -r -g spark spark
docker exec -it hadoop-namenode hdfs dfs -mkdir -p /user/spark/kafka-data
docker exec -it hadoop-namenode hdfs dfs -chown -R spark:spark /user/spark
docker exec -it hadoop-namenode hdfs dfs -chmod -R 777 /user/spark/kafka-data
