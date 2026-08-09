from app.database.database import get_connection


def create_tables():

    connection = get_connection()

    cursor = connection.cursor()

    # TPO companies
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

    # Relevant Telegram messages
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS telegram_messages (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            telegram_message_id INTEGER NOT NULL,

            chat_id INTEGER NOT NULL,

            message_text TEXT NOT NULL,

            message_date TIMESTAMP,

            company_detected INTEGER DEFAULT 0,

            name_mentioned INTEGER DEFAULT 0,

            shortlist_detected INTEGER DEFAULT 0,

            first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(chat_id, telegram_message_id)
        )
        """
    )

    connection.commit()

    connection.close()