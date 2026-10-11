
import json
from datetime import datetime, timezone

from kafka import KafkaProducer
from kafka.errors import KafkaError

# Kafka configuration
KAFKA_SERVER = "localhost:9092"
TOPIC_NAME = "player-events"


def main():
    producer = None

    try:
        # Connect Python to Kafka
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda value: json.dumps(value).encode("utf-8"),
            acks="all",
            retries=3,
        )

        print("Connected to Kafka!")
        print(f"Sending events to topic: {TOPIC_NAME}\n")

        # Sample athlete/player events
        player_events = [
            {
                "event_id": "evt-1001",
                "player_id": 27,
                "player_name": "Virat",
                "event_type": "goal",
                "match_id": 501,
            },
            {
                "event_id": "evt-1002",
                "player_id": 12,
                "player_name": "Rohit",
                "event_type": "pass",
                "match_id": 501,
            },
            {
                "event_id": "evt-1003",
                "player_id": 18,
                "player_name": "Rahul",
                "event_type": "foul",
                "match_id": 501,
            },
            {
                "event_id": "evt-1004",
                "player_id": 27,
                "player_name": "Virat",
                "event_type": "goal",
                "match_id": 501,
            },
            {
                "event_id": "evt-1005",
                "player_id": 12,
                "player_name": "Rohit",
                "event_type": "assist",
                "match_id": 501,
            },
        ]

        # Send events to Kafka
        for event in player_events:
            event["event_time"] = datetime.now(
                timezone.utc
            ).isoformat()

            # Wait for Kafka to acknowledge the message
            result = producer.send(TOPIC_NAME, value=event).get(
                timeout=15
            )

            print(f"Event sent: {event['event_id']}")
            print(f"Player: {event['player_name']}")
            print(f"Type: {event['event_type']}")
            print(f"Partition: {result.partition}")
            print(f"Offset: {result.offset}")
            print("-" * 35)

        producer.flush()
        print("\nAll player events sent successfully!")

    except (KafkaError, OSError, TimeoutError) as error:
        print(f"Kafka error: {error}")

    finally:
        if producer is not None:
            producer.close()
            print("Producer connection closed.")


if __name__ == "__main__":
    main()
