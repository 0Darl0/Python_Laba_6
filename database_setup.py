import sqlite3

con = sqlite3.connect('account.db')
cur = con.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS telegram_connections (
        telegram_id TEXT PRIMARY KEY,
        owner_id INTEGER NOT NULL,
        telegram_username TEXT,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS task_notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL,
        notification_type TEXT NOT NULL,
        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

con.commit()
con.close()
print("Готово!")