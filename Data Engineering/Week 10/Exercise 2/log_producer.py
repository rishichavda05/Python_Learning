
import json
import time
from datetime import datetime, timezone

from kafka import KafkaProducer
from kafka.errors import KafkaError

KAFKA_SERVER = "localhost:9092"
TOPIC_NAME = "application-logs"

sample_logs = [
    {
        "level": "INFO",
        "message": "Application started",
    },
    {
        "level": "WARNING",
        "message": "API response took 2 seconds",
    },
    {
        "level": "ERROR",
        "message": "Database connection failed",
    },
    {
        "level": "INFO",
        "message": "Data processing completed",
    },
    {
        "level": "ERROR",
        "message": "Input file not found",
    },
    {
        "level": "INFO",
        "message": "Pipeline health check passed",
    },
]


def main():
    producer = None

    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda value: json.dumps(value).encode("utf-8"),
            acks="all",
            retries=3,
        )

        print("Log producer started. Press Ctrl+C to stop.")

        index = 0

        while True:
            log = sample_logs[index % len(sample_logs)]

            event = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "service": "data-pipeline",
                "level": log["level"],
                "message": log["message"],
            }

            metadata = producer.send(
                TOPIC_NAME,
                value=event,
            ).get(timeout=15)

            print(
                f"Sent [{event['level']}] "
                f"{event['message']} "
                f"(partition={metadata.partition}, "
                f"offset={metadata.offset})"
            )

            index += 1
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nStopping log producer...")

    except (KafkaError, OSError, TimeoutError) as error:
        print(f"Kafka error: {error}")

    finally:
        if producer is not None:
            producer.close()
            print("Producer closed.")


if __name__ == "__main__":
    main()
