import requests
import datetime
import sqlite3

API_BASE_URL = 'https://amazing-library-app-1.onrender.com/'

class BorrowingSystem:
    def __init__(self):
        self.borrowed_books = {}
        self.db_connection = sqlite3.connect('user_history.db')
        self.db_cursor = self.db_connection.cursor()
        self._create_tables()

    def _create_tables(self):
        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_title TEXT NOT NULL,
                book_id INTEGER NOT NULL,
                author_name TEXT NOT NULL,
                borrowed_date TEXT NOT NULL,
                due_date TEXT NOT NULL,
                return_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        self.db_connection.commit()

    def borrow_book(self, book_id, user_id, book_title, author_name):
        try:
            borrow_date = datetime.date.today().strftime('%Y-%m-%d')
            due_date = (datetime.date.today() + datetime.timedelta(days=14)).strftime('%Y-%m-%d')

            # Make a request to borrow the book and pass the user ID, borrow_date, and due_date
            response = requests.post(f"{API_BASE_URL}/borrow", json={'book_id': book_id, 'user_id': user_id, 'borrow_date': borrow_date, 'due_date': due_date})
            if response.status_code == 200:
                self.borrowed_books[book_id] = user_id
                self._log_borrow_action(user_id, book_id, book_title, author_name, borrow_date, due_date)
                return True
            else:
                error_msg = response.json().get("error", "Unknown error occurred.")
                print(f"Borrow error: {error_msg}")
                return False
        except Exception as e:
            print(f"Error borrowing book: {e}")
            return False

    def return_book(self, book_id, user_id):
        try:
            return_date = datetime.date.today().strftime('%Y-%m-%d')

            # Make a request to return the book and pass the user ID and return_date
            response = requests.post(f"{API_BASE_URL}/return", json={'book_id': book_id, 'user_id': user_id, 'return_date': return_date})
            if response.status_code == 200:
                if book_id in self.borrowed_books:
                    del self.borrowed_books[book_id]
                self._log_return_action(user_id, book_id, return_date)
                return True
            else:
                error_msg = response.json().get("error", "Unknown error occurred.")
                print(f"Return error: {error_msg}")
                return False
        except Exception as e:
            print(f"Error returning book: {e}")
            return False

    def _log_borrow_action(self, user_id, book_id, book_title, author_name, borrow_date, due_date):
        self.db_cursor.execute('''
            INSERT INTO user_history (user_id, book_title, book_id, author_name, borrowed_date, due_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, book_title, book_id, author_name, borrow_date, due_date))
        self.db_connection.commit()

    def _log_return_action(self, user_id, book_id, return_date):
        self.db_cursor.execute('''
            UPDATE user_history
            SET return_date = ?
            WHERE user_id = ? AND book_id = ? AND return_date IS NULL
        ''', (return_date, user_id, book_id))
        self.db_connection.commit()