# Real-Time Data Processing

## Goal

Learn how modern systems process events continuously and understand the
main tools and patterns used in real-time data pipelines.

## 1. Kafka Basics

**Apache Kafka** is a distributed event-streaming platform. Applications
publish events to Kafka, where they can be stored and read by other
applications.

### Core concepts

-   **Producer:** Sends events to Kafka.
-   **Consumer:** Reads events from Kafka.
-   **Topic:** A named stream of events, such as `player-events` or
    `application-logs`.
-   **Partition:** A topic is divided into partitions to support
    parallel processing. Events are ordered within a partition.
-   **Offset:** The position of an event inside a partition. Consumers
    use offsets to track their progress.
-   **Consumer group:** A group of consumers that share the work of
    reading a topic. Within a group, each partition is assigned to at
    most one consumer at a time.

### Example: Athlete tracking system

Imagine a sports application that records player activity during a
match.

A producer publishes this event to the `player-events` topic:

``` json
{
  "event_id": "evt-1001",
  "player_id": 27,
  "event_type": "goal",
  "match_id": 501,
  "event_time": "2026-10-11T15:30:00Z"
}
```

A statistics service consumes the event and updates the player's match
statistics. Another consumer could update a live scoreboard.

### How a Kafka flow works

``` text
Sports App
    |
    v
Producer
    |
    v
Kafka topic: player-events
    |
    +------> Consumer group: live-score
    |
    +------> Consumer group: analytics
```

The same event can be read by different consumer groups for different
purposes.

## 2. Event-Driven Architecture

**Event-driven architecture (EDA)** is a software design in which one
service publishes an event and other services react to it.

An **event** is a record that something has happened, such as
`OrderPlaced`, `PaymentCompleted`, or `PlayerScored`.

### Example: Online shopping

When a customer places an order:

1.  The Order Service creates the order.
2.  It publishes an `OrderPlaced` event.
3.  The Inventory Service reserves the items.
4.  The Notification Service sends an order confirmation.
5.  The Analytics Service records the order for reporting.

``` text
Customer places order
        |
        v
    OrderPlaced
        |
      Kafka
     /  |   \
Inventory Email Analytics
```

### Benefits

-   Services do not need to call every other service directly.
-   Work can happen asynchronously.
-   Services can scale independently.
-   Events can be retained and processed again when needed, depending on
    Kafka configuration and retention.

### Things to consider

-   Consumers may receive duplicate events.
-   Failed events need retries and monitoring.
-   Events should have a clear schema and unique ID.
-   A service should not assume that every other service has finished
    immediately.

## 3. Spark Streaming

**Spark Structured Streaming** processes incoming data using Spark's
DataFrame and SQL APIs. It is useful when events need filtering,
aggregation, joins, or other distributed transformations.

### Typical pipeline

``` text
Kafka topic
    |
    v
Spark Structured Streaming
    |
    +--> Filter invalid events
    +--> Calculate metrics
    +--> Group events by time
    |
    v
Data Lake / Database / Dashboard
```

### Example: Count player events

Suppose Kafka receives these events:

    player_id event_type
  ----------- ------------
           27 goal
           12 pass
           27 goal
            8 foul

A streaming job could count goals by player:

    player_id   goal_count
  ----------- ------------
           27            2

Spark can process data in small micro-batches or use supported
continuous-processing features where applicable. Structured Streaming
commonly uses micro-batches.

### Important terms

-   **Transformation:** Changes or filters the incoming data.
-   **Window:** Groups events by a time range, such as goals per five
    minutes.
-   **Checkpoint:** Stores progress and state information to help a
    query recover after failure.
-   **Sink:** The destination where processed results are written.

Checkpointing and sink behavior must be configured correctly for the
recovery and delivery guarantees you need.

## 4. At Least Once vs. Exactly Once

Streaming systems can fail while processing or writing an event.
Delivery guarantees describe what can happen during recovery.

### At least once

An event is processed one or more times. It is designed to avoid losing
events, but duplicates can happen.

**Example:** A consumer processes order `ORD-501` and writes it to a
database. Before it saves its Kafka offset, the consumer crashes. After
restarting, it reads `ORD-501` again. The database may now contain a
duplicate unless the write is protected.

### Exactly once

The intended result is that an event's effect is applied once within the
guarantees of the configured system.

**Example:** A payment event has `event_id = pay-9001`. The system uses
a transaction or idempotent write strategy so processing the same event
again does not charge the customer twice.

### Comparison

  -----------------------------------------------------------------------
  Feature                 At least once           Exactly once
  ----------------------- ----------------------- -----------------------
  Processing              One or more times       Effect applied once
                                                  within defined
                                                  guarantees

  Duplicate risk          Possible                Prevented within the
                                                  configured guarantee

  Complexity              Often simpler           Usually requires
                                                  careful configuration

  Common technique        Retry failed work       Transactions,
                                                  checkpoints, idempotent
                                                  writes
  -----------------------------------------------------------------------

**Important:** Exactly-once behavior is not automatically guaranteed
across every external database, API, or side effect. The full pipeline
must be designed to support it.

### Practical technique: Idempotency

An operation is **idempotent** when repeating it produces the same final
result as doing it once.

For example, insert an event using a unique `event_id` and reject or
update an existing record with that ID. This can prevent duplicate event
records.

## 5. Dead Letter Queue (DLQ)

A **dead letter queue** is a separate topic or queue for events that
cannot be processed successfully after the configured retries.

### Example

A consumer expects `player_id` to be an integer, but receives:

``` json
{
  "event_id": "evt-1002",
  "player_id": "unknown",
  "event_type": "goal"
}
```

The event fails validation. Instead of retrying forever or silently
dropping it, the consumer can send it to a topic such as
`player-events-dlq`.

A useful DLQ record includes: - Original event - Error message or
failure reason - Timestamp - Source topic and partition/offset, where
available - Number of attempts

### DLQ workflow

``` text
Kafka topic
    |
    v
Consumer validates event
    |
    +---- valid ----> Process event
    |
    +---- invalid after retries ----> DLQ topic
                                         |
                                         v
                                  Investigate and fix
                                         |
                                         v
                                    Replay event
```

A DLQ is not a substitute for monitoring. Track the number of failed
events and investigate recurring errors before replaying records.

## 6. Quick Summary

  -----------------------------------------------------------------------
  Concept                 Meaning                 Example
  ----------------------- ----------------------- -----------------------
  Producer                Sends events            Sports app sends a goal
                                                  event

  Consumer                Reads events            Scoreboard reads goal
                                                  events

  Topic                   Named event stream      `player-events`

  Partition               Supports parallel       A topic has three
                          processing              partitions

  Offset                  Event position in a     Consumer has read
                          partition               through offset 120

  Consumer group          Shares processing work  Three consumers process
                                                  a topic

  Event-driven            Services react to       Order placed triggers
  architecture            events                  inventory update

  Spark Streaming         Processes event streams Count goals per
                                                  five-minute window

  At least once           Event may be processed  Retry after a crash
                          again                   

  Exactly once            Effect occurs once      Deduplicate by event ID
                          within defined          
                          guarantees              

  DLQ                     Holds events that       Invalid player event
                          repeatedly fail         sent to DLQ
  -----------------------------------------------------------------------

