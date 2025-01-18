import time
from selenium import webdriver
from selenium.common import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import Workbook

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(url="https://example.com")

button = True
while button:
    try:
        load_button = driver.find_element(By.CLASS_NAME, "pager__item")
        try:
            load_button.click()
        except:
            time.sleep(1)
    except:
        web = driver.find_element(By.TAG_NAME, "body").get_attribute("outerHTML")
        with open("web_content.html", "w", encoding="utf-8") as file:
            file.write(web)
        button = False

with open("web_content.html", "r", encoding="utf-8") as file:
    web_elements = file.read()

soup = BeautifulSoup(web_elements, "html.parser")

company_location = soup.find_all("div", class_="category")
company_name = soup.find_all("h3", class_="job_title")
all_links = soup.find_all("div", class_="fee")

''' Extracting location '''
location = []
for locations in company_location:
    get_location = locations.text
    location.append(get_location)

''' Extracting Company name '''
name = []
for names in company_name:
    get_name = names.text
    name.append(get_name)

''' Extracting links '''
for company in all_links:
    with open("link.html", "a") as file:
        file.write(f"\n{company}")

with open("link.html", "r") as file:
    elements = file.read()
soup_2 = BeautifulSoup(elements, "html.parser")
a_tag = soup_2.find_all('a', href=True)

links = []
for i in range(len(a_tag)):
    a = str(a_tag[i]).split('"')
    links.append(a[1])

company_dict = []
for i in range(len(name)):
    get_list = {"Organization": name[i], "location": location[i], "website": links[i]}
    company_dict.append(get_list)

'''Exporting to xlsx file using pandas'''
df = pd.DataFrame(company_dict)
df.to_excel("company_list.xlsx", index=False)
driver.quit()
