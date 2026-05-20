import sqlite3

def init_db():
    conn = sqlite3.connect('clicker.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT UNIQUE NOT NULL,
            hearts   INTEGER DEFAULT 0,
            cookies  INTEGER DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()

init_db()