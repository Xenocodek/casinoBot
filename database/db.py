import mysql.connector
import logging
import random
from datetime import datetime

from settings.config import DatabaseConfig
from .queries import *

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
                self.connection = mysql.connector.connect(host=self.host,
                                                port=self.port,
                                                user=self.user,
                                                password=self.password,
                                                db=self.dbname,
                                                charset='utf8mb4')
                # Log a success message if connection is successful
                logging.info('Connection to the database was successful.')
            except mysql.connector.Error as e:
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
                queries = [create_table_users, create_table_balances, create_table_transactions]

                # Execute each query
                for query in queries:
                    try:
                        cursor.execute(query)
                    except mysql.connector.Error as e:
                        logging.error(f'Error executing query: {e}')

                # Commit the changes
                self.connection.commit()
                logging.info('Database tables have been created')

        except mysql.connector.Error as e:
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
                logging.info(f"User ID: {user_id}")
                
                cursor.execute(select_user, (user_id,))
                user = cursor.fetchone()

                if not user:
                    created = datetime.now()
                    amount = 1000
                    wins = 0
                    transaction_type = "Registration"
                    currency = "ALM"
                    
                    # Insert the new user into the 'users' table
                    cursor.execute(insert_new_user, (user_id, username, user_first_name, user_last_name, created))

                    # Generate a unique balance_id and insert user's initial balance in the 'balances' table
                    balance_id = None
                    while balance_id is None:
                        potential_id = random.randint(1000, 9999)
                        cursor.execute(select_potential_id, (potential_id,))
                        existing_balance = cursor.fetchone()
                        if not existing_balance:
                            balance_id = potential_id
                    
                    cursor.execute(insert_new_balance, (balance_id, user_id, amount, wins, currency, created))

                    # Add a transaction record for the initial registration
                    cursor.execute(insert_new_transactions, (balance_id, transaction_type, amount, created))

                    self.connection.commit()
                    logging.info('The request to create a new user has been completed')
                else:
                    logging.info('The user is already in the Database')

        except mysql.connector.Error as e:
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
                cursor.execute(select_admin, (user_id,))
                admin_id = cursor.fetchone()
                
                logging.info('The request to get admins has been completed')
                return admin_id  # Return the fetched user data

        except mysql.connector.Error as e:
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
                cursor.execute(select_user_data, (user_id,))
                user_data = cursor.fetchone()
                
                logging.info('The request to get user data has been completed')
                return user_data  # Return the fetched user data

        except mysql.connector.Error as e:
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
                cursor.execute(select_user_balance, (user_id,))
                balance_data = cursor.fetchone()
                
                balance = balance_data[0] if balance_data else None
                
                return balance  # Return the fetched balance

        except mysql.connector.Error as e:  # Replace with your async DB library's exception if different
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
                time_updated = datetime.now()

                # Execute the SQL query to update the balance
                cursor.execute(update_user_balance, (amount, wins, time_updated, user_id))
                # Commit the changes to the database
                self.connection.commit()

                logging.info(f"User balance updated for user_id={user_id}, amount={amount}, wins={wins}")

        except mysql.connector.Error as e:  # Replace with your async DB library's exception if different
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
                time_updated = datetime.now()
                
                # Insert a new record into the 'transactions' table
                cursor.execute(insert_new_transactions, (transaction_type, combination, amount, time_updated, user_id))

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
                time_updated = datetime.now()

                # Set the transaction type and amount for the daily bonus
                transaction_type = "Daily Bonus"
                bonus_amount = 1000

                # Insert a new transaction record for each user with a balance less than 1000
                cursor.execute(insert_daily_transaction, (transaction_type, bonus_amount, time_updated))

                # Update the balance for each user with a balance less than 1000
                cursor.execute(update_daily_balance, (bonus_amount, time_updated))
                
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
                cursor.execute(select_rating_total)
                
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
                cursor.execute(select_rating_wins)
                
                # Fetch all the results from the query
                rating = cursor.fetchall()
                return rating

        except Exception as e:  # Replace with more specific exception handling if possible
            logging.error(f"Error: {e}")
        finally:
            self.close_connection()  # Make sure this is an async call