#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
# #reload(sys)
# sys.setdefaultencoding('utf8')
from selenium import webdriver
import codecs
import time
import re
from pyquery import PyQuery
# time.sleep(20)
def get_target_text(_html_content, _css_content, _svg_content):
    # 构建词典
    height_text = {}
    p = PyQuery(_svg_content)
    # 格式1
    try:
        for item in p("path").items():
            max_height = int(item.attr("d").split()[1])
            text = p("textpath:nth-child(%s)" % item.attr("id")).text()
            height_text[max_height] = text
    except Exception:
        pass
    # 格式2
    try:
        for item in p("text").items():
            max_height = int(item.attr("y"))
            text = item.text()
            height_text[max_height] = text
    except Exception:
        pass

    def get_single_text(_class_name):
        """
        获得目标词
        """
        # 查找class对应的属性
        try:
            x, y = \
            re.findall("\.%s{background:[-]*([\d]+)[.]*[\d]+px [-]*([\d]+)[.]*[\d]+px;}" % _class_name, _css_content)[0]
            x = int(x)
            y = int(y)
        except Exception:
            return _class_name
        # 获得目标的文字的高度列表
        height_list = list(height_text.keys()) + [y]
        height_list.sort()
        # 获得目标文字
        target_text = list(height_text[height_list[height_list.index(y) + 1]])[x // 14]
        return target_text

    # 获得解密后的评论
    _html_content_list = PyQuery(re.sub(r"<[a-z]+ class=\"([a-zA-Z0-9]+)\"/>", r"|\1|", _html_content)).text().split("|")
    for i in range(len(_html_content_list)):
        _html_content_list[i] = get_single_text(_html_content_list[i])
    return re.sub("收起评论.*$", "", "".join(_html_content_list)).replace("\n", "").strip()
browser = webdriver.Chrome()

browser.get("http://www.dianping.com")
time.sleep(15)
browser.get("http://www.dianping.com/shop/98129883/review_all")
html = browser.find_element_by_css_selector('#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.reviews-items > ul > li:nth-child(2) > div.main-review').get_attribute('innerHTML')
p = PyQuery(html)

if p('div.review-words.Hide'):
    print(111)
    html = p('div.review-words.Hide').html().strip()
    print(html)
    print(get_target_text(html,
                          open('/Users/caokaiqiang/Documents/TouristSpider/style.css', 'r').read(),
                          codecs.open('/Users/caokaiqiang/Documents/TouristSpider/ie.svg', 'r',
                                      encoding='utf-8').read()));
else:
    print(222)
    html = p('div.review-words').html().strip()
    #表明没有字符
    print(get_target_text(html,
                          open('/Users/caokaiqiang/Documents/TouristSpider/style.css', 'r').read(),
                          codecs.open('/Users/caokaiqiang/Documents/TouristSpider/ie.svg', 'r',
                                      encoding='utf-8').read()));
