# -*- coding:utf-8 -*-

import re,json
from pyquery import PyQuery
from urllib.parse import urlparse
import xmltodict
with open('/home/wjl/test.txt', 'r') as f:
    _str = f.read()
p = PyQuery(_str)
info_dict = {}
for i in p('div.content-wrapper').items():
    label = i('div.label').text().strip()
    content = {}
    if '预订须知' in label:
        for j in i('dl').items('dd'):
            strong = j('strong').text()
            data = j('div').text().split('\n')
            content.setdefault(strong, data)
    elif '景点简介' in label:
        content = {'特色':i('ul.introduce-feature').text().split('\n'),'介绍':i('div.introduce-content').text()}
    elif '交通指南' in label:
        content = i('div.traffic-content').text().split('\n')
    else:
        continue
    info_dict.setdefault(label, content)
print(json.dumps(info_dict, ensure_ascii=False))




