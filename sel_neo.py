from tkinter import E
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys  # acces to exc/enter itd keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import json

def neo(brand = 'SAMSUNG'):
    brand = brand.upper()
    PATH = r'C:\Program Files (x86)/chromedriver.exe'

    # options for hide "Failed to read descriptor from node connection"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(PATH, options=options)
    driver.implicitly_wait(5)
    driver.get('https://www.neo24.pl/')
    driver.maximize_window()

    # click cookie accept
    driver.find_element(By.XPATH, "//button[text()='Zaakceptuj wszystkie']").click()

    # choose type of product
    driver.find_element(By.XPATH, "//a[text()='Smartfony i smartwatche']").click()
    time.sleep(1.5)
    driver.find_element(By.XPATH, "//a[text()='Smartfony']").click()


    # choose brand
    brand = brand.upper()
    phone_model = driver.find_element(By.XPATH, f"//a[text()='{brand}']")
    driver.execute_script("arguments[0].click();", phone_model)


    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)") 
    time.sleep(2) # waiting for load all offers

    list_of_phones = []
    while True:
        names = driver.find_elements(By.XPATH, '//h2/a')
        prices = driver.find_elements(By.XPATH, "//span[@class='uiPriceCss-integer-2sc']")
        for name, price in zip(names, prices):
            print(f'name- {name.text}, price-{price.text}')
            list_of_phones.append({'name':name.text, 'price':price.text})

        try:
            next_page = driver.find_element(By.XPATH, "//button[@aria-label='move to the next page']/span")
            driver.execute_script("arguments[0].click();", next_page)
            driver.get(driver.current_url)

        except NoSuchElementException as e:
            print(30*'=')
            break

    data_dict = {}
    data_dict[brand] = list_of_phones
    json_string = json.dumps(data_dict)
    with open(f'json_files/neo_{brand}.json', 'w+') as f:
        f.write(json_string)
