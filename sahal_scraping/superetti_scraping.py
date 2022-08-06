# for more information visit our web site : https://www.pythonaa.com/

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

max_pages=2
categories=[]
categories_names=[]
url = 'https://superetti.dz'

# columns = {'category':[],'name': [], 'price': [], 'img url': []}
def look_for_categories():
    r3 = requests.get(url)
    soup3 = BeautifulSoup(r3.content, "html.parser")
    ancher4 = soup3.find('ul',{'class':'menu wd-cat-nav'}).find_all('li')
    for pt in ancher4:
        a_tag = pt.find('a',{'class':'woodmart-nav-link'},href=True)
        categories.append(a_tag.attrs['href'])
        categories_names.append(a_tag.text)
def look_for_pages(categories,categories_names):
    for i in range(len(categories)):
        print('---', categories[i], '---')
        print('---', categories_names[i], '---')
        r2 = requests.get(categories[i])
        soup2 = BeautifulSoup(r2.content, "html.parser")
        try:
            ancher3 = soup2.find('ul',{'class':'page-numbers'}).find_all('li')
            global max_pages
            max_pages=int(ancher3[-2].text)
            print(max_pages)
            look_for_products(max_pages,categories_names[i],categories[i])
        except:
            look_for_products(1,categories_names[i],categories[i])
            pass


def look_for_products(int,file_name,category_url):
    if ' ' in file_name:
        real_file_name=file_name.replace(' ','_')
    else:
        real_file_name=file_name
    columns = {'category':[],'sub_category':[],'sub_sub_category':[],'sub_sub_sub_category':[],'name': [], 'price': [], 'img url': []}
    for i in range(1, int+1):
        print('---', i, '---')
        r = requests.get(category_url +'page/'+ str(i) + '/')
        soup = BeautifulSoup(r.content, "html.parser")
        try:
            ancher = soup.find('div',class_=re.compile("products elements-grid align-items-start")
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
                            price = pt.find('span', {'class': 'price'}).find('ins',).find('span', {'class': 'woocommerce-Price-amount amount'}).find('bdi')
                        except:
                            price = None
                    try:
                        description = pt.find('div', {'class': 'woodmart-product-cats'}).find_all('a')
                    except:
                        pass

                    columns['category'].append(file_name)
                    try:
                        columns['sub_category'].append(description[0].text)
                    except:
                        columns['sub_category'].append(' ')
                    try:
                        columns['sub_sub_category'].append(description[1].text)
                    except:
                        columns['sub_sub_category'].append(' ')
                    try:
                        columns['sub_sub_sub_category'].append(description[2].text)
                    except:
                        columns['sub_sub_sub_category'].append(' ')
                    columns['name'].append(name.text)
                    try:
                        columns['price'].append(price.text)
                    except:
                        columns['price'].append(' ')
                    columns['img url'].append(img.get('data-src'))

            data = pd.DataFrame(columns)
            data.to_excel('superetti_'+real_file_name+'.xlsx')
        except Exception as e:
            print(e)


def main():
    look_for_categories()
    look_for_pages(categories,categories_names)

if __name__ == '__main__':
    main()
