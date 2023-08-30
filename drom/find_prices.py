import json
import requests
from bs4 import BeautifulSoup


url = 'https://auto.drom.ru/region76/nissan/x-trail/'

headers = {
    "User-Agent": "Mozilla/5.0"
}

result_data = {'data': {'offers': {}}}

response = requests.get(url, headers=headers)
html = response.text
soup = BeautifulSoup(html, 'html.parser')
info = soup.find('script', type='application/ld+json')
info = eval(info.text)

offers = info['offers']['offers']
result_data['data']['offers'] = offers
for offer in result_data['data']['offers']:
    del offer['@type']
    del offer['availability']
    del offer['priceCurrency']
    del offer['priceValidUntil']

# offers = json.dumps(result_data, indent=4, sort_keys=True)
# with open('json_drom/info.json', 'w', encoding='utf-8') as file:
#     file.write(offers)
#
# with open('json_drom/info.json', 'r', encoding='utf-8') as file:
#     offers = json.load(file)
#
# data = offers['data']['offers']

if result_data:
    count_offers = len(result_data['data']['offers'])
    price = 0
    for offer in result_data['data']['offers']:
        price += offer['price']
    average_price = price / count_offers
    print(average_price)