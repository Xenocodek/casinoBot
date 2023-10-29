from datetime import datetime
import pytz
import random
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
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                    balance_id INTEGER NOT NULL UNIQUE,
                    user_id REFERENCES users(user_id),
                    amount INTEGER,
                    wins INTEGER,
                    currency VARCHAR(3),
                    last_updated TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                    balance_id REFERENCES balances(balance_id),
                    transaction_type VARCHAR(64),
                    amount INTEGER,
                    registration_date TIMESTAMP
            );
            """
        ]

        for query in queries:
            cur.execute(query)
            
        conn.commit()
        conn.close()

    async def new_user(self, user_id, username, user_first_name, user_last_name):
        try:
            conn, cur = self.connection()
            if conn is None:
                return
            
            user = cur.execute(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
            
            if not user:
                desired_timezone = pytz.timezone('Europe/Moscow')
                created = datetime.now(desired_timezone).strftime('%Y-%m-%d %H:%M:%S')
                time_updated = created
                amount = 1000
                wins = 0
                transaction_type = "Registration"
                currency = "ALM"
                
                cur.execute(
                    "INSERT INTO users (user_id, username, user_first_name, user_last_name, registration_date) VALUES (?, ?, ?, ?, ?)",
                    (user_id, username, user_first_name, user_last_name, created),
                )

                while True:
                    balance_id = random.randint(1000, 9999)

                    existing_balance = cur.execute("SELECT id FROM balances WHERE id = ?", (balance_id,)).fetchone()

                    if not existing_balance:
                        break
                
                cur.execute(
                    "INSERT INTO balances (balance_id, user_id, amount, wins, currency, last_updated) VALUES (?, ?, ?, ?, ?, ?)",
                    (balance_id, user_id, amount, wins, currency, time_updated),
                )

                cur.execute(
                    "INSERT INTO transactions (balance_id, transaction_type, amount, registration_date) VALUES (?, ?, ?, ?)",
                    (balance_id, transaction_type, amount, time_updated),
                )

                conn.commit()

        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

    async def get_user_data(self, user_id):
        try:
            conn, cur = self.connection()
            if conn is None:
                return
            
            user_data = cur.execute(
                """
                SELECT users.user_id, users.username, balances.amount, balances.wins
                FROM users
                JOIN balances ON users.user_id = balances.user_id
                WHERE users.user_id = ?;
                """, (user_id,)).fetchone()
            
            conn.close()

            return user_data

        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()