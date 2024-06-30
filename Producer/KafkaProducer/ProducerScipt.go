package KafkaProducerScript

import (
	"bufio"
	"encoding/csv"
	"encoding/json"
	"log"
	"os"

	"github.com/IBM/sarama"
)

// Message struct for JSON serialization
type Message struct {
	Sentiment string `json:"sentiment"`
	Tweet     string `json:"tweet"`
}

func KafkaProducer() {
	topic := "rawMessages"
	// Set up the Sarama configuration
	config := sarama.NewConfig()
	config.Producer.Return.Successes = true

	// Create a new Sarama producer
	producer, err := sarama.NewSyncProducer([]string{"project-k_kafka_1:9093"}, config)
	if err != nil {
		log.Fatalf("Failed to create producer: %s", err)
	}
	defer producer.Close()

	// Open the Sentiment140 dataset CSV file
	file, err := os.Open("sentiment.csv")
	if err != nil {
		log.Fatalf("Failed to open file: %s", err)
	}
	defer file.Close()

	// Read the CSV file
	reader := csv.NewReader(bufio.NewReader(file))
	reader.LazyQuotes = true
	reader.Comma = ','

	for i := 0; i <= 9; i++ {
		record, err := reader.Read()
		if err != nil {
			break
		}

		// Assuming you want to send data from columns 0 (sentiment) and 5 (tweet)
		sentiment := record[0] // The sentiment label
		tweet := record[5]     // The tweet text

		// Create a message struct
		message := Message{
			Sentiment: sentiment,
			Tweet:     tweet,
		}

		// Serialize message to JSON
		messageJSON, err := json.Marshal(message)
		if err != nil {
			log.Printf("Failed to marshal JSON: %s", err)
			continue
		}

		// Produce the message to Kafka
		msg := &sarama.ProducerMessage{
			Topic: topic,
			Value: sarama.ByteEncoder(messageJSON),
		}

		partition, offset, err := producer.SendMessage(msg)
		if err != nil {
			log.Printf("Failed to produce message: %s", err)
		} else {
			log.Printf("Message sent to partition %d with offset %d", partition, offset)
		}
	}
}
