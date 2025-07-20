from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Constants – Replace these with your actual values
PROMISED_DOWN = "YOUR PROMISED DOWNLOAD SPEED"
PROMISED_UP = "YOUR PROMISED UPLOAD SPEED"
CHROME_DRIVER_PATH = "YOUR CHROME DRIVER PATH"
TWITTER_EMAIL = "YOUR TWITTER EMAIL"
TWITTER_PASSWORD = "YOUR TWITTER PASSWORD"

class InternetSpeedTwitterBot:
    def __init__(self, driver_path):
        # Initialize Chrome WebDriver
        self.driver_path = driver_path
        self.driver = webdriver.Chrome()
        self.up = 0  # Store upload speed
        self.down = 0  # Store download speed

    def get_internet_speed(self):
        """
        This method navigates to Speedtest.net, performs a speed test, and stores
        the upload and download speeds as instance variables.
        """
        self.driver.get("https://www.speedtest.net/")
        time.sleep(3)

        # Accept cookies on Speedtest.net (may change based on your region)
        accept_button = self.driver.find_element(By.ID, value="_evidon-banner-acceptbutton")
        accept_button.click()
        time.sleep(3)

        # Click the 'GO' button to start the test
        go_button = self.driver.find_element(By.CSS_SELECTOR, value=".start-button a")
        go_button.click()

        # Wait 60 seconds for the test to complete (could adjust if needed)
        time.sleep(60)

        # Get upload and download results from the result page
        self.up = self.driver.find_element(
            By.XPATH,
            '//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[2]/div/div[4]/div/div[3]/div/div/'
            'div[2]/div[1]/div[1]/div/div[2]/span'
        ).text

        self.down = self.driver.find_element(
            By.XPATH,
            '//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[2]/div/div[4]/div/div[3]/div/div/'
            'div[2]/div[1]/div[2]/div/div[2]/span'
        ).text

    def tweet_at_provider(self):
        """
        This method logs into Twitter, composes a tweet complaining about internet speed,
        and posts it.
        """
        self.driver.get("https://x.com/i/flow/login")
        time.sleep(3)

        # Input email address
        email_input = self.driver.find_element(By.XPATH,
            '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/'
            'label/div/div[2]/div/input')
        email_input.send_keys(TWITTER_EMAIL)
        email_input.send_keys(Keys.ENTER)
        time.sleep(5)

        # Input password (make sure this is the correct path; Twitter changes frequently)
        password_input = self.driver.find_element(By.XPATH,
            '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/'
            'div/div[3]/div/label/div/div[2]/div[1]/input')
        password_input.send_keys(TWITTER_PASSWORD)
        password_input.send_keys(Keys.ENTER)
        time.sleep(5)

        # Find the tweet box (Note: Twitter’s layout may require updating this path frequently)
        tweet_compose = self.driver.find_element(By.XPATH,
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/'
            'div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div')

        # Compose the tweet
        tweet = (
            f"Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up "
            f"when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?"
        )
        tweet_compose.send_keys(tweet)
        time.sleep(3)

        # Click on the Tweet button to post the tweet
        tweet_button = self.driver.find_element(By.XPATH,
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/'
            'div/div/div/div[2]/div[4]/div/div/div[2]/div[3]')
        tweet_button.click()
        time.sleep(2)

        # Close the browser
        self.driver.quit()


# Create an instance of the bot and run it
bot = InternetSpeedTwitterBot(CHROME_DRIVER_PATH)
bot.get_internet_speed()
bot.tweet_at_provider()
