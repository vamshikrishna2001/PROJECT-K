#!/bin/bash

# Function to check if Kafka is available
wait_for_kafka() {
  while ! nc -z kafka 9093; do   
    echo "Waiting for Kafka to be ready..."
    sleep 2
  done
}

# Wait for Kafka to be available
wait_for_kafka

# Run the application
python3 llm.py

