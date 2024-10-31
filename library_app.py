import customtkinter as ctk
from tkinter import messagebox
from authentication import login_user, sign_up_user
from library_user_interface import LibraryUI
from PIL import Image
import pygame
import threading
import time
import itertools


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library App")
        self.root.geometry("800x600")

        pygame.mixer.init()
        self.default_click_sound = pygame.mixer.Sound("CB.mp3")
        self.spooky_click_sound = pygame.mixer.Sound("JackLaugh.mp3")
        self.default_bgm = "BGM.mp3"
        self.halloween_bgm = "HalloweenBGM.mp3"
        pygame.mixer.music.load(self.default_bgm)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Theme colors and fonts
        self.bg_color = "#2e2e2e"
        self.fg_color = "#f0c36c"
        self.button_bg_color = "#f0c36c"
        self.button_fg_color = "#4b3d2d"
        self.halloween_button_bg_color = "#ff7518"
        self.halloween_button_fg_color = "#000000"
        self.font_style = ("Papyrus", 16, "bold")
        self.header_font_style = ("Papyrus", 24, "bold")

        self.is_halloween_theme = False

        # Volume settings
        self.sound_effect_volume = 0.5
        self.background_music_volume = 0.5

        # Loading screen
        self.loading_label = None
        self.show_loading_screen()
        threading.Thread(target=self.initialize_app).start()

        # Background label created once and reused
        self.background_label = ctk.CTkLabel(self.root, fg_color=None)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Event binding for resizing
        self.root.bind("<Configure>", self.on_resize)

    def show_loading_screen(self):
        """Display a loading overlay on the main window."""
        self.loading_label = ctk.CTkLabel(
            self.root,
            text="Loading, please wait...",
            font=("Papyrus", 24, "bold"),
            text_color="#FFFFFF",
        )
        self.loading_label.place(relx=0.5, rely=0.5, anchor="center")
        self.root.update_idletasks()

    def hide_loading_screen(self):
        """Remove the loading overlay once initialization is complete."""
        if self.loading_label:
            self.loading_label.destroy()

    def initialize_app(self):
        """Initialize main app components after showing the loading screen."""
        time.sleep(4)  # Simulated loading delay
        self.root.after(0, self.finish_initialization)

    def finish_initialization(self):
        """Finish the initialization on the main thread."""
        self.play_background_music()
        self.add_background_image()
        self.show_login_screen()
        self.hide_loading_screen()

    def play_click_sound(self):
        try:
            sound = self.spooky_click_sound if self.is_halloween_theme else self.default_click_sound
            sound.set_volume(self.sound_effect_volume)
            sound.play()
        except Exception as e:
            print("Error playing sound:", e)

    def play_background_music(self):
        try:
            if self.is_halloween_theme:
                pygame.mixer.music.load(self.halloween_bgm)
            else:
                pygame.mixer.music.load(self.default_bgm)
                
            pygame.mixer.music.set_volume(self.background_music_volume)
            pygame.mixer.music.play(loops=-1)
        except Exception as e:
            print("Error playing background music:", e)

    def add_background_image(self):
        try:
            image_file = "HalloweenLogin.png" if self.is_halloween_theme else "loginscreen.jpg"
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
            print("Error loading background image:", e)

    def on_resize(self, event):
        self.add_background_image()

    def toggle_theme(self):
        self.show_loading_screen()
        threading.Thread(target=self.apply_theme_change).start()

    def apply_theme_change(self):
        self.is_halloween_theme = not self.is_halloween_theme
        pygame.mixer.music.stop()
        time.sleep(2)
        self.root.after(0, self.finish_theme_change)

    def finish_theme_change(self):
        self.add_background_image()
        self.play_background_music()
        self.show_login_screen()
        self.hide_loading_screen()
        
    def start_glow(self, label):
        # Create a cycle of colors for a glowing effect
        color_cycle = itertools.cycle(["#4deeea", "#74ee15", "#ffe700", "#f000ff", "#001eff"])

        def glow():
            next_color = next(color_cycle)
            label.configure(text_color=next_color)
            self.root.after(500, glow)  # Adjust 500ms as needed for glow speed

        glow()

    def show_login_screen(self):
        self.clear_window(exclude_background=True)
        self.add_background_image()

        login_label = ctk.CTkLabel(
            self.root, 
            text="Library Login", 
            font=self.header_font_style, 
            text_color=self.fg_color, 
            fg_color=None
        )
        login_label.place(relx=0.5, rely=0.2, anchor='center')
        self.start_glow(login_label)

        username_label = ctk.CTkLabel(self.root, text="Username:", font=self.font_style, text_color=self.fg_color, fg_color=None)
        username_label.place(relx=0.5, rely=0.35, anchor='center')
        self.username_entry = ctk.CTkEntry(self.root, font=self.font_style)
        self.username_entry.place(relx=0.5, rely=0.4, anchor='center')

        password_label = ctk.CTkLabel(self.root, text="Password:", font=self.font_style, text_color=self.fg_color, fg_color=None)
        password_label.place(relx=0.5, rely=0.45, anchor='center')
        self.password_entry = ctk.CTkEntry(self.root, show='*', font=self.font_style)
        self.password_entry.place(relx=0.5, rely=0.5, anchor='center')

        login_button = ctk.CTkButton(
            self.root, text="Login", font=self.font_style,
            command=lambda: [self.play_click_sound(), self.login_user()],
            fg_color=self.get_button_bg_color(), text_color=self.get_button_fg_color()
        )
        login_button.place(relx=0.5, rely=0.6, anchor='center')

        signup_button = ctk.CTkButton(
            self.root, text="Sign Up", font=self.font_style,
            command=lambda: [self.play_click_sound(), self.show_signup_screen()],
            fg_color=self.get_button_bg_color(), text_color=self.get_button_fg_color()
        )
        signup_button.place(relx=0.5, rely=0.7, anchor='center')

        theme_button = ctk.CTkButton(
            self.root, text="Toggle Halloween Theme", font=self.font_style,
            command=lambda: [self.play_click_sound(), self.toggle_theme()],
            fg_color=self.get_button_bg_color(), text_color=self.get_button_fg_color()
        )
        theme_button.place(relx=0.5, rely=0.8, anchor='center')

        volume_button = ctk.CTkButton(
            self.root, text="Volume Settings", font=self.font_style,
            command=lambda: [self.play_click_sound(), self.show_volume_settings()],
            fg_color=self.get_button_bg_color(), text_color=self.get_button_fg_color()
        )
        volume_button.place(relx=0.5, rely=0.9, anchor='center')

    def get_button_bg_color(self):
        return self.halloween_button_bg_color if self.is_halloween_theme else self.button_bg_color

    def get_button_fg_color(self):
        return self.halloween_button_fg_color if self.is_halloween_theme else self.button_fg_color

    def show_signup_screen(self):
        self.clear_window(exclude_background=True)
        self.add_background_image()

        signup_label = ctk.CTkLabel(self.root, text="Sign Up", font=self.header_font_style, text_color=self.fg_color, fg_color=None)
        signup_label.place(relx=0.5, rely=0.2, anchor='center')

        username_label = ctk.CTkLabel(self.root, text="Choose a Username:", font=self.font_style, text_color=self.fg_color, fg_color=None)
        username_label.place(relx=0.5, rely=0.35, anchor='center')
        self.username_entry = ctk.CTkEntry(self.root, font=self.font_style)
        self.username_entry.place(relx=0.5, rely=0.4, anchor='center')

        password_label = ctk.CTkLabel(self.root, text="Choose a Password:", font=self.font_style, text_color=self.fg_color, fg_color=None)
        password_label.place(relx=0.5, rely=0.45, anchor='center')
        self.password_entry = ctk.CTkEntry(self.root, show='*', font=self.font_style)
        self.password_entry.place(relx=0.5, rely=0.5, anchor='center')

        signup_button = ctk.CTkButton(self.root, text="Sign Up", font=self.font_style,
                                      command=lambda: [self.play_click_sound(), self.sign_up_user()],
                                      fg_color=self.get_button_bg_color(), text_color=self.get_button_fg_color())
        signup_button.place(relx=0.5, rely=0.6, anchor='center')

        return_button = ctk.CTkButton(self.root, text="Return to Login", font=self.font_style,
                                      command=lambda: [self.play_click_sound(), self.show_login_screen()],
                                      fg_color=self.get_button_bg_color(), text_color=self.get_button_fg_color())
        return_button.place(relx=0.5, rely=0.65, anchor='center')

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if login_user(username, password):
            messagebox.showinfo("Login Successful", "Welcome back!")
            self.launch_library_ui(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")

    def sign_up_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if sign_up_user(username, password):
            messagebox.showinfo("Sign Up Successful", "Account created successfully! You can now log in.")
            self.show_login_screen()
        else:
            messagebox.showerror("Sign Up Failed", "Sign up failed. Please try again with a different username.")

    def launch_library_ui(self, username):
        pygame.mixer.music.stop()
        self.clear_window(exclude_background=True)
        library_ui = LibraryUI(self.root, username)

    def clear_window(self, exclude_background=False):
        for widget in self.root.winfo_children():
            if exclude_background and widget is self.background_label:
                continue
            widget.destroy()

    def show_volume_settings(self):
        self.clear_window(exclude_background=True)
        self.add_background_image()

        volume_label = ctk.CTkLabel(self.root, text="Volume Settings", font=self.header_font_style, text_color=self.fg_color, fg_color=None)
        volume_label.place(relx=0.5, rely=0.2, anchor='center')

        se_volume_label = ctk.CTkLabel(self.root, text="Sound Effects Volume", font=self.font_style, text_color=self.fg_color, fg_color=None)
        se_volume_label.place(relx=0.5, rely=0.35, anchor='center')

        se_volume_slider = ctk.CTkSlider(self.root, from_=0, to=1, number_of_steps=10, command=self.set_sound_effect_volume)
        se_volume_slider.set(self.sound_effect_volume)
        se_volume_slider.place(relx=0.5, rely=0.4, anchor='center')

        bgm_volume_label = ctk.CTkLabel(self.root, text="Background Music Volume", font=self.font_style, text_color=self.fg_color, fg_color=None)
        bgm_volume_label.place(relx=0.5, rely=0.5, anchor='center')

        bgm_volume_slider = ctk.CTkSlider(self.root, from_=0, to=1, number_of_steps=10, command=self.set_background_music_volume)
        bgm_volume_slider.set(self.background_music_volume)
        bgm_volume_slider.place(relx=0.5, rely=0.55, anchor='center')

        return_button = ctk.CTkButton(
            self.root, text="Return to Login", font=self.font_style,
            command=lambda: [self.play_click_sound(), self.show_login_screen()],
            fg_color=self.get_button_bg_color(), text_color=self.get_button_fg_color()
        )
        return_button.place(relx=0.5, rely=0.65, anchor='center')

    def set_sound_effect_volume(self, volume):
        self.sound_effect_volume = volume
        self.default_click_sound.set_volume(volume)
        self.spooky_click_sound.set_volume(volume)

    def set_background_music_volume(self, volume):
        self.background_music_volume = volume
        pygame.mixer.music.set_volume(volume)


if __name__ == "__main__":
    root = ctk.CTk()
    app = LibraryApp(root)
    root.mainloop()