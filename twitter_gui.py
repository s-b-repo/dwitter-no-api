class TwitterGUI:
    def __init__(self, root, scraper):
        self.root = root
        self.scraper = scraper
        self.root.title("Twitter GUI")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.create_tabs()

    def create_tabs(self):
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(fill="both", expand=True)
        self.create_tweet_tab()
        self.create_mentions_tab()
        self.create_dms_tab()

    def create_tweet_tab(self):
        tab = self.tabview.add("Compose Tweet")
        tweet_entry = ctk.CTkTextbox(tab, height=150)
        tweet_entry.pack(padx=20, pady=10)
        ctk.CTkButton(tab, text="Tweet", command=lambda: self.scraper.tweet(tweet_entry.get("1.0", "end"))).pack()

    def create_mentions_tab(self):
        tab = self.tabview.add("Mentions")
        mentions_box = ctk.CTkTextbox(tab, state="disabled")
        mentions_box.pack(fill="both", expand=True, padx=20, pady=10)
        ctk.CTkButton(tab, text="Refresh", command=lambda: self.display_mentions(mentions_box)).pack()

    def display_mentions(self, textbox):
        mentions = self.scraper.get_mentions()
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        textbox.insert("end", "\n".join(mentions))
        textbox.configure(state="disabled")

    def create_dms_tab(self):
        tab = self.tabview.add("Direct Messages")
        dms_box = ctk.CTkTextbox(tab, state="disabled")
        dms_box.pack(fill="both", expand=True, padx=20, pady=10)
        ctk.CTkButton(tab, text="Refresh", command=lambda: self.display_dms(dms_box)).pack()
        ctk.CTkButton(tab, text="Send DM", command=self.open_dm_window).pack()

    def display_dms(self, textbox):
        dms = self.scraper.get_direct_messages()
        messages = [f"{dm['sender']}: {dm['preview']}" for dm in dms]
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        textbox.insert("end", "\n".join(messages))
        textbox.configure(state="disabled")

    def open_dm_window(self):
        dm_win = ctk.CTkToplevel(self.root)
        ctk.CTkLabel(dm_win, text="Recipient").pack()
        recipient_entry = ctk.CTkEntry(dm_win)
        recipient_entry.pack()
        ctk.CTkLabel(dm_win, text="Message").pack()
        message_entry = ctk.CTkTextbox(dm_win, height=100)
        message_entry.pack()
        ctk.CTkButton(dm_win, text="Send", command=lambda: self.scraper.send_direct_message(
            recipient_entry.get(), message_entry.get("1.0", "end"))).pack()
