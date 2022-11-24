from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import os

main_page = "https://www.otomoto.pl/osobowe/renault/megane"

def get_id_from_link(link):
    match = re.search("oferta\/(.+)\.html", link)
    if match is None: return None
    return match.groups()[0]

# Open page
driver = webdriver.Chrome()
driver.set_window_size(1400,900)
driver.get(main_page)

# Accept c00kies
driver.find_element(By.ID, "onetrust-accept-btn-handler").click()

# Find all articles
listings_elements = driver.find_elements(By.CSS_SELECTOR, "article[data-testid='listing-ad']")
listing_links = [listing.find_element(By.CSS_SELECTOR, "h2 > a").get_attribute("href") for listing in listings_elements]

for link in listing_links:
    id = get_id_from_link(link)
    os.mkdir(f'scrapped_data/pics/{id}')
    driver.get(link)

sleep(3)

# Quit
driver.quit()
