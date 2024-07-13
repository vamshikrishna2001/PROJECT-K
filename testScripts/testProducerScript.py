from kafka import KafkaProducer
import json
import time

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

producer = KafkaProducer(
    bootstrap_servers=["172.18.0.5:9092"],
    value_serializer=json_serializer
)

if __name__ == "__main__":
    while True:
        sample_data = {"name": "John Doe", "age": 30}
        producer.send("sample_topic", sample_data)
        print(f"Sent: {sample_data}")
        time.sleep(1)  # Adjust the sleep time as needed

