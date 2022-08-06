import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = 'https://superetti.dz/categorie-produit/entretien-et-nettoyage/page/'

columns = {'category':[],'sub_category':[],'sub_sub_category':[],'name': [],
           'price': [],
           'img url': []}


def main():
    for page in range(1, 27):
        print('---', page, '---')
        r = requests.get(url + str(page) + '/')
        soup = BeautifulSoup(r.content, "html.parser")

        ancher = soup.find('div', {
            'class': 'products elements-grid align-items-start woodmart-products-holder woodmart-spacing-20 pagination-pagination row grid-columns-4'}
                           ).find_all('div', class_=re.compile(
            "product-grid-item"))

        for pt in ancher:
            img = pt.find('div', {'class': 'product-element-top'}).find('a', {'class': 'product-image-link'}).find(
                'img')

            name = pt.find('h3', {'class': 'product-title'}).find('a')

            try:
                price = pt.find('span', {'class': 'price'}).find('span', {'class': 'woocommerce-Price-amount amount'}).find('bdi')
            except:
                try:
                    price = pt.find('span', {'class': 'price'}).find('del',).find('span', {'class': 'woocommerce-Price-amount amount'}).find('bdi')
                except:
                    price = None




            description = pt.find('div', {'class': 'woodmart-product-cats'}).find_all('a')

            try:
                columns['category'].append(file_name)
            except:
                columns['category'].append(' ')
            try:
                columns['sub_category'].append(description[0].text)
            except:
                columns['sub_category'].append(' ')
            try:
                columns['sub_sub_category'].append(description[0].text)
            except:
                columns['sub_sub_category'].append(' ')
            columns['name'].append(name.text)
            try:
                columns['price'].append(price.text)
            except:
                columns['price'].append('None')
            columns['img url'].append(img.get('data-src'))

    data = pd.DataFrame(columns)
    data.to_excel('superetti.xlsx')


if __name__ == '__main__':
    main()