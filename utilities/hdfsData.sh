#! /bin/bash

docker exec -it hadoop-namenode hdfs dfs -ls /user/spark/kafka-data
