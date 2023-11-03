from datetime import datetime
import pytz
import random
import sqlite3 as sq


class DatabaseManager:
    def __init__(self, db_file='database/casino_bot.db'):
        """
        Initializes the DatabaseManager class.
        """

        self.db_file = db_file

    def connection(self):
        """
        Connects to the database and returns a connection and cursor object.
        """

        try:
            conn = sq.connect(self.db_file)
            cur = conn.cursor()
            return conn, cur
        except sq.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")
            return None


    async def db_start(self):
        """
        Creates tables in the database if they don't exist.
        """

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
                    registration_date TIMESTAMP,
                    is_admin BOOLEAN DEFAULT(FALSE)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS balances (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                    balance_id INTEGER NOT NULL UNIQUE,
                    user_id REFERENCES users(user_id),
                    total REAL,
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
                    combination VARCHAR(64),
                    amount REAL,
                    last_updated TIMESTAMP
            );
            """
        ]

        for query in queries:
            cur.execute(query)
            
        conn.commit()
        conn.close()


    async def new_user(self, user_id, username, user_first_name, user_last_name):
        """
        Creates a new user in the database.
        """
        
        try:
            conn, cur = self.connection()
            if conn is None:
                return
            
            user = cur.execute(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
            
            # Check if the user already exists
            if not user:
                desired_timezone = pytz.timezone('Europe/Moscow')
                created = datetime.now(desired_timezone).strftime('%Y-%m-%d %H:%M:%S')
                time_updated = created
                amount = 1000
                wins = 0
                transaction_type = "Registration"
                currency = "ALM"
                
                # Insert the new user into the 'users' table
                cur.execute(
                    """
                    INSERT INTO users (user_id, username, user_first_name, user_last_name, registration_date) 
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (user_id, username, user_first_name, user_last_name, created),
                )

                # Generate a unique balance ID and insert user's initial balance in the 'balances' table
                while True:
                    balance_id = random.randint(1000, 9999)

                    existing_balance = cur.execute("SELECT id FROM balances WHERE id = ?", (balance_id,)).fetchone()

                    if not existing_balance:
                        break
                
                cur.execute(
                    """
                    INSERT INTO balances (balance_id, user_id, total, wins, currency, last_updated) 
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (balance_id, user_id, amount, wins, currency, time_updated),
                )

                # Add a transaction record for the initial registration
                cur.execute(
                    """
                    INSERT INTO transactions (balance_id, transaction_type, amount, last_updated) 
                    VALUES (?, ?, ?, ?)
                    """,
                    (balance_id, transaction_type, amount, time_updated),
                )

                conn.commit()   # Commit the transaction to the database

        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()    # Close the database connection


    async def get_admins(self, user_id):
        """
        Retrieves a list of admin IDs from the database.
        """
        try:
            conn, cur = self.connection()
            if conn is None:
                return
            
            # Fetch user data based on the user ID from 'users' and 'balances' tables
            admin_id = cur.execute(

                """
                SELECT user_id 
                FROM users 
                WHERE user_id = ? AND is_admin IS TRUE;
                """, (user_id,)).fetchone()
            
            conn.close()

            return admin_id    # Return the fetched user data

        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()    # Close the database connection


    async def get_user_data(self, user_id):
        """
        Retrieves user data based on the user ID.
        """

        try:
            conn, cur = self.connection()
            if conn is None:
                return
            
            # Fetch user data based on the user ID from 'users' and 'balances' tables
            user_data = cur.execute(
                """
                SELECT users.user_id, users.username, balances.total, balances.wins
                FROM users
                JOIN balances ON users.user_id = balances.user_id
                WHERE users.user_id = ?;
                """, (user_id,)).fetchone()
            
            conn.close()

            return user_data    # Return the fetched user data

        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()    # Close the database connection


    async def get_user_balance(self, user_id):
        """
        Retrieves the balance of a user based on the user ID.
        """
        
        try:
            conn, cur = self.connection()
            if conn is None:
                return
            
            # Fetch the user's balance from the 'balances' table based on the user ID
            user_data = cur.execute(
                """
                SELECT balances.total
                FROM users
                JOIN balances ON users.user_id = balances.user_id
                WHERE users.user_id = ?;
                """, (user_id,)).fetchone()
            
            conn.close()

            return user_data    # Return the fetched user data

        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()    # Close the database connection


    async def change_balance(self, amount, wins, user_id):
        """
        Changes the balance of a user based on the user ID.
        """
        
        try:
            conn, cur = self.connection()
            if conn is None:
                return
            
            # Execute the SQL query to update the balance
            cur.execute(
                """
                UPDATE balances
                SET total = total + ?,
                    wins = wins + ?
                WHERE user_id = ?
                """,
                (amount, wins, user_id),
            )   
            
            # Commit the changes to the database
            conn.commit()

        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()    # Close the database connection

    async def change__transactions(self, transaction_type, combination, amount, user_id):
        """
        Asynchronously changes the transactions in the database.
        """

        try:
            conn, cur = self.connection()
            if conn is None:
                return
            
            # Get the current time in the desired timezone
            desired_timezone = pytz.timezone('Europe/Moscow')
            time_updated = datetime.now(desired_timezone).strftime('%Y-%m-%d %H:%M:%S')
            
            # Insert a new record into the 'transactions' table
            cur.execute(
                """
                INSERT INTO transactions (balance_id, transaction_type, combination, amount, last_updated)
                SELECT balances.balance_id, ?, ?, ?, ?
                FROM balances
                WHERE balances.user_id = ?;
                """,
                (transaction_type, combination, amount, time_updated, user_id),
            )

            # Commit the changes to the database
            conn.commit()

        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()    # Close the database connection

    
    async def give_daily_bonus(self):
        """
        Asynchronously gives a daily bonus to users who have a balance less than 1000.
        """

        try:
            conn, cur = self.connection()
            if conn is None:
                return
            
            # Set the desired timezone and get the current time
            desired_timezone = pytz.timezone('Europe/Moscow')
            time_updated = datetime.now(desired_timezone).strftime('%Y-%m-%d %H:%M:%S')

            # Set the transaction type and amount for the daily bonus
            transaction_type = "LOW Bonus"
            amount = 1000
            
            # Insert a new transaction record for each user with a balance less than 1000
            cur.execute(
                """
                INSERT INTO transactions (balance_id, transaction_type, amount, last_updated)
                SELECT balances.balance_id, ?, ?, ?
                FROM balances
                WHERE balances.total < 1000;
                """,
                (transaction_type, amount, time_updated),
            )

            # Commit the transaction to the database
            conn.commit()

            # Update the balance for each user with a balance less than 1000
            cur.execute(
                """
                UPDATE balances
                SET total = ?, last_updated = ?
                WHERE total < 1000;
                """,
                (amount, time_updated),
            )
            
            # Commit the changes to the database
            conn.commit()

        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()    # Close the database connection