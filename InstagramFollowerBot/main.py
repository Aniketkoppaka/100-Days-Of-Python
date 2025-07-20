# Import necessary modules from Selenium and Python standard library
from selenium import webdriver  # Main module to control the Chrome browser
from selenium.webdriver.common.keys import Keys  # To simulate keyboard input (e.g., Enter)
from selenium.webdriver.common.by import By  # Allows you to select elements using different strategies (e.g., by name, xpath, css)
from selenium.common.exceptions import ElementClickInterceptedException  # Catches errors when an element can’t be clicked
import time  # Used for delays to let pages load

# Constants (fill these with your actual values before running)
SIMILAR_ACCOUNT = "INSTAGRAM_ACCOUNT_YOU_WANT_TO_BECOME"  # The target account whose followers you want to follow
USERNAME = "YOUR_INSTAGRAM_EMAIL"  # Your Instagram login email or username
PASSWORD = "YOUR_INSTAGRAM_PASSWORD"  # Your Instagram password

# Define a class that handles all Instagram automation logic
class InstaFollower:

    # Constructor method — called automatically when an object is created
    def __init__(self):
        # Create Chrome options to configure the browser
        chrome_options = webdriver.ChromeOptions()

        # This keeps the browser window open after the script finishes
        chrome_options.add_experimental_option("detach", True)

        # Create the Chrome driver with the given options
        self.driver = webdriver.Chrome(options=chrome_options)

    # Method to log into Instagram using provided credentials
    def login(self):
        # Navigate to Instagram's login page
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(5)  # Wait for the page and elements to load

        # Dismiss the cookie consent pop-up if it appears
        decline_xpath = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]"
        cookie_warning = self.driver.find_elements(By.XPATH, decline_xpath)
        if cookie_warning:
            cookie_warning[0].click()  # Click "Decline All" if the cookie banner is found

        # Locate the username and password input fields by their 'name' attribute
        username_input = self.driver.find_element(by=By.NAME, value="username")
        password_input = self.driver.find_element(by=By.NAME, value="password")

        # Enter your credentials into the input fields
        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)

        time.sleep(1)  # Small delay before submitting

        # Press ENTER to submit the login form
        password_input.send_keys(Keys.ENTER)

        time.sleep(5)  # Wait for the page to load after login

        # Handle "Save Your Login Info?" prompt if it appears
        try:
            not_now_btn = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Not now')]")
            not_now_btn.click()
        except:
            pass  # If the popup doesn't appear, skip it

        time.sleep(4)  # Wait before handling the next prompt

        # Handle "Turn on Notifications" prompt if it appears
        try:
            not_now_btn_2 = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
            not_now_btn_2.click()
        except:
            pass

    # Method to go to the target account's followers and scroll through the list
    def find_followers(self):
        time.sleep(5)  # Let the page settle before navigating again

        # Navigate to the followers page of the account you want to copy
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}/followers")

        time.sleep(5)  # Wait for the followers modal to appear

        # Locate the scrollable modal that contains the followers list
        modal_xpath = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]"
        modal = self.driver.find_element(by=By.XPATH, value=modal_xpath)

        # Scroll the modal 10 times to load more followers
        for _ in range(10):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
            time.sleep(2)  # Delay between scrolls to allow followers to load

    # Method to click the "Follow" buttons next to each user
    def follow(self):
        # Find all the follow buttons using a CSS selector that matches Instagram's current structure
        follow_buttons = self.driver.find_elements(By.CSS_SELECTOR, "._aano button")

        # Loop through each button and click it
        for button in follow_buttons:
            try:
                button.click()  # Attempt to click the follow button
                time.sleep(1)  # Small delay between clicks to avoid detection
            except ElementClickInterceptedException:
                # If something blocks the click (e.g., a confirmation dialog), close it
                try:
                    cancel_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Cancel')]")
                    cancel_button.click()
                except:
                    pass  # If no cancel button is found, skip to the next

# Create an object of the class to run the bot
bot = InstaFollower()
bot.login()           # Step 1: Log in to Instagram
bot.find_followers()  # Step 2: Go to target account and scroll through followers
bot.follow()          # Step 3: Click "Follow" on all loaded users
