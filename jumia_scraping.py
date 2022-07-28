# for more information visit our web site : https://www.pythonaa.com/

import requests
from bs4 import BeautifulSoup
import pandas as pd
from jumia_model import Brand

brands = [
    Brand('amir', 1),
    Brand('bingo', 1),
    Brand('bref', 1),
    Brand('brand-brilex', 1),
    Brand('force-xpress', 1),
    Brand('life', 1),
    Brand('test', 1),

]

# url = 'https://www.jumia.dz/jus-boissons-bebe/?page='
# url='https://www.jumia.dz/epicerie-eau-javel/'+ Brand.name +'/#catalog-listing'

columns = {'product_type':[],'category':[],'sub_category':[],'brand':[],'name': [], 'price': [],'old_price':[],'percentage':[], 'img url': [],}
def look_for_brands(brands):
    for Brand in brands:
        print('---', Brand.name, '---')
        url='https://www.jumia.dz/epicerie-eau-javel/'+ Brand.name +'/#catalog-listing'
        for page in range(1, Brand.pages+1):
            print('---', page, '---')
            r = requests.get(url + str(page))
            soup = BeautifulSoup(r.content, "html.parser")
            ancher = soup.find('div', {'class': '-paxs row _no-g _4cl-3cm-shs'}
                               ).find_all('article', {'class': 'prd _fb col c-prd'})

            ancher2= soup.find('div',{'class':'brcbs col16 -pvs'}).find_all('a', {'class': 'cbs'})

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
                columns['brand'].append(ancher2[4].text)
                columns['name'].append(name.text)
                columns['price'].append(price.text)
                if(old_price is not None):
                    columns['old_price'].append(old_price.contents[0].text)
                    columns['percentage'].append(old_price.contents[1].text)
                else:
                    columns['old_price'].append('')
                    columns['percentage'].append('')
                columns['img url'].append(img.get('data-src'))


        data = pd.DataFrame(columns)
        data.to_excel('jumia_eau_de_javel.xlsx')

def main():
    look_for_brands(brands)


if __name__ == '__main__':
    main()