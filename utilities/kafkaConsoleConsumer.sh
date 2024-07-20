#! /bin/bash


docker exec -it project-k_kafka_1 ./opt/kafka/bin/kafka-console-consumer.sh --topic classifiedMessages --bootstrap-server localhost:9092 --from-beginning 
