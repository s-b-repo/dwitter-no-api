import time
import os
import pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class TwitterScraper:
    COOKIE_FILE = "twitter_cookies.pkl"

    def __init__(self):
        self.driver = self.initialize_driver()

    def initialize_driver(self):
        """Initialize the Selenium WebDriver."""
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def login(self, username=None, password=None):
        """
        Log in to Twitter. If cookies are present, reuse them to bypass login.
        If cookies are not valid, prompt the user to log in manually.
        """
        self.driver.get("https://twitter.com/login")
        time.sleep(3)

        # Load cookies if available
        if os.path.exists(self.COOKIE_FILE):
            self.load_cookies()
            self.driver.refresh()
            time.sleep(3)

        # If already logged in, return
        if "home" in self.driver.current_url:
            print("Login successful using cookies!")
            return

        # Manual login if cookies are not valid
        if username and password:
            print("Attempting manual login...")
            self.driver.find_element(By.NAME, "session[username_or_email]").send_keys(username)
            self.driver.find_element(By.NAME, "session[password]").send_keys(password + Keys.RETURN)
            time.sleep(5)

        # If CAPTCHA or manual intervention is needed, inform the user
        if "login" in self.driver.current_url:
            print("Manual login required. Please complete the login in the browser.")
            self.wait_for_manual_login()

        # Save cookies after successful login
        if "home" in self.driver.current_url:
            self.save_cookies()
            print("Login successful and cookies saved!")
        else:
            raise RuntimeError("Login failed! Please check your credentials.")

    def wait_for_manual_login(self):
        """Wait until the user has logged in manually."""
        while "home" not in self.driver.current_url:
            print("Waiting for manual login...")
            time.sleep(5)

    def save_cookies(self):
        """Save cookies to a file."""
        with open(self.COOKIE_FILE, "wb") as file:
            pickle.dump(self.driver.get_cookies(), file)
        print("Cookies saved to file.")

    def load_cookies(self):
        """Load cookies from a file."""
        with open(self.COOKIE_FILE, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        print("Cookies loaded from file.")

    def tweet(self, tweet_text):
        """Post a tweet."""
        self.driver.get("https://twitter.com/compose/tweet")
        time.sleep(3)
        tweet_box = self.driver.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetTextarea_0"]')
        tweet_box.send_keys(tweet_text)
        self.driver.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetButtonInline"]').click()
        time.sleep(3)

    def close(self):
        """Close the Selenium driver."""
        self.driver.quit()
