import sqlite3
import json

# Load book data from books.json
with open('books.json', 'r') as f:
    books = json.load(f)

# Connect to the library.db database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Step 1: Delete all existing books in the books table
cursor.execute('DELETE FROM books')

# Step 2: Insert books into the books table
for book in books:
    cursor.execute('''
        INSERT INTO books (title, author, year, genre) 
        VALUES (?, ?, ?, ?)
    ''', (book['title'], book['author'], book['published_year'], book['genre']))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Books table reset and new books inserted into the database successfully.")