# for more information visit our web site : https://www.pythonaa.com/
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
import codecs

chapters = []
chapter = None
chapters_merge = []
chapter_urls = []
url = 'http://hisnulmuslim.com/index-page-liste-lang-fr.html'


# columns = {'category':[],'name': [], 'price': [], 'img url': []}
def look_for_chapters():
    r3 = requests.get(url)
    soup3 = BeautifulSoup(r3.content, "html.parser")
    ancher4 = soup3.find('div', {'id': 'middle'}).find('ul').find_all('li')
    del ancher4[0:5]
    co = 1
    position = 8
    for pt in ancher4:
        a_tag = pt.find('a', href=True)
        chapter_urls.append(a_tag.get('href'))
        categoty_name = re.sub('\d', '', a_tag.text)
        categoty_name2 = re.sub('  - ', '', categoty_name)
        categories_names = categoty_name2[:position] + ': ' + categoty_name2[position:]
        chapters_merge.append(categories_names)
        # print(categories_names)
        chapter = {}
        chapter['id'] = co
        chapter['title_fr'] = categories_names
        chapters.append(chapter)
        co = co + 1
    chapters_merge.insert(10, ' ')
    chapter_urls.insert(10, ' ')
    # print(chapters_merge)
    # merge_chapters(chapters_merge)
    look_for_adkar(chapter_urls)

def look_for_adkar(urls):
    co2=0
    translit_list=[]
    for i in range(0, len(urls)):
    # for i in range(0, 20):
        print('---', i+1, '---')
        if urls[i] != ' ':
            r = requests.get(urls[i])
            soup = BeautifulSoup(r.content, "html.parser")
            ancher = soup.find('div',{'id':'middle'}).find_all('p',{'class':'txt_trans'})

            for pt in ancher:
                corrected_text=pt.text
                translit_list.append(corrected_text)
                # print(corrected_text)
    # adkar_list.insert(72, ' ')
    # adkar_list.insert(98, ' ')
    co2=co2+len(translit_list)
    print(co2)
    with codecs.open('hisn-muslim-translit_fr.json', 'w', 'utf-8') as outfile:
        outfile.write(json.dumps(translit_list, ensure_ascii=False, indent=2))




def merge_chapters(list):
    data = json.load(codecs.open('hisn-muslim-chapters.json', 'r', 'utf-8'))
    for d in data:
        d["title_fr"] = list[d["id"] - 1]
    with codecs.open('hisn-muslim-chapters.json','w','utf-8') as outfile:
        outfile.write(json.dumps(data, ensure_ascii=False, indent=2))

def merge_adkar(list):
    data = json.load(codecs.open('hisn-muslim-supps.json', 'r', 'utf-8'))
    for d in data:
        d["text_fr"]=list[d["id"]-1]
    with codecs.open('hisn-muslim-supps.json','w','utf-8') as outfile:
        outfile.write(json.dumps(data, ensure_ascii=False, indent=2))

def main():
    look_for_chapters()
    # look_for_adkar(chapter_urls)


if __name__ == '__main__':
    main()
