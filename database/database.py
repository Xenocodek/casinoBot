import sqlite3 as sq

class DatabaseManager:
    def __init__(self, db_file='database/casino_bot.db'):
        try:
            self.db = sq.connect(db_file)
            self.cur = self.db.cursor()
        except sq.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")