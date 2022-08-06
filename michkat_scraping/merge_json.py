import json
import codecs


def main():
    translit_list = []
    data = json.load(codecs.open('akram_adkar_fr.json', 'r', 'utf-8'))
    data1 = json.load(codecs.open('hisn-muslim-translit_en.json', 'r', 'utf-8'))
    data2 = json.load(codecs.open('hisn-muslim-translit_fr.json', 'r', 'utf-8'))

    for d in data:
        d['text_translit_en'] = data1[d['id']-1]
        d['text_translit_fr'] = data2[d['id']-1]


    with codecs.open('hisn-muslim-supps-final.json', 'w', 'utf-8') as outfile:
        outfile.write(json.dumps(data, ensure_ascii=False, indent=2))

# with open("hisn-muslim.json", "w") as jsonFile:
#     json.dump(data, jsonFile)

if __name__ == '__main__':
    main()
