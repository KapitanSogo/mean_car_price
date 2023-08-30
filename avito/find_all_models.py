import json
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

result_data = {'data': {}}
names = []
names_in_url = []

driver = webdriver.Chrome()
driver.set_window_size(1200, 800)
driver.set_window_position(0, 0)
driver.get("https://www.avito.ru/all/avtomobili/")
#таймаут на авторизацию руками
time.sleep(60)

with open('../json_avito/marks.json', 'r', encoding='utf-8') as file:
    marks = json.load(file)

for names, names_in_url in marks.items():
    url = f'https://www.avito.ru/all/avtomobili/{names_in_url}'
    driver.get(url)
    try:
        driver.find_element(By.CLASS_NAME, 'popular-rubricator-button-WWqUy').click()
    except:
        pass
    elements = driver.find_elements(By.CLASS_NAME, 'popular-rubricator-link-Hrkjd')
    result_data['data'].update({names_in_url.split('-')[0]: {}})
    temp_dict ={}
    for element in elements:
        temp_dict.update({
            f'{element.text}': element.get_attribute('href').split('/')[-1]
                     })
    result_data['data'][names_in_url.split('-')[0]].update(temp_dict)

with open('../json_avito/marks_models_all.json', 'w', encoding='utf-8') as file:
    json.dump(result_data, file, indent=4, ensure_ascii=False)
