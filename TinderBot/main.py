from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from time import sleep

# === Credentials ===
FB_EMAIL = "YOUR FACEBOOK LOGIN EMAIL"
FB_PASSWORD = "YOUR FACEBOOK PASSWORD"

# === Set up Chrome browser ===
driver = webdriver.Chrome()

# === Open Tinder ===
driver.get("https://tinder.com/")
sleep(2)

# === Click "Log in" button on Tinder homepage ===
login_button = driver.find_element(By.XPATH, '//*[@id="o-1778884828"]/div/div[1]/div/div/div/main/div/div[2]/div/div[3]/div/div/button/div[2]/div[2]')
login_button.click()
sleep(2)

# === Choose "Log in with Facebook" ===
fb_login_button = driver.find_element(By.XPATH, '//*[@id="o787701392"]/div/div/div/div[2]/div/div/div[2]/div[2]/span/div[2]/button/div[2]/div[2]/div[2]/div/div')
fb_login_button.click()
sleep(2)

# === Handle Facebook login in new window ===
base_window = driver.window_handles[0]
fb_login_window = driver.window_handles[1]
driver.switch_to.window(fb_login_window)

# === Enter Facebook credentials ===
email_input = driver.find_element(By.ID, "email")
email_input.send_keys(FB_EMAIL)
password_input = driver.find_element(By.ID, "pass")
password_input.send_keys(FB_PASSWORD)
password_input.send_keys(Keys.ENTER)

# === Switch back to Tinder main window ===
driver.switch_to.window(base_window)
sleep(5)

# === Handle location permission popup ===
try:
    allow_location_button = driver.find_element(By.XPATH, '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
    allow_location_button.click()
except NoSuchElementException:
    print("Location permission popup not found")

# === Handle notifications popup ===
try:
    notifications_button = driver.find_element(By.XPATH, '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]')
    notifications_button.click()
except NoSuchElementException:
    print("Notification popup not found")

# === Accept cookies ===
try:
    cookies_button = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/div/div[1]/button')
    cookies_button.click()
except NoSuchElementException:
    print("Cookies button not found")

# === Auto-like loop ===
for n in range(100):  # Adjust number of swipes as needed
    sleep(1)
    try:
        print(f"Liking profile {n + 1}")
        like_button = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')
        like_button.click()
    except ElementClickInterceptedException:
        # Handle "It's a Match!" popup
        try:
            match_popup = driver.find_element(By.CSS_SELECTOR, ".itsAMatch a")
            match_popup.click()
        except NoSuchElementException:
            print("Match popup not found, waiting...")
            sleep(2)
    except NoSuchElementException:
        print("Like button not found, possibly out of swipes.")
        break

# === Close browser after finishing ===
driver.quit()
