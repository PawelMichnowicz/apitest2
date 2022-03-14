from tkinter import E
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys  # acces to exc/enter itd keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import json

def avans(brand='SAMSUNG', type_product='Smartphone'):
    brand = brand.upper()

    PATH = r'C:\Program Files (x86)/chromedriver.exe'

    # options for hide "Failed to read descriptor from node connection"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(PATH, options=options)
    driver.implicitly_wait(5)
    driver.get('https://www.avans.pl/')
    driver.maximize_window()

    # cookie accept
    driver.find_element(By.XPATH, "//label[@class='c-alert_close']").click()

    # choose type of product
    if type_product=='Smartphone':
        driver.find_element(
            By.XPATH, "//div[@class='c-menu clearfix is-mainShopMenu is-withColumns']/ul[@data-component = 'accordion']").click()
        driver.find_element(By.XPATH, "//img[@alt='SMARTFONY I TELEFONY']").click()
    
    elif type_product=='TV':
        driver.find_element(By.XPATH, "//a[contains(text(), 'TV, Audio')]").click()
        driver.find_element(By.XPATH, "//img[@alt='TELEWIZORY']").click()

    else:
        raise ValueError("Program doesn't recognize this type of product")
    # choose model
    brand = brand.upper()
    model_phone = driver.find_element(
        By.XPATH, f"//span[contains(text(),'{brand}')]")
    driver.execute_script("arguments[0].click();", model_phone)
    filter_button = driver.find_element(By.XPATH, "//button[@class='c-btn ']")
    driver.execute_script("arguments[0].click();", filter_button)

    list_of_phones = []
    while True:
        prices = driver.find_elements(By.XPATH, "//div[@class = 'a-price_new  is-big  ']/span[1]")
        names = driver.find_elements(By.XPATH, "//a[@class='a-typo is-secondary']")

        if type_product=='Smartphone':
            for price, name in zip(prices, names):
                list_of_phones.append({'name': name.text, 'price': price.text})
                print(f"price - {price.text}, name = {name.text}")
        
        elif type_product=='TV':
            resolutions = driver.find_elements(By.XPATH, "//div[@data-zone='OFFERBOX_ATTRIBUTES']//tr[1]/td[2]")
            for price, resol, name in zip(prices, resolutions, names):
                list_of_phones.append({'name': name.text,'resol': resol.text,  'price': price.text})
                print(f"price - {price.text}, resol - {resol.text}, name = {name.text}")

        else:
            raise ValueError("Program doesn't recognize this type of product")

        try:
            driver.find_element(By.XPATH, "//a[@class='is-nextLink']").click()
            #WebDriverWait(driver, 10).until( EC.element_to_be_clickable((By.XPATH, "//a[@class='is-nextLink']/.."))).click()
            driver.get(driver.current_url)

        except NoSuchElementException as e:
            print(30*'=')
            break

    data_dict = {}
    data_dict[brand] = list_of_phones
    json_string = json.dumps(data_dict)
    with open(f'json_files/avans_{brand}_{type_product}.json', 'w+') as f:
        f.write(json_string)

