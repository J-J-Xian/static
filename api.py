import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Configure Chrome options (headless mode helps in non-interactive environments)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

# Initialize the Chrome driver with the desired options
driver = webdriver.Chrome(options=chrome_options)

# Open the PTT NBA page
driver.get("https://www.ptt.cc/bbs/nba/index.html")
time.sleep(2)  # Give the page a moment to load

# If the page shows an over18 confirmation, click the "yes" button to proceed.
if "over18" in driver.current_url:
    try:
        # Find and click the button with class "btn-big"
        over18_button = driver.find_element(By.CSS_SELECTOR, "button.btn-big")
        over18_button.click()
        time.sleep(2)  # Wait for the confirmation to be processed
    except Exception as e:
        print("Error handling over18 prompt:", e)

# Once at the main page, locate all article elements with class "r-ent"
articles = driver.find_elements(By.CSS_SELECTOR, "div.r-ent")
data_list = []

# Loop through each article element and extract data
for article in articles:
    data = {}
    
    # Get the title; check if the article still exists (some may have been deleted)
    try:
        title_element = article.find_element(By.CSS_SELECTOR, "div.title")
        try:
            link = title_element.find_element(By.TAG_NAME, "a")
            data["title"] = link.text.strip()
        except Exception:
            data["title"] = "No Content!"
    except Exception:
        data["title"] = "No Content!"
    
    # Get the popularity, if available (otherwise use "N/A")
    try:
        pop_element = article.find_element(By.CSS_SELECTOR, "div.nrec")
        pop_text = pop_element.text.strip()
        data["popularity"] = pop_text if pop_text != "" else "N/A"
    except Exception:
        data["popularity"] = "N/A"
    
    # Get the date for the article
    try:
        date_element = article.find_element(By.CSS_SELECTOR, "div.date")
        data["date"] = date_element.text.strip()
    except Exception:
        data["date"] = "N/A"
    
    data_list.append(data)

driver.quit()

# Write the results to a CSV file named "api.csv"
with open("api.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["title", "popularity", "date"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in data_list:
        writer.writerow(row)

print("CSV file 'api.csv' created successfully.")
