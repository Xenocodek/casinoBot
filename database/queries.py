create_table_users = """CREATE TABLE IF NOT EXISTS users (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id VARCHAR(64) NOT NULL UNIQUE,
                    username VARCHAR(64),
                    user_first_name VARCHAR(64),
                    registration_date TIMESTAMP,
                    is_admin BOOLEAN DEFAULT FALSE,
                    default_language VARCHAR(2) DEFAULT 'RU'
                    );"""

create_table_balances = """CREATE TABLE IF NOT EXISTS balances (
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        balance_id INT NOT NULL UNIQUE,
                        user_id VARCHAR(64),
                        total REAL,
                        wins INT,
                        currency VARCHAR(3),
                        last_updated TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
                        );"""

create_table_transactions = """CREATE TABLE IF NOT EXISTS transactions (
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        balance_id INT,
                        transaction_type VARCHAR(64),
                        combination VARCHAR(64) DEFAULT '',
                        amount REAL,
                        last_updated TIMESTAMP,
                        FOREIGN KEY (balance_id) REFERENCES balances(balance_id)
                        );"""


select_user = "SELECT * FROM users WHERE user_id = %s"

insert_new_user = """
                INSERT INTO users (user_id, username, user_first_name, registration_date) 
                VALUES (%s, %s, %s, %s);
                """

select_potential_id = "SELECT id FROM balances WHERE balance_id = %s"

insert_new_balance = """
                    INSERT INTO balances (balance_id, user_id, total, wins, currency, last_updated) 
                    VALUES (%s, %s, %s, %s, %s, %s);
                    """

insert_new_transactions = """
                        INSERT INTO transactions (balance_id, transaction_type, amount, last_updated) 
                        VALUES (%s, %s, %s, %s);
                        """

select_admin = """
                SELECT user_id 
                FROM users 
                WHERE user_id = %s AND is_admin = 1;
                """

select_user_data = """
                    SELECT users.user_id, users.username, balances.total, balances.wins
                    FROM users
                    JOIN balances ON users.user_id = balances.user_id
                    WHERE users.user_id = %s;
                    """

select_user_balance = """
                    SELECT balances.total
                    FROM users
                    JOIN balances ON users.user_id = balances.user_id
                    WHERE users.user_id = %s;
                    """

update_user_balance = """
                    UPDATE balances
                    SET total = total + %s,
                        wins = wins + %s,
                        last_updated = %s
                    WHERE user_id = %s;
                    """

insert_transactions = """
                        INSERT INTO transactions (balance_id, transaction_type, combination, amount, last_updated)
                        SELECT balances.balance_id, %s, %s, %s, %s
                        FROM balances
                        WHERE balances.user_id = %s;
                        """

insert_daily_transaction = """
                        INSERT INTO transactions (balance_id, transaction_type, amount, last_updated)
                        SELECT balances.balance_id, %s, %s, %s
                        FROM balances
                        WHERE balances.total < 1000;
                        """

update_daily_balance = """
                    UPDATE balances
                    SET total = %s, last_updated = %s
                    WHERE total < 1000;
                    """

select_rating_total = """
                    SELECT users.username, balances.total
                    FROM balances
                    JOIN users ON balances.user_id = users.user_id
                    ORDER BY balances.total DESC
                    LIMIT 10;
                    """

select_rating_wins = """
                    SELECT users.username, balances.wins
                    FROM balances
                    JOIN users ON balances.user_id = users.user_id
                    ORDER BY balances.wins DESC
                    LIMIT 10;
                    """