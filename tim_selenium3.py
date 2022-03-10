from tkinter import E
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # acces to exc/enter itd keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

PATH = r'C:\Program Files (x86)/chromedriver.exe'

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(PATH, options=options)
driver.implicitly_wait(3)
#driver.get('https://www.ebay.pl/sch/Telefony-i-Akcesoria/15032/i.html')
driver.get('https://www.ebay.com/b/Cell-Phones-Smartphones/9355/bn_320094')

cookie = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.ID, "gdpr-banner-accept")))
cookie.click()

search = driver.find_element(By.XPATH, '//input[@placeholder="Search for anything"]')
search.click()
search.send_keys('samsung')
search.send_keys(Keys.RETURN) # click enter



number_of_pages = 15
list_of_phones = []
for num in range(number_of_pages):
    offers = driver.find_elements(By.XPATH, '//*[@id = "srp-river-results"]/ul/li')
    for offer in offers:
        print(30*'=')
        if offer.find_element(By.CLASS_NAME, 's-item__price') and offer.find_element(By.CLASS_NAME, 's-item__title')
            price = offer.find_element(By.CLASS_NAME, 's-item__price').text
            name = offer.find_element(By.CLASS_NAME, 's-item__title').text
            list_of_phones.append({'name':name, 'price':price})
        print(f'name - {name}, price = {price}')
        print(30*'=')

    next_page = driver.find_element(By.XPATH, '//a[@class="pagination__next icon-link"]')
    next_page.click()
    time.sleep(1)
    driver.get(driver.current_url)

