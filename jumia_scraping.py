# for more information visit our web site : https://www.pythonaa.com/

import requests
from bs4 import BeautifulSoup
import pandas as pd

brands=['bingo','amir']

# url = 'https://www.jumia.dz/jus-boissons-bebe/?page='

columns = {'product_type':[],'category':[],'sub_category':[],'name': [], 'price': [], 'img url': [],}
def main():
    for brand in brands:
        print('---', brand, '---')
        url = 'https://www.jumia.dz/produit-lessive/'+ brand +'/#catalog-listing'
        for page in range(1, 2):
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

                columns['product_type'].append(ancher2[1].text)
                columns['category'].append(ancher2[2].text)
                columns['sub_category'].append(ancher2[3].text)
                columns['name'].append(name.text)
                columns['price'].append(price.text)
                columns['img url'].append(img.get('data-src'))


        data = pd.DataFrame(columns)
        data.to_excel('jumia_boisson.xlsx')

if __name__ == '__main__':
    main()