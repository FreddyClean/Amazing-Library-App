from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn

# Fetch all books
@app.route('/books', methods=['GET'])
def get_books():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return jsonify([dict(row) for row in books]), 200

# Fetch a single book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    conn.close()
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(dict(book)), 200

# Borrow a book (with borrow_date and due_date)
@app.route('/borrow', methods=['POST'])
def borrow_book():
    data = request.get_json()

    # Input validation
    book_id = data.get('book_id')
    user_id = data.get('user_id')
    borrow_date = data.get('borrow_date')
    due_date = data.get('due_date')

    if not all([book_id, user_id, borrow_date, due_date]):
        return jsonify({"error": "Missing data, please provide book_id, user_id, borrow_date, and due_date"}), 400

    conn = get_db_connection()
    # Check if the book is already borrowed and not yet returned
    borrowed = conn.execute('SELECT * FROM borrowings WHERE book_id = ? AND return_date IS NULL', (book_id,)).fetchone()
    
    if borrowed:
        conn.close()
        return jsonify({"error": "Book already borrowed"}), 400

    # If not borrowed, add a record to the borrowings table
    conn.execute(
        'INSERT INTO borrowings (user_id, book_id, borrow_date, due_date) VALUES (?, ?, ?, ?)', 
        (user_id, book_id, borrow_date, due_date)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Book borrowed successfully!"}), 200

# Return a book (with return_date)
@app.route('/return', methods=['POST'])
def return_book():
    data = request.get_json()

    # Input validation
    book_id = data.get('book_id')
    user_id = data.get('user_id')
    return_date = data.get('return_date')

    if not all([book_id, user_id, return_date]):
        return jsonify({"error": "Missing data, please provide book_id, user_id, and return_date"}), 400

    conn = get_db_connection()
    # Check if the book is borrowed by this user and not yet returned
    borrowed = conn.execute(
        'SELECT * FROM borrowings WHERE book_id = ? AND user_id = ? AND return_date IS NULL',
        (book_id, user_id)
    ).fetchone()
    
    if not borrowed:
        conn.close()
        return jsonify({"error": "Book not borrowed by this user or already returned"}), 400

    # Update the return_date in the borrowings table
    conn.execute(
        'UPDATE borrowings SET return_date = ? WHERE id = ?', 
        (return_date, borrowed['id'])
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Book returned successfully!"}), 200

# Check book availability
@app.route('/check_availability/<int:book_id>', methods=['GET'])
def check_availability(book_id):
    conn = get_db_connection()
    borrowed = conn.execute('SELECT * FROM borrowings WHERE book_id = ? AND return_date IS NULL', (book_id,)).fetchone()
    conn.close()

    if borrowed:
        return jsonify({"available": False}), 200
    else:
        return jsonify({"available": True}), 200

if __name__ == '__main__':
    app.run(debug=True)