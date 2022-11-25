from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import os
import urllib

main_page = "https://www.otomoto.pl/osobowe/renault/megane"

def get_id_from_link(link):
    match = re.search("oferta\/(.+)\.html", link)
    if match is None: return None
    return match.groups()[0]

def remove_resize_from_link(link):
    if link is None: return None
    return re.sub(";s=\d+x\d+", "", link)

# Open page
driver = webdriver.Chrome()
driver.set_window_size(1400,900)

# Find all listings
listing_links = ["https://www.otomoto.pl/oferta/renault-megane-stan-bdb-100-bezwypadkowy-ID6EVnkK.html"]

# Traverse listings
for link in listing_links:
    id = get_id_from_link(link)
    pics_dir = f'scrapped_data/pics/{id}'
    docs_dir = 'documents'
    os.makedirs(pics_dir, exist_ok=True)

    # Go to page
    driver.get(link)
    driver.find_element(By.ID, "onetrust-accept-btn-handler").click()

    # Download images
    # imgs = [remove_resize_from_link(img.get_attribute("src")) for img in driver.find_elements(By.CSS_SELECTOR, ".slick-slide img")]
    # for index, img_link in enumerate(imgs):
    #     if img_link is None: continue
    #     filepath = f'{dir}/{index}.webp'
    #     print(f'Downloading {img_link} to {filepath}')
    #     urllib.request.urlretrieve(img_link, filepath)

    main_params = {}
    for param_el in driver.find_elements(By.CLASS_NAME, "offer-params__item"):
        key = param_el.find_element(By.CLASS_NAME, "offer-params__label").get_attribute("innerText")
        val = param_el.find_element(By.CLASS_NAME, "offer-params__value").get_attribute("innerText")
        print((key, val))

sleep(3)

# Quit
driver.quit()
