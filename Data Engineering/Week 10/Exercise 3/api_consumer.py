
import json

from kafka import KafkaConsumer
from kafka.errors import KafkaError

KAFKA_SERVER = "localhost:9092"
TOPIC_NAME = "api-events"


def main():
    consumer = None

    try:
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=KAFKA_SERVER,
            group_id="api-events-consumer-group",
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )

        print("API event consumer started.")
        print("Waiting for API events... Press Ctrl+C to stop.\n")

        for record in consumer:
            try:
                event = json.loads(record.value.decode("utf-8"))

                user = event.get("user", {})

                print("=" * 55)
                print(f"Event ID: {event.get('event_id')}")
                print(f"Event type: {event.get('event_type')}")
                print(f"User ID: {user.get('id')}")
                print(f"Name: {user.get('name')}")
                print(f"Username: {user.get('username')}")
                print(f"Email: {user.get('email')}")
                print(f"Kafka partition: {record.partition}")
                print(f"Kafka offset: {record.offset}")

            except (json.JSONDecodeError, UnicodeDecodeError) as error:
                print(f"Invalid Kafka message: {error}")

    except KeyboardInterrupt:
        print("\nStopping API consumer...")

    except (KafkaError, OSError, TimeoutError) as error:
        print(f"Kafka consumer error: {error}")

    finally:
        if consumer is not None:
            consumer.close()
            print("Consumer closed.")


if __name__ == "__main__":
    main()
