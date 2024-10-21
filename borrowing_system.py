import requests
import datetime

API_BASE_URL = 'https://amazing-library-app-1.onrender.com/'

class BorrowingSystem:
    def __init__(self):
        self.borrowed_books = {}

    def borrow_book(self, book_id, user_id):
        try:
            borrow_date = datetime.date.today().strftime('%Y-%m-%d')
            due_date = (datetime.date.today() + datetime.timedelta(days=14)).strftime('%Y-%m-%d')

            # Make a request to borrow the book and pass the user ID, borrow_date, and due_date
            response = requests.post(f"{API_BASE_URL}/borrow", json={'book_id': book_id, 'user_id': user_id, 'borrow_date': borrow_date, 'due_date': due_date})
            if response.status_code == 200:
                self.borrowed_books[book_id] = user_id
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
                return True
            else:
                error_msg = response.json().get("error", "Unknown error occurred.")
                print(f"Return error: {error_msg}")
                return False
        except Exception as e:
            print(f"Error returning book: {e}")
            return False