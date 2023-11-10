import pymysql
import logging
import random
import pytz

from datetime import datetime

from settings.config import DatabaseConfig

dbconfig = DatabaseConfig()


class DatabaseManager:
    def __init__(self, host = dbconfig.host, 
                port = dbconfig.port,  
                user = dbconfig.user, 
                password = dbconfig.password, 
                dbname = dbconfig.database):
        
        """
        Initialize the class with database connection parameters.
        """
        
        # Assign the input parameters to class attributes
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname

        # Initialize the connection to None
        self.connection = None

    def open_connection(self):
        # Check if a connection already exists
        if not self.connection:
            try:
                # Establish a new connection using pymysql
                self.connection = pymysql.connect(host=self.host,
                                                port=self.port,
                                                user=self.user,
                                                password=self.password,
                                                db=self.dbname,
                                                charset='utf8mb4',
                                                cursorclass=pymysql.cursors.DictCursor)
                # Log a success message if connection is successful
                logging.info('Connection to the database was successful.')
            except pymysql.MySQLError as e:
                # Log an error message if connection fails and raise the exception
                logging.info(f'Connection to the database failed: {e}')
                raise e
    
    def close_connection(self):
        # Check if the connection exists
        if self.connection:
            # Close the connection
            self.connection.close()
            # Set the connection to None
            self.connection = None
            # Log the closing of the database connection
            logging.info('Database connection closed.')


    async def db_start(self):
        """
        Creates tables in the database if they don't exist.
        """

        try:
            self.open_connection()
            with self.connection.cursor() as cursor:
                # Define SQL queries to create tables if they don't exist
                queries = [
                    """CREATE TABLE IF NOT EXISTS users (
                            id INT PRIMARY KEY AUTO_INCREMENT,
                            user_id VARCHAR(64) NOT NULL UNIQUE,
                            username VARCHAR(64),
                            user_first_name VARCHAR(64),
                            user_last_name VARCHAR(64),
                            registration_date TIMESTAMP,
                            is_admin BOOLEAN DEFAULT FALSE,
                            default_language VARCHAR(2) DEFAULT 'RU'
                    );""",
                    """CREATE TABLE IF NOT EXISTS balances (
                            id INT PRIMARY KEY AUTO_INCREMENT,
                            balance_id INT NOT NULL UNIQUE,
                            user_id VARCHAR(64),
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

                # Execute each query
                for query in queries:
                    cursor.execute(query)

                # Commit the changes
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
            
                logging.info(f"{user_id}")
                
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


    async def get_admins(self, user_id):
        """
        Retrieves a list of admin IDs from the database.
        """
        try:
            self.open_connection()

            with self.connection.cursor() as cursor:
                # Fetch user data based on the user ID from 'users' table
                cursor.execute(
                    """
                    SELECT user_id 
                    FROM users 
                    WHERE user_id = %s AND is_admin = 1;
                    """, (user_id,))
                admin_id = cursor.fetchone()
                
                logging.info('The request to get admins has been completed')
                return admin_id  # Return the fetched user data

        except pymysql.MySQLError as e:
            logging.error(f'Database operation failed: {e}')
        finally:
            self.close_connection()

    
    async def get_user_data(self, user_id):
        """
        Retrieves user data based on the user ID.
        """
        try:
            self.open_connection()
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT users.user_id, users.username, balances.total, balances.wins
                    FROM users
                    JOIN balances ON users.user_id = balances.user_id
                    WHERE users.user_id = %s;
                    """, (user_id,))
                user_data = cursor.fetchone()
                
                logging.info('The request to get user data has been completed')
                return user_data  # Return the fetched user data

        except pymysql.MySQLError as e:
            logging.error(f"Database operation failed: {e}")
        finally:
            self.close_connection()

    
    async def get_user_balance(self, user_id):
        """
        Retrieves the balance of a user based on the user ID.
        """
        try:
            self.open_connection()  # Assumes this is an async call
            with self.connection.cursor() as cursor:  # Assumes self.connection supports async context manager
                cursor.execute(
                    """
                    SELECT balances.total
                    FROM users
                    JOIN balances ON users.user_id = balances.user_id
                    WHERE users.user_id = %s;
                    """, (user_id,))
                balance_data = cursor.fetchone()
                
                balance = balance_data['total'] if balance_data else None
                
                return balance  # Return the fetched balance

        except pymysql.MySQLError as e:  # Replace with your async DB library's exception if different
            logging.error(f"Database operation failed: {e}")
        finally:
            self.close_connection()


    async def change_balance(self, amount, wins, user_id):
        """
        Changes the balance of a user based on the user ID.
        """
        
        try:
            self.open_connection()  # Assumes this is an async call
            with self.connection.cursor() as cursor:  # Assumes self.connection supports async context manager
                # Get the current time in the desired timezone
                desired_timezone = pytz.timezone('Europe/Moscow')
                time_updated = datetime.now(desired_timezone).strftime('%Y-%m-%d %H:%M:%S')

                
                # Execute the SQL query to update the balance
                cursor.execute(
                    """
                    UPDATE balances
                    SET total = total + %s,
                        wins = wins + %s,
                        last_updated = %s
                    WHERE user_id = %s
                    """,
                    (amount, wins, time_updated, user_id),
                )
                # Commit the changes to the database
                self.connection.commit()

                logging.info(f"User balance updated for user_id={user_id}, amount={amount}, wins={wins}")

        except pymysql.MySQLError as e:  # Replace with your async DB library's exception if different
            logging.error(f"Database operation failed: {e}")
        finally:
            self.close_connection()  # Assumes this is an async call

    
    async def change_transactions(self, transaction_type, combination, amount, user_id):
        """
        Asynchronously changes the transactions in the database.
        """
        try:
            self.open_connection()  # Make sure this is an async call
            with self.connection.cursor() as cursor:  # Assumes self.connection supports async context manager
                # Get the current time in the desired timezone
                desired_timezone = pytz.timezone('Europe/Moscow')
                time_updated = datetime.now(desired_timezone).strftime('%Y-%m-%d %H:%M:%S')
                
                # Insert a new record into the 'transactions' table
                cursor.execute(
                    """
                    INSERT INTO transactions (balance_id, transaction_type, combination, amount, last_updated)
                    SELECT balances.balance_id, %s, %s, %s, %s
                    FROM balances
                    WHERE balances.user_id = %s;
                    """,
                    (transaction_type, combination, amount, time_updated, user_id),
                )

                # Commit the changes to the database
                self.connection.commit()

                logging.info(f"Transaction changed for user_id={user_id}, amount={amount}, type={transaction_type}")

        except Exception as e:  # Preferably use a more specific exception
            logging.error(f"Error: {e}")
        finally:
            self.close_connection()  # Make sure this is an async call


    async def give_daily_bonus(self):
        """
        Asynchronously gives a daily bonus to users who have a balance less than 1000.
        """
        try:
            self.open_connection()  # Make sure this is an async call
            with self.connection.cursor() as cursor:  # Assumes self.connection supports async context manager
                # Set the desired timezone and get the current time
                desired_timezone = pytz.timezone('Europe/Moscow')
                time_updated = datetime.now(desired_timezone).strftime('%Y-%m-%d %H:%M:%S')

                # Set the transaction type and amount for the daily bonus
                transaction_type = "Daily Bonus"
                bonus_amount = 1000

                # Insert a new transaction record for each user with a balance less than 1000
                cursor.execute(
                    """
                    INSERT INTO transactions (balance_id, transaction_type, amount, last_updated)
                    SELECT balances.balance_id, %s, %s, %s
                    FROM balances
                    WHERE balances.total < 1000;
                    """,
                    (transaction_type, bonus_amount, time_updated),
                )

                # Update the balance for each user with a balance less than 1000
                cursor.execute(
                    """
                    UPDATE balances
                    SET total = %s, last_updated = %s
                    WHERE total < 1000;
                    """,
                    (bonus_amount, time_updated),
                )
                
                # Commit the changes to the database
                self.connection.commit()

                # Log the transaction
                logging.info(f"Transaction Daily Bonus")

        except Exception as e:  # Replace with more specific exception handling if possible
            logging.error(f"Error: {e}")
        finally:
            self.close_connection()  # Make sure this is an async call

    
    async def get_rating_total(self):
        """
        Retrieves the total rating of the users based on their balances.
        """
        try:
            self.open_connection()  # Make sure this is an async call
            with self.connection.cursor() as cursor:  # Assumes self.connection supports async context manager

                # Execute the SQL query to retrieve the username and total balance of users
                cursor.execute(
                    """
                    SELECT users.username, balances.total
                    FROM balances
                    JOIN users ON balances.user_id = users.user_id
                    ORDER BY balances.total DESC
                    LIMIT 10;
                    """)
                
                # Fetch all the results from the query
                rating = cursor.fetchall()
                return rating

        except Exception as e:  # Replace with more specific exception handling if possible
            logging.error(f"Error: {e}")
        finally:
            self.close_connection()  # Make sure this is an async call

    
    async def get_rating_wins(self):
        """
        Retrieves the top 10 users and their wins from the database.
        """
        try:
            self.open_connection()  # Make sure this is an async call
            with self.connection.cursor() as cursor:  # Assumes self.connection supports async context manager
                cursor.execute(
                    """
                    SELECT users.username, balances.wins
                    FROM balances
                    JOIN users ON balances.user_id = users.user_id
                    ORDER BY balances.wins DESC
                    LIMIT 10;
                    """)
                
                # Fetch all the results from the query
                rating = cursor.fetchall()
                return rating

        except Exception as e:  # Replace with more specific exception handling if possible
            logging.error(f"Error: {e}")
        finally:
            self.close_connection()  # Make sure this is an async call