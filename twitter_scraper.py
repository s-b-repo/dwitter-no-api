from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

class TwitterScraper:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = self.initialize_driver()

    def initialize_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def login(self):
        """Log in to Twitter."""
        self.driver.get("https://twitter.com/login")
        time.sleep(3)
        self.driver.find_element(By.NAME, "session[username_or_email]").send_keys(self.username)
        self.driver.find_element(By.NAME, "session[password]").send_keys(self.password + Keys.RETURN)
        time.sleep(5)

    def tweet(self, tweet_text):
        """Post a tweet."""
        self.driver.get("https://twitter.com/compose/tweet")
        time.sleep(3)
        tweet_box = self.driver.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetTextarea_0"]')
        tweet_box.send_keys(tweet_text)
        self.driver.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetButtonInline"]').click()
        time.sleep(3)

    def get_mentions(self):
        """Fetch mentions."""
        self.driver.get("https://twitter.com/notifications/mentions")
        time.sleep(5)
        mentions = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
        return [mention.text for mention in mentions]

    def get_direct_messages(self):
        """Fetch DMs."""
        self.driver.get("https://twitter.com/messages")
        time.sleep(5)
        conversations = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="conversation"]')
        return [
            {
                "sender": convo.find_element(By.CSS_SELECTOR, '[data-testid="usernames"]').text,
                "preview": convo.find_element(By.CSS_SELECTOR, '[data-testid="conversationPreview"]').text,
            }
            for convo in conversations
        ]

    def send_direct_message(self, recipient, message):
        """Send a direct message."""
        self.driver.get("https://twitter.com/messages/compose")
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, '[data-testid="searchPeople"]').send_keys(recipient + Keys.RETURN)
        time.sleep(3)
        message_box = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="dmComposerTextInput"]')
        message_box.send_keys(message + Keys.RETURN)
        time.sleep(3)

    def close(self):
        """Close the Selenium driver."""
        self.driver.quit()
