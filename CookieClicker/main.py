from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep, time

# Set up Chrome browser options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)  # Keeps the browser open after a script finishes

# Start the browser and open the Cookie Clicker game
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://ozh.github.io/cookieclicker/")

# Give time for the page to load
sleep(3)

# Try selecting the English language if the prompt shows up
print("Looking for language selection...")
try:
    language_button = driver.find_element(By.ID, "langSelect-EN")
    print("Found language button, clicking...")
    language_button.click()
    sleep(3)  # Wait after clicking language
except NoSuchElementException:
    print("Language selection not found.")  # If already in English or element isn't found

# Wait for the game to fully initialize
sleep(2)

# Locate the main cookie element we will be clicking
cookie = driver.find_element(by=By.ID, value="bigCookie")

# Create a list of product IDs we might buy (18 total items in the game shop)
item_ids = [f"product{i}" for i in range(18)]

# Define how often we check for upgrades (in seconds)
wait_time = 5
timeout = time() + wait_time

# Define the total run time of the script (5 minutes from start)
five_min = time() + 60 * 5

# Main game loop
while True:
    # Click the big cookie continuously
    cookie.click()

    # Every 'wait_time' seconds, try to buy the most expensive available product
    if time() > timeout:
        try:
            # Get the current number of cookies from the top display
            cookies_element = driver.find_element(by=By.ID, value="cookies")
            cookie_text = cookies_element.text
            cookie_count = int(cookie_text.split()[0].replace(",", ""))  # Clean up the number

            # Find all product elements (buildings/upgrades)
            products = driver.find_elements(by=By.CSS_SELECTOR, value="div[id^='product']")

            best_item = None
            # Iterate through products in reverse order (most expensive first)
            for product in reversed(products):
                # Only consider products that are currently enabled (i.e., affordable)
                if "enabled" in product.get_attribute("class"):
                    best_item = product
                    break

            # If an item was found to buy, click it
            if best_item:
                best_item.click()
                print(f"Bought item: {best_item.get_attribute('id')}")
        except (NoSuchElementException, ValueError):
            # Handle cases where the element structure changed or text parsing failed
            print("Couldn't find cookie count or items")

        # Reset timeout to run the check again after `wait_time` seconds
        timeout = time() + wait_time

    # If 5 minutes have passed, print the final cookie count and exit
    if time() > five_min:
        try:
            cookies_element = driver.find_element(by=By.ID, value="cookies")
            print(f"Final result: {cookies_element.text}")
        except NoSuchElementException:
            print("Couldn't get final cookie count")
        break
