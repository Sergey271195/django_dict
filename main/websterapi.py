import requests
import json
from bs4 import BeautifulSoup
import re

class GetWordDefinition():
    def __init__(self, word):
        self.word = word
        self.dict_api_key = 'c5f232a9-0296-4e84-92e5-07884638a8dd'
        self.thes_api_key = '94a6db4c-286f-49c5-ac06-9535edf62d68'
        self.url = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{self.word}'
        self.result = {}
        self.general_info = {}

    def linksearch(self, index, index_2, index_3, definition, sdsense = False, example = False):
        link_tags = [r'\{a_link\|(?P<link>(\w+\s?)*)\|?.*?\}', r'\{d_link\|(?P<link>(\w+\s?)*)\|?.*?\}', r'\{dxt\|(?P<link>(\w+\s?)*)\|?.*?\}',
        r'\{et_link\|(?P<link>(\w+\s?)*)\|?.*?\}', r'\{i_link\|(?P<link>(\w+\s?)*)\|?.*?\}',
        r'\{mat\|(?P<link>(\w+\s?)*)\|?.*?\}', r'\{sx\|(?P<link>(\w+\s?)*)\|?.*?\}']
        new_string = definition
        if index != 'etymology':
            index = str(int(index)+1)
            index_2 = str(int(index_2)+1)+')'
            if index not in self.result:
                self.result[index] = {}
            if index_2 not in self.result[index]:
                self.result[index][index_2] = {}
        
        all_links = []
        for link in link_tags:
            l = re.findall(link, definition)
            l = [x[0] for x in l]
            all_links = all_links + l
            new_string = re.sub(link, '['+r'\g<link>'+']', new_string)
        if index == 'etymology':
            self.general_info[index]['links'] = all_links
            self.general_info[index]['text'] = new_string
        elif index_3 != 0:
            self.result[index][index_2][index_3] = {}
            if sdsense and example:
                self.result[index][index_2][index_3]['sd_example'] = new_string
            elif example:
                self.result[index][index_2][index_3]['example'] = new_string
            elif sdsense:
                self.result[index][index_2][index_3]['sdlinks'] = all_links
                self.result[index][index_2][index_3]['sdsense'] = new_string
            else:
                self.result[index][index_2][index_3]['links'] = all_links
                self.result[index][index_2][index_3]['sense'] = new_string
        else:
            if sdsense and example:
                self.result[index][index_2]['sd_example'] = new_string
            elif example:
                self.result[index][index_2]['example'] = new_string
            elif sdsense:
                self.result[index][index_2]['sdlinks'] = all_links
                self.result[index][index_2]['sdsense'] = new_string
            else:
                self.result[index][index_2]['links'] = all_links
                self.result[index][index_2]['sense'] = new_string

    def scrap(self, index, data):
        for index_2, entry in enumerate(data):
            if 'bs' in entry:
                def_text = entry[1]['sense']['dt'][0][1]
                self.linksearch(str(index), str(index_2), 0, def_text)
            elif 'pseq' in entry:
                for index_3, ent in enumerate(entry[1]):
                    def_text = ent[1]['dt'][0][1]
                    self.linksearch(str(index), str(index_2), str(index_3+1), def_text)
                    try:
                        example = ent[1]['dt'][1][1][0]['t']
                        self.linksearch(str(index), str(index_2), str(index_3+1), example, sdsense=False, example = True)
                    except Exception as e:
                        pass

            elif 'dt' in entry[1]:
                # Check for uns
                if 'uns' in entry[1]['dt'][0]:
                    def_text = entry[1]['dt'][0][1][0][0][1]
                    try:
                        example = entry[1]['dt'][0][1][0][1][1][0]['t']
                        self.linksearch(str(index), str(index_2), 0, example, sdsense=False, example = True)
                    except Exception as e:
                        pass
                        #print('No example', e)
                else:
                    def_text = entry[1]['dt'][0][1]
                    try:
                        example = entry[1]['dt'][1][1][0]['t']
                        self.linksearch(str(index), str(index_2), 0, example, sdsense=False, example = True)
                    except Exception as e:
                        pass
                        #print('No example', e)
                self.linksearch(str(index), str(index_2), 0, def_text)
                
                try:
                    div_sense = entry[1]['sdsense']['dt'][0][1]
                    self.linksearch(str(index), str(index_2), 0, div_sense, sdsense = True, example = False)
                        
                except Exception as e:
                    pass
                    #print('No divideed sense')
                try:
                    div_example = entry[1]['dt'][1][1][0]['t']
                    self.linksearch(str(index), str(index_2), 0, div_example, sdsense = True, example = True)
                except Exception as e:
                    pass

    def get_definition(self):
        
        params = {'key': self.dict_api_key}
        r = requests.get(self.url, params = params)

        response = r.json()
        data = response[0]
        if 'meta' not in data:
            print('Maybe you were looking for', response)
            return {'Error_links': response}
        else:
            meta = data['meta']
            if 'et' in data:
                etymology = data['et'][0][1]
                self.general_info['etymology'] = {}
                self.linksearch('etymology', 0, 0, etymology)
            if 'uros' in data:
                self.general_info['ure'] = data['uros'][0]['ure']
                if 'prs' in data['uros'][0]:
                    self.general_info['transcription'] = data['uros'][0]['prs'][0]['mw']
                
            definition = data['def']
            all_sences = definition[0]['sseq']
            #print(json.dumps(data, indent=2, sort_keys=True))
            for index, sence in enumerate(all_sences):
                self.scrap(index, sence)
            return(self.result, self.general_info)


word = GetWordDefinition('for').get_definition()


