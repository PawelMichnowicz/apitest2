from tkinter import E
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # acces to exc/enter itd keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

PATH = r'C:\Program Files (x86)/chromedriver.exe'

# options for hide "Failed to read descriptor from node connection"
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(PATH, options=options)
driver.implicitly_wait(5)
driver.get('https://www.x-kom.pl/g-4/c/1590-smartfony-i-telefony.html')

# click cookie accept
driver.find_element(By.XPATH, "//button[text()='W porządku']").click()

search = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
    (By.XPATH, '//input[@placeholder="Czego szukasz?"]')))
search.click()
search.send_keys("samsung")
search.send_keys(Keys.RETURN)

offers = driver.find_elements(
    By.XPATH, '//div[@class="sc-162ysh3-1 dAqvUz sc-EHOje hDVxfb"]')
number_of_pages = 5
list_of_phones = []
for num in range(number_of_pages):
    for offer in offers:
        try:
            print(44*'-')
            # if offer.find_element_by_tag_name('span'):
            for span in offer.find_elements(By.TAG_NAME, 'span'):
                if span.text:
                    print(span.text)
                    if span.text.endswith("zł"):
                        price = span.text
                    if span.text.startswith("Samsung"):
                        name = span.text
            print(f'name - {name}, price {price}')
            list_of_phones.append({'Name': name, 'Price': price})

        except Exception as e:
            print(e)

    driver.find_element(By.XPATH, "//span[text()='Następna']").click()
    time.sleep(3)


# if span.text and span.text.endswith("zł"):
#                 price = span.text
#             elif span.text and span.text.startswith("Samsung"):
#                     name = span.text


# for offer in offers:
#     print(44*'-')
#     for span in offer.find_elements(By.TAG_NAME, 'span'):
#         if span.text and span.text.endswith("zł"):
#             price = span.text
#         if span.text and span.text.startswith("Samsung"):
#                 name = span.text
#     print (f'name - {name}, price {price}')


driver.quit()  # close() for tab? / quit() close whole website
