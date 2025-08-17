import csv
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

url = 'https://steamdb.info/charts/'
options = uc.ChromeOptions()
driver = uc.Chrome(options=options, use_subprocess=True)

print("🚀 Launching patched browser and navigating to URL...")

try:
    driver.get(url)

    print("⏳ Waiting for Cloudflare check and for the game chart to load...")
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "tr.app"))
    )

    print("✅ Cloudflare passed! Game chart has loaded.")
    time.sleep(2)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    scraped_data = []
    game_rows = soup.find_all('tr', class_='app')

    if not game_rows:
        print("❌ Could not find any game rows. Check the website and selectors.")
    else:
        for row in game_rows:
            cols = row.find_all('td')
            if len(cols) > 5:

                game_name = cols[2].find('a').get_text(strip=True) if cols[2].find('a') else 'N/A'
                current_players = cols[3].get_text(strip=True)
                peak_today = cols[4].get_text(strip=True)
                all_time_peak = cols[5].get_text(strip=True)

                scraped_data.append({
                    'Game Name': game_name,
                    'Current Players': current_players,
                    '24h Peak': peak_today,
                    'All-Time Peak': all_time_peak
                })

    if scraped_data:
        csv_file = 'steamdb_charts_uc.csv'
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['Game Name', 'Current Players', '24h Peak', 'All-Time Peak']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(scraped_data)
        print(f"🎉 Success! Data has been scraped and saved to {csv_file}")
    else:
        print("No data was scraped.")

except Exception as e:
    print(f"❌ An error occurred: {e}")

finally:
    print("Closing the browser.")
    driver.quit()