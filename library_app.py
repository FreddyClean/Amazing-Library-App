import customtkinter as ctk
from tkinter import messagebox
from authentication import login_user, sign_up_user  # Import updated authentication functions
from library_user_interface import LibraryUI
from PIL import Image

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library App")
        self.root.geometry("800x600")

        # Set customtkinter appearance and theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Define colors similar to library_user_interface.py
        self.bg_color = "#2e2e2e"
        self.fg_color = "#f0c36c"
        self.button_bg_color = "#f0c36c"
        self.button_fg_color = "#4b3d2d"

        self.background_label = None

        # Show the login screen first
        self.show_login_screen()

        # Bind resize event to adjust background image when the window is resized
        self.root.bind("<Configure>", self.on_resize)

    def show_login_screen(self):
        self.clear_window()
        self.add_background_image()

        # Login label
        login_label = ctk.CTkLabel(self.root, text="Library Login", font=("Arial", 24), text_color=self.fg_color)
        login_label.pack(pady=20)

        # Username
        username_label = ctk.CTkLabel(self.root, text="Username:", text_color=self.fg_color)
        username_label.pack(pady=5)
        self.username_entry = ctk.CTkEntry(self.root)
        self.username_entry.pack(pady=5)

        # Password
        password_label = ctk.CTkLabel(self.root, text="Password:", text_color=self.fg_color)
        password_label.pack(pady=5)
        self.password_entry = ctk.CTkEntry(self.root, show='*')
        self.password_entry.pack(pady=5)

        # Login button
        login_button = ctk.CTkButton(self.root, text="Login", command=self.login_user, fg_color=self.button_bg_color, text_color=self.button_fg_color)
        login_button.pack(pady=10)

        # Sign-up button
        signup_button = ctk.CTkButton(self.root, text="Sign Up", command=self.show_signup_screen, fg_color=self.button_bg_color, text_color=self.button_fg_color)
        signup_button.pack(pady=5)

    def add_background_image(self):
        try:
            # Load the background image using PIL
            background_image = Image.open("loginscreen.jpg")
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

            self.background_label.lower()  # Send the background image to the back
        except Exception as e:
            print("Error loading background image:", e)

    def on_resize(self, event):
        # Reapply the background image when the window is resized
        self.add_background_image()

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if login_user(username, password):  # API call to login
            messagebox.showinfo("Login Successful", f"Welcome {username}!")
            self.load_library_ui(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def show_signup_screen(self):
        self.clear_window()
        self.add_background_image()

        # Sign-up label
        signup_label = ctk.CTkLabel(self.root, text="Sign Up", font=("Arial", 24), text_color=self.fg_color)
        signup_label.pack(pady=20)

        # Username
        username_label = ctk.CTkLabel(self.root, text="Choose a Username:", text_color=self.fg_color)
        username_label.pack(pady=5)
        self.username_entry = ctk.CTkEntry(self.root)
        self.username_entry.pack(pady=5)

        # Password
        password_label = ctk.CTkLabel(self.root, text="Choose a Password:", text_color=self.fg_color)
        password_label.pack(pady=5)
        self.password_entry = ctk.CTkEntry(self.root, show='*')
        self.password_entry.pack(pady=5)

        # Sign-up button
        signup_button = ctk.CTkButton(self.root, text="Sign Up", command=self.sign_up_user, fg_color=self.button_bg_color, text_color=self.button_fg_color)
        signup_button.pack(pady=10)

    def sign_up_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if sign_up_user(username, password):  # API call to register
            messagebox.showinfo("Sign Up Successful", "You can now log in with your new account.")
            self.show_login_screen()
        else:
            messagebox.showerror("Sign Up Failed", "Username already exists.")

    def load_library_ui(self, username):
        # Load the main library UI once the user logs in
        LibraryUI(self.root, username)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    app = LibraryApp(root)
    root.mainloop()