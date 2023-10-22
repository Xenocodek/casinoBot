from database.database import DatabaseManager

db_manager = DatabaseManager()

async def db_start():
    query = """
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER,
        tg_username TEXT,
        tg_first_name TEXT
    )
    """
    db_manager.cur.execute(query)
    db_manager.db.commit()

async def new_user(user_id, username, first_name):
    user = db_manager.cur.execute(
        "SELECT * FROM accounts WHERE tg_id = ?", (user_id,)
    ).fetchone()
    if not user:
        db_manager.cur.execute(
            "INSERT INTO accounts (tg_id, tg_username, tg_first_name) VALUES (?, ?, ?)",
            (user_id, username, first_name),
        )
        db_manager.db.commit()