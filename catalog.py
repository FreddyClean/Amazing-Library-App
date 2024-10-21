import requests
from tkinter import messagebox

API_BASE_URL = 'https://amazing-library-app-1.onrender.com/'

class Catalog:
    def __init__(self):
        self.books = []

    def fetch_books(self):
        """Fetch all books with availability status from the API"""
        try:
            response = requests.get(f'{API_BASE_URL}/books')
            if response.status_code == 200:
                self.books = response.json()
                # Check availability for each book
                for book in self.books:
                    book['available'] = self.check_availability(book['id'])
                return self.books
            else:
                messagebox.showerror("Error", "Failed to fetch books from the API.")
                return []
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching books: {e}")
            return []

    def search_books(self, query):
        """Filter books based on the search query"""
        query = query.lower()
        return [book for book in self.books if query in book['title'].lower()]

    def get_book_details(self, book_id):
        """Fetch book details from the API"""
        try:
            response = requests.get(f'{API_BASE_URL}/books/{book_id}')
            if response.status_code == 200:
                return response.json()
            else:
                messagebox.showerror("Error", "Failed to fetch book details from the API.")
                return None
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching book details: {e}")
            return None

    def check_availability(self, book_id):
        """Check the availability status of a specific book"""
        try:
            response = requests.get(f'{API_BASE_URL}/check_availability/{book_id}')
            if response.status_code == 200:
                return response.json().get('available', False)
            else:
                messagebox.showerror("Error", "Failed to check availability.")
                return False
        except Exception as e:
            messagebox.showerror("Error", f"Error checking availability: {e}")
            return False