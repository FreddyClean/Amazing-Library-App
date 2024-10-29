import sqlite3

def get_user_history(user_id):
    conn = sqlite3.connect("user_history.db")  # Connect to the local user history database
    cursor = conn.cursor()

    cursor.execute("""
        SELECT book_title, author_name, borrowed_date, due_date, return_date, book_id
        FROM user_history
        WHERE user_id = ?
    """, (user_id,))

    history = cursor.fetchall()
    conn.close()

    return history