# -*- coding:utf-8 -*-

from pyquery import PyQuery
import json
import re

with open('/home/wjl/test.txt','r') as f:
    _str = f.read()
p = PyQuery(_str)
if p('div.review-words.Hide'):
    print(p('div.review-words.Hide').text())
elif p('div.review-words'):
    print(p('div.review-words').text())
elif p('div.review-truncated-words'):
    print(p('div.review-truncated-words').text())