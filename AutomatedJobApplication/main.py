from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

# === Configuration Section ===
ACCOUNT_EMAIL = "YOUR LOGIN EMAIL"
ACCOUNT_PASSWORD = "YOUR LOGIN PASSWORD"
PHONE = "YOUR PHONE NUMBER"
URL = "YOUR JOB URL"

# === Function to Abort Multi-Step Applications ===
def abort_application():
    """Closes the application modal if it's a complex multistep form."""
    try:
        # Close the modal
        close_button = driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss")
        close_button.click()
        time.sleep(2)

        # Confirm discarding the application
        discard_buttons = driver.find_elements(By.CLASS_NAME, "artdeco-modal__confirm-dialog-btn")
        if discard_buttons:
            discard_buttons[-1].click()
    except NoSuchElementException:
        print("Couldn't find discard modal buttons.")

# === Browser Setup ===
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)  # Keeps browser open after script ends

driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)

# === Cookie/Popup Dismissal ===
time.sleep(2)
try:
    # Attempt to reject cookies or close the popup if it exists
    reject_button = driver.find_element(By.CLASS_NAME, "artdeco-global-alert-action__confirm-button")
    reject_button.click()
except NoSuchElementException:
    print("No cookie reject button found.")

# === Sign In to LinkedIn ===
time.sleep(2)
sign_in_button = driver.find_element(By.LINK_TEXT, "Sign in")
sign_in_button.click()

# Wait for the login page to load
time.sleep(5)

# Fill in email and password
email_field = driver.find_element(By.ID, "username")
email_field.send_keys(ACCOUNT_EMAIL)

password_field = driver.find_element(By.ID, "password")
password_field.send_keys(ACCOUNT_PASSWORD)
password_field.send_keys(Keys.ENTER)

# Wait for manual CAPTCHA solving (if prompted)
input("⚠️ Press Enter after solving CAPTCHA and login is complete...")

# === Get All Job Listings on Page ===
time.sleep(5)
all_listings = driver.find_elements(By.CSS_SELECTOR, ".job-card-container--clickable")

# === Loop Through Each Job and Try to Apply ===
for listing in all_listings:
    print("🔍 Opening job listing...")
    listing.click()
    time.sleep(2)

    try:
        # Look for the "Easy Apply" button
        apply_button = driver.find_element(By.CSS_SELECTOR, ".jobs-s-apply button")
        apply_button.click()
        time.sleep(5)

        # Fill in the phone number if input is empty
        try:
            phone_input = driver.find_element(By.CSS_SELECTOR, "input[id*=phoneNumber]")
            if phone_input.get_attribute("value") == "":
                phone_input.send_keys(PHONE)
        except NoSuchElementException:
            print("⚠️ No phone input field found.")

        # Find the submit button (could be "Submit" or "Next")
        submit_button = driver.find_element(By.CSS_SELECTOR, "footer button")

        # Detect if it's a multistep form
        control_name = submit_button.get_attribute("data-control-name")
        if control_name == "continue_unify":
            abort_application()
            print("⚠️ Complex application detected. Skipped.")
            continue
        else:
            # Submit application
            print("✅ Submitting job application...")
            submit_button.click()

        # Close confirmation modal after applying
        time.sleep(2)
        try:
            close_button = driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss")
            close_button.click()
        except NoSuchElementException:
            print("ℹ️ No modal to close after applying.")

    except NoSuchElementException:
        # If no Easy Apply button, skip this listing
        print("❌ No Easy Apply button. Skipping.")
        continue

# === Finished All Applications ===
print("🎉 Job application automation complete.")
time.sleep(5)
driver.quit()
