from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Headers to avoid being blocked as a bot
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
    "Accept-Language": "en-US,en;q=0.9"
}

# Step 1: Get HTML content
response = requests.get("https://appbrewery.github.io/Zillow-Clone/", headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Step 2: Extract listing data
all_links = [link["href"] for link in soup.select(".StyledPropertyCardDataWrapper a")]
all_addresses = [addr.get_text().replace(" | ", " ").strip() for addr in
                 soup.select(".StyledPropertyCardDataWrapper address")]
all_prices = [
    price.get_text().replace("/mo", "").split("+")[0]
    for price in soup.select(".PropertyCardWrapper span")
    if "$" in price.text
]

# Step 3: Setup Chrome for automation
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)  # Optional; remove if not needed
driver = webdriver.Chrome(options=chrome_options)

# Step 4: Fill Google Form for each listing
for n in range(len(all_links)):
    driver.get("YOUR_GOOGLE_FORM_LINK_HERE")
    time.sleep(2)  # Wait for form to load

    # Fill form fields using XPath (replace with CSS if available)
    driver.find_element(By.XPATH, '//input[@type="text" and contains(@aria-label, "address")]').send_keys(
        all_addresses[n])
    driver.find_element(By.XPATH, '//input[@type="text" and contains(@aria-label, "price")]').send_keys(all_prices[n])
    driver.find_element(By.XPATH, '//input[@type="text" and contains(@aria-label, "link")]').send_keys(all_links[n])

    driver.find_element(By.XPATH, '//div[@role="button" and contains(text(), "Submit")]').click()
