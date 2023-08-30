import json
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0"
}

data_models = {'data': {}}

# TODO: переписать на json и брать оттуда
# собрано один раз в find_all_marks и больше не трогать
name_models = ['AC', 'Acura', 'AITO', 'Alfa Romeo', 'Alpina', 'Aro', 'Aston Martin', 'Audi', 'Avatr', 'BAIC', 'Baojun',
               'Barkas', 'BAW', 'Bedford', 'Bentley', 'BMW', 'Brilliance', 'Bugatti', 'Buick', 'BYD', 'Cadillac',
               'Changan', 'Changhe', 'Chery', 'Chevrolet', 'Chrysler', 'Citroen', 'Cupra', 'Dacia', 'Dadi', 'Daewoo',
               'Daihatsu', 'Datsun', 'Dayun', 'DeLorean', 'Denza', 'Derways', 'Dodge', 'Dongfeng', 'DW Hower',
               'Evolute',
               'EXEED', 'FAW', 'Ferrari', 'Fiat', 'Fisker', 'Ford', 'Forthing', 'Foton', 'GAC', 'Geely', 'Genesis',
               'Geo', 'GMC', 'Great Wall', 'Hafei', 'Haima', 'Haval', 'Hawtai', 'HiPhi', 'Honda', 'Hongqi', 'Hozon',
               'Hummer', 'Hyundai', 'IM Motors', 'Infiniti', 'Iran Khodro', 'Isuzu', 'IVECO', 'JAC', 'Jaecoo', 'Jaguar',
               'Jeep', 'Jetour', 'Jetta', 'Jinbei', 'Kaiyi', 'Kia', 'Kuayue', 'Lamborghini', 'Lancia', 'Land Rover',
               'Landwind', 'Leapmotor', 'Lexus', 'Li', 'Lifan', 'Lincoln', 'Livan', 'Lotus', 'Lucid', 'Luxgen',
               'Lynk & Co', 'Marussia', 'Maserati', 'Maxus', 'Maybach', 'Mazda', 'McLaren', 'Mercedes-Benz', 'Mercury',
               'MG', 'MINI', 'Mitsubishi', 'Mitsuoka', 'Nio', 'Nissan', 'Oldsmobile', 'OMODA', 'Opel', 'Oshan',
               'Pagani',
               'Peugeot', 'Piaggio', 'Plymouth', 'Polestar', 'Pontiac', 'Porsche', 'Qingling', 'Radar', 'RAM', 'Ravon',
               'Renault', 'Renault Samsung', 'Rimac', 'Rising Auto', 'Rivian', 'Roewe', 'Rolls-Royce', 'Rover', 'Saab',
               'SAIPA', 'Saturn', 'Scion', 'SEAT', 'Seres', 'Shineray', 'Shuanghuan', 'Skoda', 'Skywell', 'Smart',
               'Soueast', 'SsangYong', 'Subaru', 'Suzuki', 'SWM', 'Tank', 'TATA', 'Tesla', 'Tianma', 'Tianye', 'Toyota',
               'VGV', 'Volkswagen', 'Volvo', 'Vortex', 'Voyah', 'Weltmeister', 'WEY', 'Wuling', 'Xpeng', 'Yangwang',
               'Zeekr', 'Zotye', 'ZX', 'Аурус', 'Богдан', 'ГАЗ', 'Донинвест', 'ЗАЗ', 'ЗИЛ', 'ЗиС', 'ИЖ', 'Лада', 'ЛуАЗ',
               'Москвич', 'ТагАЗ', 'УАЗ']

name_models_links = ['ac', 'acura', 'aito', 'alfa_romeo', 'alpina', 'aro', 'aston_martin', 'audi', 'avatr', 'baic',
                     'baojun', 'barkas',
                     'baw', 'bedford', 'bentley', 'bmw', 'brilliance', 'bugatti', 'buick', 'byd', 'cadillac', 'changan',
                     'changhe', 'chery',
                     'chevrolet', 'chrysler', 'citroen', 'cupra', 'dacia', 'dadi', 'daewoo', 'daihatsu', 'datsun',
                     'dayun', 'delorean',
                     'denza', 'derways', 'dodge', 'dongfeng', 'dw_hower', 'evolute', 'cheryexeed', 'faw', 'ferrari',
                     'fiat', 'fisker',
                     'ford', 'forthing', 'foton', 'gac', 'geely', 'genesis', 'geo', 'gmc', 'great_wall', 'hafei',
                     'haima', 'haval',
                     'hawtai', 'hiphi', 'honda', 'hongqi', 'hozon', 'hummer', 'hyundai', 'im_motors', 'infiniti',
                     'iran_khodro', 'isuzu',
                     'iveco', 'jac', 'jaecoo', 'jaguar', 'jeep', 'jetour', 'jetta', 'jinbei', 'kaiyi', 'kia', 'kuayue',
                     'lamborghini',
                     'lancia', 'land_rover', 'landwind', 'leapmotor', 'lexus', 'li', 'lifan', 'lincoln', 'livan',
                     'lotus', 'lucid',
                     'luxgen', 'lynk_and_co', 'marussia', 'maserati', 'maxus', 'maybach', 'mazda', 'mclaren',
                     'mercedes-benz', 'mercury',
                     'mg', 'mini', 'mitsubishi', 'mitsuoka', 'nio', 'nissan', 'oldsmobile', 'omoda', 'opel', 'oshan',
                     'pagani', 'peugeot',
                     'piaggio', 'plymouth', 'polestar', 'pontiac', 'porsche', 'qingling', 'radar', 'ram', 'ravon',
                     'renault',
                     'renault_samsung', 'rimac', 'rising_auto', 'rivian', 'roewe', 'rolls-royce', 'rover', 'saab',
                     'saipa', 'saturn',
                     'scion', 'seat', 'seres', 'shineray', 'shuanghuan', 'skoda', 'skywell', 'smart', 'soueast',
                     'ssang_yong', 'subaru',
                     'suzuki', 'swm', 'tank', 'tata', 'tesla', 'tianma', 'tianye', 'toyota', 'vgv', 'volkswagen',
                     'volvo', 'vortex',
                     'voyah', 'weltmeister', 'wey', 'wuling', 'xpeng', 'yangwang', 'zeekr', 'zotye', 'zx', 'aurus',
                     'bogdan', 'gaz',
                     'doninvest', 'zaz', 'zil', 'zis', 'izh', 'lada', 'luaz', 'moskvitch', 'tagaz', 'uaz']

for name_model in name_models_links:
    url = f'https://www.drom.ru/catalog/{name_model}/'
    print(url)
    response = requests.get(url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    models_all = soup.find_all('script', type='text/javascript')
    models = models_all[-2]
    models = models.get('data-drom-module-data')
    models = models.split('[')[1]
    models = models.split(']')[0]
    models = '[' + models + ']'
    data_models['data'].update({f'{name_model}': json.loads(models)})

    for item in data_models['data'][f'{name_model}']:
        del item['hasPanorama']
        url = item['url']
        url = url.split('/')
        url = url[-2]
        del item['url']
        item['name_in_url'] = url

models = json.dumps(data_models, indent=4, sort_keys=True)
with open(f'json_avito/marks_models_all.json', 'w', encoding='utf-8') as file:
    file.write(models)
