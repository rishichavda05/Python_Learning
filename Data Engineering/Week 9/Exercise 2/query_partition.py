import psycopg2


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "sports_warehouse",
    "user": "postgres",
    "password": "postgres"
}


def query_data():

    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    query = """
        SELECT
            athlete_id,
            sport,
            performance_date,
            score,
            rank
        FROM athlete_performance
        WHERE performance_date >= '2025-01-01'
          AND performance_date < '2026-01-01'
        ORDER BY performance_date;
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    print("\n2025 Performance Data")
    print("-" * 70)

    for row in rows:
        print(row)

    cursor.close()
    connection.close()


if __name__ == "__main__":
    query_data()