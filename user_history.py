import sqlite3

def get_user_history(user_id):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT books.title, books.author, borrowings.borrow_date, borrowings.due_date, borrowings.return_date
        FROM borrowings
        JOIN books ON books.id = borrowings.book_id
        WHERE borrowings.user_id = ?
    """, (user_id,))

    history = cursor.fetchall()
    conn.close()

    return history