import sqlite3

conn = sqlite3.connect('user_history.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(user_history)")
columns = cursor.fetchall()
conn.close()

for column in columns:
    print(column)