from tkinter import E
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # acces to exc/enter itd keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import time
import json
import re

def xkom(brand = 'Samsung', type_product='Smartphone'):
    brand = brand.upper()
    PATH = r'C:\Program Files (x86)/chromedriver.exe'

    # options for hide "Failed to read descriptor from node connection"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(PATH, options=options)
    driver.implicitly_wait(5)
    driver.get('https://www.x-kom.pl')
    driver.maximize_window()

    # click cookie accept
    driver.find_element(By.XPATH, "//button[text()='W porządku']").click()

    # choose type of product
    if type_product=='Smartphone':
        driver.find_element(By.XPATH, '//ul[@class="sc-1ktmy3g-2 iXwiqH"]/li[2]').click()
        driver.find_element(By.XPATH, "//span[@class='sc-1tblmgq-0 joe0ba-2 kTwLqk sc-1tblmgq-3 jMzGaB']").click()
    elif type_product=='TV':
        driver.find_element(By.XPATH, "//li[@class='sc-13hctwf-3 kOeglL'][6]").click()
        driver.find_element(By.XPATH, "//span[@class='sc-1tblmgq-0 joe0ba-2 kTwLqk sc-1tblmgq-3 jMzGaB']").click()
        


    # choose brand
    brand= brand[0].upper() + brand[1:].lower()
    #driver.find_element(By.XPATH, f'//span[@class="sc-1sjec7y-1 dqUbGF" and text()="{brand}"]').click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f'//span[@class="sc-1sjec7y-1 dqUbGF" and text()="{brand}"]'))).click()

    list_of_phones = []

    time.sleep(1)
    num_of_pages = driver.find_element(By.XPATH, "//span[@class='sc-11oikyw-2 ekasrY']").text
    print(num_of_pages)
    num = int(re.findall(r'\d+', num_of_pages)[0])

    for n in range(num):
        time.sleep(1.5)
        names = driver.find_elements(By.XPATH, "//span[contains(@style, 'display: -webkit-box;')]")
        prices = driver.find_elements(By.XPATH, "//span[@class='sc-6n68ef-0 sc-6n68ef-3 iepkXv']")
        if type_product=='TV':
            resolutions = driver.find_elements(By.XPATH, "//li[contains(text(), 'Przekątna')]")
            
        if type_product=='Smartphone':
            for name, price in zip(names, prices):
                print(f'name- {name.text}, price-{price.text}')
                list_of_phones.append({'name':name.text, 'price':price.text})
        
        elif type_product=='TV':
            for name, resol, price in zip(names, resolutions, prices):
                print(f'name- {name.text}, resol- {resol.text}, price-{price.text}')
                list_of_phones.append({'name':name.text, 'resol':resol.text, 'price':price.text})

        else:
            raise ValueError("Program doesn't recognize this type of product")
        
        try:
            next_page = driver.find_element(By.XPATH, "//span[text()='Następna']/..")
            next_page.click()
            time.sleep(1)
            driver.get(driver.current_url)

        except NoSuchElementException as e:
            print(e)
            break

    # save result as JSON file 
    data_dict = {}
    data_dict[brand.upper()] = list_of_phones
    json_string = json.dumps(data_dict)
    with open(f'json_files/xkom_{brand.upper()}_{type_product}.json', 'w+') as f:
        f.write(json_string)

