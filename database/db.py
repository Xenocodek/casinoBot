import pymysql
import logging
import random
import pytz

from datetime import datetime

from settings.config import DatabaseConfig

dbconfig = DatabaseConfig()


class DatabaseManager:
    def __init__(self, host = dbconfig.host, port = dbconfig.port,  user = dbconfig.user, password = dbconfig.password, dbname = dbconfig.database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname
        self.connection = None

    def open_connection(self):
        if not self.connection:
            try:
                self.connection = pymysql.connect(host=self.host,
                                                port=self.port,
                                                user=self.user,
                                                password=self.password,
                                                db=self.dbname,
                                                charset='utf8mb4',
                                                cursorclass=pymysql.cursors.DictCursor)
                logging.info('Connection to the database was successful.')
            except pymysql.MySQLError as e:
                logging.info(f'Connection to the database failed: {e}')
                raise e
    
    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            logging.info('Database connection closed.')


    def db_start(self):
        try:
            self.open_connection()
            with self.connection.cursor() as cursor:
                queries = [
                    """CREATE TABLE IF NOT EXISTS users (
                            id INT PRIMARY KEY AUTO_INCREMENT,
                            user_id INT NOT NULL UNIQUE,
                            username VARCHAR(64),
                            user_first_name VARCHAR(64),
                            user_last_name VARCHAR(64),
                            registration_date TIMESTAMP,
                            is_admin BOOLEAN DEFAULT FALSE
                    );""",
                    """CREATE TABLE IF NOT EXISTS balances (
                            id INT PRIMARY KEY AUTO_INCREMENT,
                            balance_id INT NOT NULL UNIQUE,
                            user_id INT,
                            total REAL,
                            wins INT,
                            currency VARCHAR(3),
                            last_updated TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users(user_id)
                    );""",
                    """CREATE TABLE IF NOT EXISTS transactions (
                            id INT PRIMARY KEY AUTO_INCREMENT,
                            balance_id INT,
                            transaction_type VARCHAR(64),
                            combination VARCHAR(64),
                            amount REAL,
                            last_updated TIMESTAMP,
                            FOREIGN KEY (balance_id) REFERENCES balances(balance_id)
                    );"""
                ]

                for query in queries:
                    cursor.execute(query)

                self.connection.commit()
                logging.info('Database tables have been created')

        except pymysql.MySQLError as e:
            logging.error(f'Database operation failed: {e}')
        finally:
            self.close_connection()

    
    async def new_user(self, user_id, username, user_first_name, user_last_name):
        """
        Creates a new user in the database.
        """

        try:
            self.open_connection()
            with self.connection.cursor() as cursor:
            
                cursor.execute(
                    "SELECT * FROM users WHERE user_id = %s", (user_id,))
                user = cursor.fetchone()

                if not user:
                    desired_timezone = pytz.timezone('Europe/Moscow')
                    created = datetime.now(desired_timezone).strftime('%Y-%m-%d %H:%M:%S')
                    amount = 1000
                    wins = 0
                    transaction_type = "Registration"
                    currency = "ALM"
                    
                    # Insert the new user into the 'users' table
                    cursor.execute(
                        """
                        INSERT INTO users (user_id, username, user_first_name, user_last_name, registration_date) 
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (user_id, username, user_first_name, user_last_name, created),
                    )

                    # Generate a unique balance_id and insert user's initial balance in the 'balances' table
                    balance_id = None
                    while balance_id is None:
                        potential_id = random.randint(1000, 9999)
                        cursor.execute("SELECT id FROM balances WHERE balance_id = %s", (potential_id,))
                        existing_balance = cursor.fetchone()
                        if not existing_balance:
                            balance_id = potential_id
                    
                    cursor.execute(
                        """
                        INSERT INTO balances (balance_id, user_id, total, wins, currency, last_updated) 
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (balance_id, user_id, amount, wins, currency, created),
                    )

                    # Add a transaction record for the initial registration
                    cursor.execute(
                        """
                        INSERT INTO transactions (balance_id, transaction_type, amount, last_updated) 
                        VALUES (%s, %s, %s, %s)
                        """,
                        (balance_id, transaction_type, amount, created),
                    )

                    self.connection.commit()
                    logging.info('The request to create a new user has been completed')

                else:
                    logging.info('The user is already in the Database')

        except pymysql.MySQLError as e:
            logging.error(f'Database operation failed: {e}')
        finally:
            self.close_connection()
