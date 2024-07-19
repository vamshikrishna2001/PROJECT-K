from kafka import KafkaConsumer, KafkaProducer
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Define the Kafka consumer
consumer = KafkaConsumer(
    'processedMessages',      # Replace with your topic name
    bootstrap_servers=['project-k_kafka_1:9093'],  # Replace with your Kafka server address
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    consumer_timeout_ms=1000
)

# Define the Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['project-k_kafka_1:9093'],  # Replace with your Kafka server address
    value_serializer=lambda v: str(v).encode('utf-8')
)

# Initialize the tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased')

# Function to classify sentiment
def classify_sentiment(messages, tokenizer, model):
    inputs = tokenizer(messages, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=1)
    return predictions

# Function to process messages and classify sentiment
def process_messages(consumer, producer, tokenizer, model):
    while True:
        try:
            messages = []
            
            for message in consumer:
                messages.append(message.value.decode('utf-8'))
                if len(messages) >= 32:  # You can adjust this batch size as needed
                    break
            
            if messages:
                # Perform sentiment analysis
                predictions = classify_sentiment(messages, tokenizer, model)
                
                # Publish the classified messages to the new Kafka topic
                for i, prediction in enumerate(predictions):
                    result = {'message': messages[i], 'sentiment': prediction.item()}
                    producer.send('classifiedMessages', value=result)
                
                print(f"Processed {len(messages)} messages and classified their sentiments.")
        
        except Exception as e:
            print(f"Error occurred: {e}")

# Start processing messages
process_messages(consumer, producer, tokenizer, model)

# Close the consumer and producer gracefully
consumer.close()
producer.close()

