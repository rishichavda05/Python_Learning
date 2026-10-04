import psycopg2


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "sports_warehouse",
    "user": "postgres",
    "password": "postgres"
}


def create_partitioned_table():

    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    # Main partitioned table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS athlete_performance (
            performance_id SERIAL,
            athlete_id INT NOT NULL,
            sport VARCHAR(50),
            performance_date DATE NOT NULL,
            score DECIMAL(10, 2),
            rank INT
        )
        PARTITION BY RANGE (performance_date);
    """)

    # 2024 partition
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS athlete_performance_2024
        PARTITION OF athlete_performance
        FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
    """)

    # 2025 partition
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS athlete_performance_2025
        PARTITION OF athlete_performance
        FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
    """)

    # 2026 partition
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS athlete_performance_2026
        PARTITION OF athlete_performance
        FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');
    """)

    connection.commit()

    print("Partitioned table created successfully!")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    create_partitioned_table()