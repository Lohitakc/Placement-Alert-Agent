from app.database.database import get_connection


def create_tables():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS companies (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            company_code TEXT UNIQUE NOT NULL,

            company_name TEXT NOT NULL,

            company_type TEXT,

            min_package TEXT,

            max_package TEXT,

            offering TEXT,

            dead_backlog TEXT,

            live_backlog TEXT,

            year_down TEXT,

            first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()

    connection.close()