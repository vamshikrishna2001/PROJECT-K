package KafkaConsumerScript

import (
	"fmt"
	"log"
	"os"
	"os/signal"

	"github.com/IBM/sarama"
)

func KafkaConsumer() {
	// Kafka broker address and topic names
	broker := "project-k_kafka_1:9093" // Adjust to your Kafka broker address
	consumerTopic := "rawMessages"
	producerTopic := "processedMessages"

	// Create Kafka consumer configuration
	config := sarama.NewConfig()
	config.Consumer.Return.Errors = true

	// Create Kafka consumer
	consumer, err := sarama.NewConsumer([]string{broker}, config)
	if err != nil {
		log.Fatalf("Error creating consumer: %v", err)
	}
	defer func() {
		if err := consumer.Close(); err != nil {
			log.Fatalf("Error closing consumer: %v", err)
		}
	}()

	// Create Kafka producer configuration
	producerConfig := sarama.NewConfig()
	producerConfig.Producer.Return.Successes = true

	// Create Kafka producer
	producer, err := sarama.NewSyncProducer([]string{broker}, producerConfig)
	if err != nil {
		log.Fatalf("Error creating producer: %v", err)
	}
	defer func() {
		if err := producer.Close(); err != nil {
			log.Fatalf("Error closing producer: %v", err)
		}
	}()

	// Create signal channel to handle SIGINT
	signals := make(chan os.Signal, 1)
	signal.Notify(signals, os.Interrupt)

	// Create consumer for topic
	consumerPartition, err := consumer.ConsumePartition(consumerTopic, 0, sarama.OffsetOldest)
	if err != nil {
		log.Fatalf("Error consuming topic %s: %v", consumerTopic, err)
	}

	// Consume messages
	go func() {
		for {
			select {
			case msg := <-consumerPartition.Messages():
				fmt.Printf("Received message from topic %s: %s\n", consumerTopic, string(msg.Value))

				// Example of processing the message (here we just append 'Processed: ' to the message)
				processedMessage := fmt.Sprintf("Processed: %s", msg.Value)

				// Produce the processed message to the new topic
				_, _, err := producer.SendMessage(&sarama.ProducerMessage{
					Topic: producerTopic,
					Value: sarama.StringEncoder(processedMessage),
				})
				if err != nil {
					log.Printf("Failed to produce message: %v\n", err)
				} else {
					fmt.Printf("Produced message to topic %s: %s\n", producerTopic, processedMessage)
				}

			case <-signals:
				fmt.Println("Interrupt signal received, shutting down consumer...")
				return
			}
		}
	}()

	// Wait for interrupt signal to gracefully shut down
	<-signals
}
