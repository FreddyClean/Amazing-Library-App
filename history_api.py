from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('user_history.db')
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

@app.route('/user_history', methods=['POST'])
def add_user_history():
    data = request.get_json()
    user_id = data['user_id']
    book_title = data['book_title']
    author_name = data['author_name']
    borrowed_date = data['borrowed_date']
    due_date = data['due_date']
    return_date = data.get('return_date')  # Optional

    # Here you may want to validate user_id against the Users API or database

    conn = get_db_connection()
    conn.execute('INSERT INTO user_history (user_id, book_title, author_name, borrowed_date, due_date, return_date) VALUES (?, ?, ?, ?, ?, ?)',
                 (user_id, book_title, author_name, borrowed_date, due_date, return_date))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"}), 201

@app.route('/user_history/<int:user_id>', methods=['GET'])
def get_user_history(user_id):
    conn = get_db_connection()
    user_history = conn.execute('SELECT * FROM user_history WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()
    
    return jsonify([dict(history) for history in user_history]), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)