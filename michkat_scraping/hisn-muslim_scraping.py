
import requests
from pathlib import Path
import json
from copy import copy

import bs4
from bs4 import BeautifulSoup

url = 'https://sunnah.com/hisn'

def main():

    hm_html_doc = requests.get(url)
    # soup = BeautifulSoup(r.content, "html.parser")
    # hm_html_doc_fp = Path('hisn-muslim.html')

# if not hm_html_doc_fp.exists():
#     print('the html doc for hisn el muslim does not exist')
#     exit()

# hm_html_doc = hm_html_doc_fp.read_text()

    hm_html_data = BeautifulSoup(hm_html_doc.content, 'html.parser')

# print(hm_html_data.find_all(class_='arabicchapter arabic'))

    supp_html = hm_html_data.find(class_='AllHadith')
# print(supplications_html)
    supp_chapters = []
    supp_chapter = None

    chapters_list = []
    supps_list = []

    supps_with_issue = []

    chapter_id = 1
    supp_id = 1

    for supp_html_child in supp_html.children:
        if isinstance(supp_html_child, bs4.element.Tag):
            # print(supp_html_child.get('class'))
            if supp_html_child.get('class') and supp_html_child.get('class')[0] == 'chapter':
                # print(supp_html_child)
                supp_chapter = {}
                supp_chapter['id'] = chapter_id
                supp_chapter['num'] = supp_html_child.find(class_='echapno').string
                supp_chapter['title_en'] = supp_html_child.find(class_='englishchapter').string
                supp_chapter['title_ar'] = supp_html_child.find(class_='arabicchapter arabic').string
                supp_chapter['supps'] = []
                supp_chapters.append(supp_chapter)
                chapter_id += 1

                chapter_witout_supp = copy(supp_chapter)
                del chapter_witout_supp['supps']
                chapters_list.append(chapter_witout_supp)
            elif supp_chapter and supp_html_child.get('class') and supp_html_child.get('class')[
                0] == 'actualHadithContainer':
                # print(supp_html_child)
                supp = {}
                supp['id'] = supp_id
                if supp_html_child.find(class_='arabic_text_details arabic'):
                    supp['text_ar'] = supp_html_child.find(class_='arabic_text_details arabic').string
                elif supp_html_child.find(class_='arabic_hadith_full arabic'):
                    supp['text_ar'] = supp_html_child.find(class_='arabic_hadith_full arabic').string
                else:
                    supp['text_ar'] = None
                if supp_html_child.find(class_='transliteration'):
                    supp['text_translit'] = supp_html_child.find(class_='transliteration').string
                else:
                    supp['text_translit'] = None
                supp['text_en'] = supp_html_child.find(class_='translation').string
                supp['chapter_id'] = chapter_id - 1
                supp['favorite'] = 0
                supp_id += 1
                supp_chapter['supps'].append(supp)

                supps_list.append(supp)

# print(supp_chapters[0])


    for supp in supps_list:
        if supp['text_ar'] == None or supp['text_translit'] == None or supp['text_en'] == None:
            supps_with_issue.append(supp)
        if supp['text_ar']:
            supp['text_ar'] = supp['text_ar'].replace('\n', ' ')
        if supp['text_translit']:
            supp['text_translit'] = supp['text_translit'].replace('\n', ' ')
        if supp['text_en']:
            supp['text_en'] = supp['text_en'].replace('\n', ' ')

    hm_html_json_fp = Path('hisn-muslim.json')
    hm_chapters_json_fp = Path('hisn-muslim-chapters.json')
    hm_supps_json_fp = Path('hisn-muslim-supps1.json')
    hm_supps_with_issues = Path('hisn-muslim-supps-with-issue.json')

# print(json.dumps(supp_chapters))
    hm_html_json_fp.write_text(json.dumps(supp_chapters, ensure_ascii=False, indent=2))
    hm_chapters_json_fp.write_text(json.dumps(chapters_list, ensure_ascii=False, indent=2))
    hm_supps_json_fp.write_text(json.dumps(supps_list, ensure_ascii=False, indent=2))
    hm_supps_with_issues.write_text(json.dumps(supps_with_issue, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()