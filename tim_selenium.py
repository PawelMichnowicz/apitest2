from tkinter import E
from selenium import webdriver
from selenium.webdriver.common.keys import Keys # acces to exc/enter itd keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

PATH = r'C:\Program Files (x86)/chromedriver.exe'

# options for hide "Failed to read descriptor from node connection"
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])


driver = webdriver.Chrome(PATH, options=options)
driver.get('https://www.olx.pl/elektronika/telefony/') #driver.page_source for html file

cookies = driver.find_element(By.ID,"onetrust-accept-btn-handler").click()

search = driver.find_element(By.ID,'search-text')
search.send_keys('samsung')
search.send_keys(Keys.RETURN) # click enter

###################################
# try: #wait max 10 sec
#     print('yeaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
#     table = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "offers_table"))
#     )
#     offers = table.find_elements(By.CLASS_NAME, 'offer')
#     for offer in offers:
#         print(30*'-')
#         elements = offer.find_elements(By.TAG_NAME,'strong')
#         if len(elements) == 2:
#             print(f"Name - {elements[0].text}, Price - {elements[1].text}")

#     next_page = driver.find_element(By.XPATH, "//a[@class='link pageNextPrev {page:2}']")
#     driver.execute_script("arguments[0].click();", next_page)
    
# finally:
#     driver.quit()
##################################

number_of_pages = 5
list_of_phones = []
for num in range(2, number_of_pages+2):
    time.sleep(3)
    table = driver.find_element(By.ID, "offers_table")
    offers = table.find_elements(By.CLASS_NAME, 'offer')
    for offer in offers:
            print(30*'-')
            elements = offer.find_elements(By.TAG_NAME,'strong')
            if len(elements) == 2:
                print(f"Name - {elements[0].text}, Price - {elements[1].text}")
                list_of_phones.append({'Name': elements[0].text, 'Price': elements[1].text})
    next_page = driver.find_element(By.XPATH, f"//a[@class='link pageNextPrev {{page:{num}}}']")
    driver.execute_script("arguments[0].click();", next_page)


driver.quit() # close() for tab? / quit() close whole website




