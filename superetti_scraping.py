# for more information visit our web site : https://www.pythonaa.com/

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = 'https://superetti.dz/categorie-produit/epicerie-sucree/page/'

columns = {'name': [], 'price': [], 'img url': []}


def main():
    for page in range(1, 2):
        print('---', page, '---')
        r = requests.get(url + str(page) + '/')
        soup = BeautifulSoup(r.content, "html.parser")

        ancher = soup.find('div', {
            'class': 'products elements-grid align-items-start woodmart-products-holder woodmart-spacing-20 pagination-pagination row grid-columns-4'}
                           ).find_all('div', class_=re.compile(
            "product-grid-item product woodmart-hover-standard col-md-3 col-sm-4 col-6"))

        # print(ancher)
        for pt in ancher:
            img = pt.find('div', {'class': 'product-element-top'}).find('a', {'class': 'product-image-link'}).find(
                'img')

            name = pt.find('h3', {'class': 'product-title'}).find('a')

            price = pt.find('span', {'class': 'price'}).find('span', {'class': 'woocommerce-Price-amount amount'}).find(
                'bdi')

            columns['name'].append(name.text)
            columns['price'].append(price.text)
            columns['img url'].append(img.get('data-src'))

    data = pd.DataFrame(columns)
    data.to_excel('superetti.xlsx')


if __name__ == '__main__':
    main()
