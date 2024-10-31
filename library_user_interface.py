import customtkinter as ctk
from tkinter import messagebox, simpledialog, ttk, Scale, Toplevel
from PIL import Image, ImageTk
from borrowing_system import BorrowingSystem
from catalog import Catalog
from user_history import get_user_history
import datetime
import pygame
import threading
import time
import itertools

class LibraryUI:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.borrowing_system = BorrowingSystem()
        self.catalog = Catalog()
        self.catalog.fetch_books()
        self.background_label = ctk.CTkLabel(self.root, fg_color=None) 
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1) 
        self.resize_job = None
        self.loading_label = None
        self.sound_effect_volume = 0.5
        self.background_music_volume = 0.5
        self.is_halloween_theme = False

      
        pygame.mixer.init()
        self.button_sound = pygame.mixer.Sound("CB.mp3")
        self.spooky_sound = pygame.mixer.Sound("JackLaugh.mp3")
        self.default_bgm = ("BGM.mp3")
        self.halloween_bgm = ("HalloweenBGM.mp3")
        
        self.button_sound.set_volume(self.sound_effect_volume)
        self.spooky_sound.set_volume(self.sound_effect_volume)
        
        self.play_bgm()
        
    
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

   
        self.bg_color = "#f0c36c"
        self.fg_color = "#4b3d2d"
        self.button_bg_color = "#f0c36c"
        self.button_fg_color = "#4b3d2d"
        self.halloween_button_bg_color = "#ff7518"
        self.halloween_button_fg_color = "#000000"

    
        self.create_ui()
        self.root.bind("<Configure>", self.on_resize)
        
    def start_ui(self):
        """Initialize the main UI components."""
        time.sleep(2) 
        self.root.after(0, self.finish_initialization)
        
    def finish_initialization(self):
        """Finishes initialization by playing BGM and loading the main interface."""
        self.play_bgm() 
        self.add_background_image()
        self.show_main_screen() 
        self.hide_loading_screen()

    def play_bgm(self):
        """Plays theme-specific background music based on the current theme setting."""
        try:
            music_file = "HalloweenBGM.mp3" if self.is_halloween_theme else "BGM.mp3"
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(self.background_music_volume)
            pygame.mixer.music.play(loops=-1)
        except Exception as e:
            print("Error playing background music:", e)
            
    def play_click_sound(self):
        """Plays spooky sound effect if toggling Halloween theme, otherwise plays button sound."""
        try:
            sound = self.spooky_sound if self.is_halloween_theme else self.button_sound
            sound.set_volume(self.sound_effect_volume)
            sound.play()
        except Exception as e:
            print("Error playing sound:", e)
            
    def play_sound_then_execute(self, command):
        """Plays sound effect and then executes the command."""
        self.play_click_sound()
        self.root.after(100, command)

    def show_loading_screen(self):
        """Shows a loading screen while the UI is being created."""
        self.loading_label = ctk.CTkLabel(
            self.root,
            text="Loading, please wait...",
            font=("Papyrus", 20, "bold"),
            text_color=self.fg_color,
            fg_color=self.bg_color
        )
        self.loading_label.place(relx=0.5, rely=0.5, anchor="center")
        self.root.update()

    def hide_loading_screen(self):
        """Hides the loading screen."""
        if self.loading_label:
            self.loading_label.destroy()
            self.loading_label = None

    def clear_window(self, exclude_background=False):
        """Clears the main window, excluding the background image if specified."""
        for widget in self.root.winfo_children():
            if exclude_background and widget == self.background_label:
                continue
            widget.destroy()

    def add_background_image(self):
        """Adds or updates the background image based on the current theme."""
        background_image_path = "HalloweenMain.png" if self.is_halloween_theme else "oioi.jpeg"

        try:
    
            bg_image = Image.open(background_image_path)
            bg_image = bg_image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.ANTIALIAS)
            self.bg_image = ImageTk.PhotoImage(bg_image)
            
       
            self.background_label.configure(image=self.bg_image)
            self.background_label.image = self.bg_image  
            self.background_label.lower() 
        except Exception as e:
            print(f"Error loading background image: {e}")
            
    def create_ui(self):
        """Creates the main menu UI."""
        self.show_loading_screen()
        self.clear_window(exclude_background=True)
        self.add_background_image()

        self.welcome_label = ctk.CTkLabel(
            self.root,
            text=f"Welcome to the Library System, {self.username}!",
            font=("Papyrus", 24, "bold"),
            text_color=self.fg_color,
            fg_color="#000000"
        )
        self.welcome_label.pack(pady=40)
        self.start_glow()

        button_style = {
            'font': ("Papyrus", 16, "bold"),
            'fg_color': self.button_bg_color,
            'text_color': self.button_fg_color,
            'width': 200,
            'height': 40
        }
        
        self.ui_buttons = []

        buttons = [
            ("Borrow a Book", self.borrow_book),
            ("Return a Book", self.return_book),
            ("Check Availability", self.check_availability),
            ("User History", self.user_history),
            ("Search Catalog", self.search_catalog),
            ("Exit", self.exit_application),
            ("Adjust Volume", self.show_volume_control)
        ]

        for idx, (text, command) in enumerate(buttons):
            button = ctk.CTkButton(
                self.root, 
                text=text,
                command=lambda cmd=command: self.play_sound_then_execute(cmd),
                **button_style
            )
            button.pack(padx=10, pady=(50, 10))
            self.ui_buttons.append(button)

        self.toggle_theme_button = ctk.CTkButton(
            self.root,
            text="Toggle Halloween Theme",
            command=lambda: self.play_sound_then_execute(self.toggle_theme),
            **button_style
        )
        self.toggle_theme_button.place(relx=0.95, rely=0.95, anchor="se")
        self.ui_buttons.append(self.toggle_theme_button)

        self.hide_loading_screen()
        
    def start_glow(self):
        # Create a cycle of colors to mimic a glowing effect
        color_cycle = itertools.cycle(["#4deeea", "#74ee15", "#ffe700", "#f000ff", "#001eff"])
        
        def glow():
            next_color = next(color_cycle)
            self.welcome_label.configure(text_color=next_color)
            self.root.after(500, glow)  # Adjust 500ms to control glow speed

        glow()
        
    def init_ui(self):
        # Use themed colors for the buttons
        borrow_button = ctk.CTkButton(
            self.root,
            text="Borrow Book",
            fg_color=self.get_button_bg_color(),
            text_color=self.get_button_fg_color(),
        )
        borrow_button.place(relx=0.5, rely=0.4, anchor='center')      
        
    def update_button_theme_colors(self):
        """Updates the button colors based on the current theme setting."""
        button_bg_color = self.halloween_button_bg_color if self.is_halloween_theme else self.button_bg_color
        button_fg_color = self.halloween_button_fg_color if self.is_halloween_theme else self.button_fg_color

        # Update colors for each button created in `create_ui`
        for button in self.ui_buttons:
            button.configure(fg_color=button_bg_color, text_color=button_fg_color)
        
        self.toggle_theme_button.configure(fg_color=button_bg_color, text_color=button_fg_color)
        
    def get_button_bg_color(self):
        return self.halloween_button_bg_color if self.is_halloween_theme else self.button_bg_color

    def get_button_fg_color(self):
        return self.halloween_button_fg_color if self.is_halloween_theme else self.button_fg_color

    def show_volume_control(self):
        """Switches to the volume control slide in the main window."""
        self.clear_window(exclude_background=True)
        self.add_background_image()

        volume_label = ctk.CTkLabel(self.root, text="Volume Settings", font=("Papyrus", 20, "bold"), text_color=self.fg_color)
        volume_label.pack(pady=20)

        se_volume_label = ctk.CTkLabel(self.root, text="Sound Effects Volume", font=("Papyrus", 16, "bold"), text_color=self.fg_color)
        se_volume_label.pack(pady=10)
        
        se_volume_slider = ctk.CTkSlider(
            self.root,
            from_=0,
            to=1,
            number_of_steps=10,
            command=self.set_sound_effect_volume
        )
        se_volume_slider.set(self.sound_effect_volume)   
        se_volume_slider.pack(pady=10)
        
        bgm_volume_label = ctk.CTkLabel(self.root, text="Background Music Volume", font=("Papyrus", 16, "bold"), text_color=self.fg_color)
        bgm_volume_label.pack(pady=10)
        
        bgm_volume_slider = ctk.CTkSlider(
            self.root,
            from_=0,
            to=1,
            number_of_steps=10,
            command=self.set_bgm_volume
        )
        
        bgm_volume_slider.set(self.background_music_volume)
        bgm_volume_slider.pack(pady=10)
        
        back_button = ctk.CTkButton(
            self.root,
            text="Back to Main Menu",
            command=lambda: self.play_sound_then_execute(lambda: self.create_ui()),
            font=("Papyrus", 20, "bold"),
            fg_color=self.button_bg_color,
            text_color=self.button_fg_color
        )
        back_button.pack(pady=20)

    def set_sound_effect_volume(self, volume):
        """Sets the volume for sound effects."""
        self.sound_effect_volume = volume
        self.button_sound.set_volume(volume)
        self.spooky_sound.set_volume(volume)

    def set_bgm_volume(self, volume):
        """Sets the volume for background music."""
        self.background_music_volume = float(volume)
        pygame.mixer.music.set_volume(self.background_music_volume)
        
    def add_background_image(self):
        try:
    
            image_file = "HalloweenMain.png" if self.is_halloween_theme else "oioi.jpeg"
        
            background_image = Image.open(image_file)
            background_ctk_image = ctk.CTkImage(
                light_image=background_image,
                dark_image=background_image,
                size=(self.root.winfo_width(), self.root.winfo_height())
            )
     
            self.background_label.configure(image=background_ctk_image)
            self.background_label.image = background_ctk_image 
            self.background_label.lower() 
        except Exception as e:
            print(f"Error loading background image: {e}")
        
    def toggle_theme(self):
        """Toggles between Halloween and default theme, showing a loading screen during the transition."""
        self.show_loading_screen()
        threading.Thread(target=self.apply_theme_change).start()

    def apply_theme_change(self):
        """Applies the theme change by stopping current music, toggling the theme flag, and adding a delay."""
        self.is_halloween_theme = not self.is_halloween_theme
        pygame.mixer.music.stop() 
        time.sleep(2) 
        self.root.after(0, self.finish_theme_change) 

    def finish_theme_change(self):
        """Completes the theme change by updating the background image, playing background music, and hiding the loading screen."""
        self.add_background_image() 
        self.play_bgm()  
        self.update_button_theme_colors()
        self.hide_loading_screen() 
            
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

        user_id = self.username  
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

    def exit_application(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.quit()

    def get_book_id(self, prompt):
        book_id = simpledialog.askstring("Book ID", prompt)
        return book_id

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1024x768")
    LibraryUI(root, username="Guest")
    root.mainloop()