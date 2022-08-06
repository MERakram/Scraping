# for more information visit our web site : https://www.pythonaa.com/

import requests
from bs4 import BeautifulSoup
import pandas as pd
from jumia_model import Brand
import re

brands_list=[]

base_url='https://www.jumia.dz/'

#
#
url2=base_url+'sante-beaute-dentifrice/'
#
#

columns = {'product_type': [],
           'category': [],
           'sub_category': [],
           # 'sub_sub_category': [],
           # 'sub_sub_sub_category': [],
           # 'sub_sub_sub_sub_category': [],
           'brand': [], 'name': [],'price': [],
           'old_price': [], 'percentage': [], 'img url': [], }

def look_for_brands():
    r2 = requests.get(url2)
    soup2 = BeautifulSoup(r2.content, "html.parser")
    ancher3 = soup2.find('div',class_=re.compile(
        "-phs -pvxs -df -d-co")).find_all('a', {'class': 'fk-cb -me-start -fsh0'}, href=True)
    for pt in ancher3:
        brands_list.append(pt.attrs['href'])
def look_for_products(brands_list):
    for brand in brands_list:
        print('---', brand, '---')
        url = base_url+brand
        for page in range(1, 2):
            print('---', page, '---')
            r = requests.get(url + str(page))
            soup = BeautifulSoup(r.content, "html.parser")

            ancher = soup.find('div', {'class': '-paxs row _no-g _4cl-3cm-shs'}
                               ).find_all('article', {'class': 'prd _fb col c-prd'})

            ancher2 = soup.find('div', {'class': 'brcbs col16 -pvs'}).find_all('a', {'class': 'cbs'})

            for pt in ancher:
                img = pt.find('a').find(
                    'div', {'class': 'img-c'}).find('img', {'class': 'img'})

                name = pt.find('a').find('div', {'class': 'info'}).find(
                    'h3', {'class': 'name'})

                price = pt.find('a').find('div', {'class': 'info'}).find(
                    'div', {'class': 'prc'})

                old_price = pt.find('a').find('div', {'class': 'info'}).find(
                    'div', {'class': 's-prc-w'})

                columns['product_type'].append(ancher2[1].text)
                columns['category'].append(ancher2[2].text)
                columns['sub_category'].append(ancher2[3].text)
                # columns['sub_sub_category'].append(ancher2[4].text)
                # columns['sub_sub_sub_category'].append(ancher2[5].text)
                # columns['sub_sub_sub_sub_category'].append(ancher2[6].text)
                columns['brand'].append(ancher2[4].text)
                columns['name'].append(name.text)
                columns['price'].append(price.text)
                if (old_price is not None):
                    columns['old_price'].append(old_price.contents[0].text)
                    columns['percentage'].append(old_price.contents[1].text)
                else:
                    columns['old_price'].append('')
                    columns['percentage'].append('')
                columns['img url'].append(img.get('data-src'))

        data = pd.DataFrame(columns)
        data.to_excel('jumia_sante_beaute_dentifrice.xlsx')


def main():
    look_for_brands()
    look_for_products(brands_list)


if __name__ == '__main__':
    main()
