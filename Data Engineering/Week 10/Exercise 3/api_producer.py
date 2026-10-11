
import time
from datetime import datetime, timezone

import requests
from kafka import KafkaProducer
from kafka.errors import KafkaError

API_URL = "https://jsonplaceholder.typicode.com/users"
KAFKA_SERVER = "localhost:9092"
TOPIC_NAME = "api-events"
POLL_INTERVAL = 15  # seconds


def main():
    producer = None
    seen_user_ids = set()

    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda value: __import__("json").dumps(
                value
            ).encode("utf-8"),
            acks="all",
            retries=3,
        )

        print("API producer started.")
        print(f"Polling API every {POLL_INTERVAL} seconds.")
        print("Press Ctrl+C to stop.\n")

        while True:
            try:
                response = requests.get(API_URL, timeout=10)
                response.raise_for_status()
                users = response.json()

                if not isinstance(users, list):
                    raise ValueError("API response must be a list")

                new_count = 0

                for user in users:
                    user_id = user.get("id")

                    if user_id is None:
                        print("Skipping record without a user ID.")
                        continue

                    if user_id in seen_user_ids:
                        continue

                    event = {
                        "event_id": f"user-{user_id}",
                        "event_type": "user_discovered",
                        "source": "jsonplaceholder",
                        "ingested_at": datetime.now(
                            timezone.utc
                        ).isoformat(),
                        "user": user,
                    }

                    metadata = producer.send(
                        TOPIC_NAME,
                        value=event,
                    ).get(timeout=15)

                    # Mark as seen only after Kafka acknowledges it.
                    seen_user_ids.add(user_id)
                    new_count += 1

                    print(
                        f"Published user ID {user_id} "
                        f"to partition {metadata.partition}, "
                        f"offset {metadata.offset}"
                    )

                if new_count == 0:
                    print(
                        f"{datetime.now().isoformat(timespec='seconds')}: "
                        "No new users found."
                    )
                else:
                    print(f"Published {new_count} new user events.")

            except requests.RequestException as error:
                print(f"API request failed: {error}")

            except (ValueError, TypeError) as error:
                print(f"Invalid API response: {error}")

            except (KafkaError, OSError, TimeoutError) as error:
                print(f"Kafka publishing failed: {error}")

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\nStopping API producer...")

    except (KafkaError, OSError, TimeoutError) as error:
        print(f"Could not connect to Kafka: {error}")

    finally:
        if producer is not None:
            producer.close()
            print("Producer closed.")


if __name__ == "__main__":
    main()
