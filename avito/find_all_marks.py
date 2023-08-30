import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

url = f'https://www.avito.ru/all/avtomobili'


names = []
names_in_url = []

driver = webdriver.Chrome()
driver.set_window_size(1200, 800)
driver.set_window_position(0, 0)
driver.get(url)
driver.find_element(By.CLASS_NAME, 'popular-rubricator-button-WWqUy').click()
elements = driver.find_elements(By.CLASS_NAME, 'popular-rubricator-link-Hrkjd')
for element in elements:
    names.append(element.text)
    names_in_url.append(element.get_attribute('href').split('/')[-1])

count = names.count('')
names_in_url = names_in_url[:-count]
names = list(filter(None, names))

with open('json_avito/marks.json', 'w', encoding='utf-8') as file:
    json.dump(dict(zip(names, names_in_url)), file, indent=4, ensure_ascii=False)
