import sqlite3
import os

# Delete the existing library.db file if it exists
if os.path.exists('library.db'):
    os.remove('library.db')
    print("library.db deleted successfully.")
else:
    print("library.db does not exist.")

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('library.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table for books if it doesn't exist already
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER NOT NULL,
        genre TEXT  -- Added genre column
    )
''')

# Drop the old borrowings table if it exists
cursor.execute('''
    DROP TABLE IF EXISTS borrowings
''')

# Create a new borrowings table with the updated structure
cursor.execute('''
    CREATE TABLE IF NOT EXISTS borrowings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        book_id INTEGER NOT NULL,
        borrow_date TEXT NOT NULL,   -- Date when the book is borrowed
        due_date TEXT NOT NULL,      -- Date when the book is due to be returned
        return_date TEXT DEFAULT NULL,  -- Date when the book is returned (NULL if not returned yet)
        FOREIGN KEY (book_id) REFERENCES books(id)
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database recreated and tables created successfully.")