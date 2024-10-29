import sqlite3

def create_database():
    # Connect to SQLite database (it will create it if it doesn't exist)
    conn = sqlite3.connect('user_history.db')  
    cursor = conn.cursor()

    # Create user_history table with additional fields, including book_id
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            book_id INTEGER,  -- Added book_id column
            book_title TEXT NOT NULL,
            author_name TEXT NOT NULL,
            borrowed_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            return_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)  -- Assuming you have a users table
        )
    ''')

    print("Database and table with book_id column created successfully.")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()