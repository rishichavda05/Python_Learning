import psycopg2


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "sports_warehouse",
    "user": "postgres",
    "password": "postgres"
}


def insert_data():

    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    data = [
        (101, "Cricket", "2024-03-15", 85.5, 2),
        (102, "Football", "2024-06-20", 78.0, 5),
        (103, "Athletics", "2024-09-10", 91.5, 1),

        (101, "Cricket", "2025-02-12", 88.0, 1),
        (102, "Football", "2025-07-18", 82.5, 3),
        (104, "Swimming", "2025-11-05", 89.0, 2),

        (101, "Cricket", "2026-01-25", 92.0, 1),
        (103, "Athletics", "2026-04-14", 87.5, 2),
        (104, "Swimming", "2026-08-22", 94.0, 1)
    ]

    insert_query = """
        INSERT INTO athlete_performance
        (
            athlete_id,
            sport,
            performance_date,
            score,
            rank
        )
        VALUES (%s, %s, %s, %s, %s);
    """

    cursor.executemany(insert_query, data)

    connection.commit()

    print("Data inserted successfully!")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    insert_data()