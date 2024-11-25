import customtkinter as ctk
from twitter_gui import TwitterGUI
from twitter_scraper import TwitterScraper


class TwitterLoginGUI:
    def __init__(self, root):
        self.root = root
        self.scraper = None
        self.root.title("Twitter Login")
        self.root.geometry("400x500")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.create_login_screen()

    def create_login_screen(self):
        login_frame = ctk.CTkFrame(self.root)
        login_frame.pack(fill="both", expand=True, padx=20, pady=20)
        ctk.CTkLabel(login_frame, text="Twitter Login", font=("Arial", 24, "bold")).pack(pady=20)
        self.username_entry = self.create_input_field(login_frame, "Username")
        self.password_entry = self.create_input_field(login_frame, "Password")
        ctk.CTkButton(login_frame, text="Login", command=self.handle_login).pack(pady=20)
        self.status_label = ctk.CTkLabel(login_frame, text="", text_color="red")
        self.status_label.pack(pady=10)

    def create_input_field(self, parent, placeholder):
        ctk.CTkLabel(parent, text=placeholder).pack(pady=(10, 0))
        entry = ctk.CTkEntry(parent, show="*" if placeholder == "Password" else None)
        entry.pack(pady=5)
        return entry

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not all([username, password]):
            self.status_label.configure(text="All fields are required!", text_color="red")
            return
        try:
            self.scraper = TwitterScraper(username, password)
            self.scraper.login()
            self.status_label.configure(text="Login successful!", text_color="green")
            self.load_main_gui()
        except Exception as e:
            self.status_label.configure(text=f"Login failed: {str(e)}", text_color="red")

    def load_main_gui(self):
        self.root.destroy()
        main_root = ctk.CTk()
        TwitterGUI(main_root, self.scraper)
        main_root.mainloop()


if __name__ == "__main__":
    root = ctk.CTk()
    TwitterLoginGUI(root)
    root.mainloop()
