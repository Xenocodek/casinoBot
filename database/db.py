from datetime import datetime
import pytz
import sqlite3 as sq


class DatabaseManager:
    def __init__(self, db_file='database/casino_bot.db'):
        self.db_file = db_file

    def connection(self):
        try:
            conn = sq.connect(self.db_file)
            cur = conn.cursor()
            return conn, cur
        except sq.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")
            return None


    async def db_start(self):
        conn, cur = self.connection()
        if conn is None:
            return
        
        queries = [
            """
            CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                    user_id INTEGER NOT NULL UNIQUE,
                    username        VARCHAR(64),
                    user_first_name VARCHAR(64),
                    user_last_name  VARCHAR(64),
                    registration_date TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS balances (
                    id INTEGER PRIMARY KEY UNIQUE NOT NULL,
                    user_id REFERENCES users(user_id),
                    balance INTEGER,
                    last_updated TIMESTAMP
            );
            """
        ]

        for query in queries:
            cur.execute(query)
            
        conn.commit()
        conn.close()

    async def new_user(self, user_id, username, user_first_name, user_last_name):
        conn, cur = self.connection()
        if conn is None:
            return
        
        user = cur.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()

        if not user:
            desired_timezone = pytz.timezone('Europe/Moscow')
            created = datetime.now(desired_timezone).strftime('%Y-%m-%d %H:%M:%S')
            time_updated = created
            
            cur.execute(
                "INSERT INTO users (user_id, username, user_first_name, user_last_name, registration_date) VALUES (?, ?, ?, ?, ?)",
                (user_id, username, user_first_name, user_last_name, created),
            )
            cur.execute(
                "INSERT INTO balances (user_id, balance, last_updated) VALUES (?, ?, ?)",
                (user_id, 1000, time_updated),
            )

            conn.commit()
            conn.close()