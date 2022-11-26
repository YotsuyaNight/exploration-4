from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import os
import json
import urllib
import nltk
import re

nltk.download('punkt')

main_page = "https://www.otomoto.pl/osobowe/renault/megane"

# Helpers
def __tokenize_document__(contents):
    lowercase_contents = contents.lower()
    stripped_contents = re.sub('\n|\t', ' ', lowercase_contents)
    tokenized_content = nltk.word_tokenize(stripped_contents)
    return tokenized_content

def __get_id_from_link__(link):
    match = re.search("oferta\/(.+)\.html", link)
    if match is None: return None
    return match.groups()[0]

def __remove_resize_from_link__(link):
    if link is None: return None
    return re.sub(";s=\d+x\d+", "", link)

# Open page
driver = webdriver.Chrome()
driver.set_window_size(1400,900)
driver.get(main_page)

# Accept c00kies
driver.find_element(By.ID, "onetrust-accept-btn-handler").click()

# Find all listings
listings_elements = driver.find_elements(By.CSS_SELECTOR, "article[data-testid='listing-ad']")
listing_links = [listing.find_element(By.CSS_SELECTOR, "h2 > a").get_attribute("href") for listing in listings_elements]

# Traverse listings
for link in listing_links:
    id = __get_id_from_link__(link)
    pics_dir = f'scrapped_data/pics/{id}'
    docs_dir = 'scrapped_data/documents'
    car_data_dir = 'scrapped_data/data'
    os.makedirs(pics_dir, exist_ok=True)

    # Go to page
    driver.get(link)

    # Download images
    # imgs = [__remove_resize_from_link__(img.get_attribute("src")) for img in driver.find_elements(By.CSS_SELECTOR, ".slick-slide img")]
    # for index, img_link in enumerate(imgs):
    #     if img_link is None: continue
    #     filepath = f'{pics_dir}/{index}.webp'
    #     print(f'Downloading {img_link} to {filepath}')
    #     urllib.request.urlretrieve(img_link, filepath)

    # Parse main car params
    main_params = {}
    for param_el in driver.find_elements(By.CLASS_NAME, "offer-params__item"):
        key = param_el.find_element(By.CLASS_NAME, "offer-params__label").get_attribute("innerText")
        val = param_el.find_element(By.CLASS_NAME, "offer-params__value").get_attribute("innerText")
        main_params[key] = val

    # Parse additional features into document tokens
    features = [el.get_attribute("innerText") for el in driver.find_elements(By.CLASS_NAME, "parameter-feature-item")]
    description = __tokenize_document__(driver.find_element(By.CLASS_NAME, "offer-description__description").get_attribute("innerText"))
    
    # Save
    document_filepath = f'{docs_dir}/{id}.txt'
    data_filepath = f'{car_data_dir}/{id}.txt'
    with open(document_filepath, "w+", encoding="utf-8") as file:
        file.write("\n".join(features))
        file.write("\n")
        file.write("\n".join(description))
    with open(data_filepath, "w+", encoding="utf-8") as file:
        file.write(json.dumps(main_params, indent=4, ensure_ascii=False))

# Quit
driver.quit()
