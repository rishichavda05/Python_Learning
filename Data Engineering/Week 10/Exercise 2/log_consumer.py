
import json

from kafka import KafkaConsumer
from kafka.errors import KafkaError

KAFKA_SERVER = "localhost:9092"
TOPIC_NAME = "application-logs"

# Counts for the current consumer run
total_logs = 0
error_count = 0
warning_count = 0
info_count = 0


def main():
    global total_logs, error_count, warning_count, info_count

    consumer = None

    try:
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=KAFKA_SERVER,
            group_id="log-monitor-group",
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )

        print("Real-time log consumer started.")
        print("Waiting for log messages... Press Ctrl+C to stop.\n")

        for record in consumer:
            try:
                log_event = json.loads(
                    record.value.decode("utf-8")
                )

                level = str(
                    log_event.get("level", "UNKNOWN")
                ).upper()

                message = log_event.get(
                    "message", "No message provided"
                )

                timestamp = log_event.get(
                    "timestamp", "Unknown time"
                )

                total_logs += 1

                if level == "ERROR":
                    error_count += 1
                elif level == "WARNING":
                    warning_count += 1
                elif level == "INFO":
                    info_count += 1

                print(f"Time: {timestamp}")
                print(f"Level: {level}")
                print(f"Message: {message}")

                if level == "ERROR":
                    print("*** ERROR DETECTED ***")

                print(
                    f"Stats: total={total_logs}, "
                    f"errors={error_count}, "
                    f"warnings={warning_count}, "
                    f"info={info_count}"
                )
                print("-" * 60)

            except (json.JSONDecodeError, UnicodeDecodeError) as error:
                print(f"Invalid log message: {error}")

    except KeyboardInterrupt:
        print("\nStopping log consumer...")

    except (KafkaError, OSError, TimeoutError) as error:
        print(f"Kafka error: {error}")

    finally:
        if consumer is not None:
            consumer.close()
            print("Consumer closed.")


if __name__ == "__main__":
    main()
