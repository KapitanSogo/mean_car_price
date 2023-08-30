import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd

result_data = {'data': {}}

with open('../json_avito/marks_models_all.json', 'r', encoding='utf-8') as file:
    marks_models_all = json.load(file)

df = pd.DataFrame(
    columns=['mark', 'name_model', 'type_of_car', 'type_of_drive', 'type_fuel', 'engine', 'power', 'mileage',
             'is_broken', 'price'])

driver = webdriver.Chrome()
driver.set_window_size(1200, 800)
driver.set_window_position(0, 0)

count_models = 0
for mark, models in marks_models_all['data'].items():
    for name_model, name_in_url in models.items():
        count_models += name_in_url.count('-')

print(f'Всего моделей: {count_models}')
count = 0

for mark, models in marks_models_all['data'].items():
    for name_model, name_in_url in models.items():
        url = f'https://www.avito.ru/yaroslavskaya_oblast/avtomobili/{mark}/{name_in_url}&localPriority=1'
        # url = f'https://www.avito.ru/yaroslavskaya_oblast/avtomobili/vaz_lada/niva_travel-ASgBAgICAkTgtg3GmSjitg3uyz8?cd=1&localPriority=1'
        driver.get(url)


        def find():
            count_for_price = 0
            final_price = []
            ads = driver.find_element(By.XPATH, '//*[@data-marker="catalog-serp"]')
            try:
                driver.execute_script(
                    """ var element = document.querySelector('[data-marker="witcher/block"]'); element.parentNode.removeChild(element); """)
            except:
                pass
            soup = BeautifulSoup(ads.get_attribute('innerHTML'), 'html.parser')
            prices = soup.find_all('div', class_='price-price-JP7qe')
            for price in prices:
                price = price.find('p',
                                   class_='styles-module-root-_KFFt styles-module-size_l-_oGDF styles-module-size_l_dense-Wae_G styles-module-size_l-hruVE styles-module-size_dense-z56yO stylesMarningNormal-module-root-OSCNq stylesMarningNormal-module-paragraph-l-dense-TTLmp')
                if price:
                    price = price.text
                    price = price.replace('\xa0', '')
                    price = price.replace('₽', '')
                    try:
                        final_price.append(int(price))
                    except:
                        final_price.append(int(price.split('от ')[1]))
            descriptions = soup.find_all('div', class_='iva-item-autoParamsStep-WzfS8')
            for description in descriptions:
                ad = description.find('p',
                                      class_='styles-module-root-_KFFt styles-module-size_s-awPvv styles-module-size_s-_P6ZA stylesMarningNormal-module-root-OSCNq stylesMarningNormal-module-paragraph-s-_c6vD')
                if ad:

                    ad = ad.text
                    ad = ad.split(', ')
                    type_fuel = ad[len(ad) - 1]
                    type_of_drive = ad[len(ad) - 2]
                    type_of_car = ad[len(ad) - 3]
                    engine = ad[len(ad) - 4]
                    power = int(engine.split(' (')[1].split(' ')[0].split('л.с.)')[0])
                    try:
                        mileage = int(ad[len(ad) - 5].split(' ')[0].replace('\xa0', '').replace('км', ''))
                    except:
                        mileage = 0
                    try:
                        if ad[0] == 'Битый':
                            is_broken = True
                        else:
                            is_broken = False
                    except:
                        is_broken = False

                    df.loc[len(df)] = [mark, name_in_url.split('-')[0], type_of_car, type_of_drive, type_fuel, engine,
                                       power, mileage,
                                       is_broken, final_price[count_for_price]]
                    count_for_price += 1
                    df.to_csv('../csv_avito/avito_yar_obl.csv', index=False)
                else:
                    pass

            return count_for_price


        find()
        if driver.find_elements(By.XPATH, '//*[@data-marker="pagination-button/page(2)"]'):
            driver.find_element(By.XPATH, '//*[@data-marker="pagination-button/page(2)"]').click()
            time.sleep(2)
            # если адресная строка поменялась, то выполняем функцию find()
            if driver.current_url != url:
                find()

        count += 1
        print(f'{count} из {count_models}')

time.sleep(10)
