import psycopg2


# PostgreSQL connection details
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "sports_warehouse",
    "user": "postgres",
    "password": "postgres"
}


def create_warehouse_schema():
    try:
        # Connect to PostgreSQL
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        print("Connected to PostgreSQL")

        # Create dimension table: Athlete
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dim_athlete (
                athlete_key SERIAL PRIMARY KEY,
                athlete_id INT UNIQUE NOT NULL,
                athlete_name VARCHAR(100) NOT NULL,
                country VARCHAR(100),
                gender VARCHAR(20),
                date_of_birth DATE
            );
        """)

        # Create dimension table: Sport
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dim_sport (
                sport_key SERIAL PRIMARY KEY,
                sport_id INT UNIQUE NOT NULL,
                sport_name VARCHAR(100) NOT NULL,
                category VARCHAR(100)
            );
        """)

        # Create dimension table: Date
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dim_date (
                date_key INT PRIMARY KEY,
                full_date DATE UNIQUE NOT NULL,
                year INT,
                month INT,
                day INT,
                quarter INT
            );
        """)

        # Create fact table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fact_performance (
                performance_key SERIAL PRIMARY KEY,

                athlete_key INT NOT NULL,
                sport_key INT NOT NULL,
                date_key INT NOT NULL,

                score DECIMAL(10,2),
                rank INT,
                performance_time DECIMAL(10,2),

                FOREIGN KEY (athlete_key)
                    REFERENCES dim_athlete(athlete_key),

                FOREIGN KEY (sport_key)
                    REFERENCES dim_sport(sport_key),

                FOREIGN KEY (date_key)
                    REFERENCES dim_date(date_key)
            );
        """)

        # Save changes
        connection.commit()

        print("Warehouse schema created successfully!")

        # Close connection
        cursor.close()
        connection.close()

    except psycopg2.Error as error:
        print("Database error:", error)


if __name__ == "__main__":
    create_warehouse_schema()