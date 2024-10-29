import customtkinter as ctk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image
from borrowing_system import BorrowingSystem
from catalog import Catalog
from user_history import get_user_history
import datetime

class LibraryUI:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.borrowing_system = BorrowingSystem()
        self.catalog = Catalog()
        self.background_label = None
        self.resize_job = None
        self.loading_label = None

        # Set customtkinter appearance and theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Define colors
        self.bg_color = "#2e2e2e"
        self.fg_color = "#f0c36c"
        self.button_bg_color = "#f0c36c"
        self.button_fg_color = "#4b3d2d"

        self.create_ui()

        # Bind resize event to adjust background image when the window is resized
        self.root.bind("<Configure>", self.on_resize)

    def show_loading_screen(self):
        """Displays a loading screen."""
        self.loading_label = ctk.CTkLabel(
            self.root,
            text="Loading, please wait...",
            font=("Arial", 20),
            text_color=self.fg_color,
            fg_color=self.bg_color
        )
        self.loading_label.place(relx=0.5, rely=0.5, anchor="center")
        self.root.update()  # Force update the UI to immediately show the loading label

    def hide_loading_screen(self):
        """Removes the loading screen."""
        if self.loading_label:
            self.loading_label.destroy()
            self.loading_label = None

    def create_ui(self):
        self.show_loading_screen()  # Show loading screen while preparing UI
        self.clear_window()

        # Set background image
        self.add_background_image()

        # Welcome message
        welcome_label = ctk.CTkLabel(
            self.root,
            text=f"Welcome to the Library System, {self.username}!",
            font=("Arial", 24),
            text_color=self.fg_color,
            fg_color=self.bg_color
        )
        welcome_label.pack(pady=20)

        # Frame to hold the buttons in a grid layout
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=20)

        # Create buttons
        button_style = {
            'font': ("Arial", 16),
            'fg_color': self.button_bg_color,
            'text_color': self.button_fg_color,
            'width': 200,
            'height': 40
        }

        buttons = [
            ("Borrow a Book", self.borrow_book),
            ("Return a Book", self.return_book),
            ("Check Availability", self.check_availability),
            ("User History", self.user_history),
            ("Search Catalog", self.search_catalog),
            ("Sign Out", self.sign_out),
            ("Exit", self.exit_application)
        ]

        # Arrange buttons in a 2-column grid
        for idx, (text, command) in enumerate(buttons):
            row = idx // 2
            col = idx % 2
            button = ctk.CTkButton(button_frame, text=text, command=command, **button_style)
            button.grid(row=row, column=col, padx=10, pady=10)

        self.hide_loading_screen()  # Hide loading screen once everything is ready

    def add_background_image(self):
        try:
            # Load the background image using PIL
            background_image = Image.open("AMAZING LIBRARY/imagesLIBRARY/oioi.jpeg")
            # Create CTkImage for High DPI support
            background_ctk_image = ctk.CTkImage(
                light_image=background_image,  # Use the same image for light and dark modes
                dark_image=background_image,  # Alternatively, provide different images for each mode
                size=(self.root.winfo_width(), self.root.winfo_height())  # Automatically scale based on window size
            )

            if self.background_label:
                self.background_label.configure(image=background_ctk_image)
            else:
                self.background_label = ctk.CTkLabel(self.root, image=background_ctk_image, fg_color=self.bg_color)
                self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

            self.background_label.lower()
        except Exception as e:
            print("Error loading background image:", e)

    def on_resize(self, event):
        if self.resize_job is not None:
            self.root.after_cancel(self.resize_job)
        self.resize_job = self.root.after(100, self.add_background_image)

    def borrow_book(self):
        book_id = self.get_book_id("Enter the Book ID to borrow:")
        if book_id:
            user_id = self.username
            book_details = self.catalog.get_book_details(book_id)
            book_title = book_details['title']
            author_name = book_details['author']

            if messagebox.askyesno("Confirm Borrow", f"Do you want to borrow '{book_title}' by {author_name}?"):
                if self.borrowing_system.borrow_book(book_id, user_id, book_title, author_name):
                    due_date = (datetime.date.today() + datetime.timedelta(days=14)).strftime('%Y-%m-%d')
                    messagebox.showinfo("Success", f"Book borrowed successfully!\nDue Date: {due_date}")
                else:
                    messagebox.showerror("Error", "This book is currently borrowed by another person.")

    def return_book(self):
        book_id = self.get_book_id("Enter the Book ID to return:")
        if book_id:
            user_id = self.username
            book_details = self.catalog.get_book_details(book_id)
            book_title = book_details['title']
            author_name = book_details['author']

            if messagebox.askyesno("Confirm Return", f"Do you want to return '{book_title}' by {author_name}?"):
                if self.borrowing_system.return_book(book_id, user_id):
                    messagebox.showinfo("Success", "Book returned successfully!")
                else:
                    messagebox.showerror("Error", "Failed to return book.")

    def check_availability(self):
        book_id = self.get_book_id("Enter the Book ID to check availability:")
        if book_id:
            available = self.catalog.check_availability(book_id)
            if available:
                messagebox.showinfo("Available", "The book is available.")
            else:
                messagebox.showinfo("Not Available", "The book is not available.")

    def user_history(self):
        history_window = ctk.CTkToplevel(self.root)
        history_window.title("Borrowing History")
        history_window.geometry("800x400")

        tree = ttk.Treeview(history_window, columns=('Title', 'Author', 'Borrow Date', 'Due Date', 'Return Date'), show='headings')
        tree.heading('Title', text='Title')
        tree.heading('Author', text='Author')
        tree.heading('Borrow Date', text='Borrow Date')
        tree.heading('Due Date', text='Due Date')
        tree.heading('Return Date', text='Return Date')
        tree.pack(pady=10, fill='both', expand=True)

        tree.column('Title', width=200, anchor='w')
        tree.column('Author', width=150, anchor='w')
        tree.column('Borrow Date', width=100, anchor='center')
        tree.column('Due Date', width=100, anchor='center')
        tree.column('Return Date', width=100, anchor='center')

        user_id = self.username  # Assuming `username` is the user ID
        history = get_user_history(user_id)

        for record in history:
            tree.insert('', 'end', values=record)

    def search_catalog(self):
        catalog_window = ctk.CTkToplevel(self.root)
        catalog_window.title("Search Catalog")
        catalog_window.geometry("800x500")

        search_label = ctk.CTkLabel(catalog_window, text="Search by Title:", text_color=self.fg_color, fg_color=self.bg_color)
        search_label.pack(pady=5)
        search_entry = ctk.CTkEntry(catalog_window, width=50)
        search_entry.pack(pady=5)

        tree = ttk.Treeview(catalog_window, columns=('ID', 'Title', 'Author', 'Genre', 'Available'), show='headings')
        tree.heading('ID', text='ID')
        tree.heading('Title', text='Title')
        tree.heading('Author', text='Author')
        tree.heading('Genre', text='Genre')
        tree.heading('Available', text='Available')
        tree.pack(pady=10, fill='both', expand=True)

        tree.column('ID', width=100, anchor='center')
        tree.column('Title', width=200, anchor='w')
        tree.column('Author', width=150, anchor='w')
        tree.column('Genre', width=100, anchor='w')
        tree.column('Available', width=100, anchor='center')

        def update_tree(books):
            for row in tree.get_children():
                tree.delete(row)

            for book in books:
                availability = "Yes" if book.get('available', False) else "No"
                tree.insert('', 'end', values=(book['id'], book['title'], book['author'], book['genre'], availability))

        def search_books():
            query = search_entry.get()
            if query:
                books = self.catalog.search_books(query)
                update_tree(books)
            else:
                update_tree(self.catalog.fetch_books())

        search_button = ctk.CTkButton(catalog_window, text="Search", command=search_books, fg_color=self.button_bg_color, text_color=self.button_fg_color)
        search_button.pack(pady=5)

        update_tree(self.catalog.fetch_books())

    def get_book_id(self, prompt):
        return simpledialog.askinteger("Input", prompt)

    def sign_out(self):
        self.show_loading_screen()  # Show loading screen during sign out transition
        self.clear_window()

        from library_app import LibraryApp  # Import the login screen here
        LibraryApp(self.root)  # Reinitialize the login screen

        self.hide_loading_screen()  # Hide loading screen after loading the login screen

    def exit_application(self):
        self.root.quit()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
