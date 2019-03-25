# -*- coding:utf-8 -*-

from spider.driver.travel.core.traveldriver import TravelDriver
from spider.driver.base.page import Page,NextPageCssSelectorSetup,PageFunc
from spider.driver.base.field import Fieldlist,Field,FieldName
from spider.driver.base.tabsetup import TabSetup
from spider.driver.base.listcssselector import ListCssSelector
from spider.driver.base.mongodb import Mongodb
import re
import time
import json
from pyquery import PyQuery
import xmltodict
import math
import datetime
fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME,css_selector='div.spot-info > h4 > em'),
    Field(fieldname=FieldName.SHOP_RATE, css_selector='div.search_ticket_title > h2 > span > span.rate'),
    Field(fieldname=FieldName.SHOP_URL,css_selector='div.search_ticket_title > h2 > a',attr='href'),
    Field(fieldname=FieldName.SHOP_IMG, css_selector='a > img', attr='src'),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='div.search_ticket_title > div.adress'),
    Field(fieldname=FieldName.SHOP_GRADE,css_selector='div.search_ticket_assess > span.grades > em'),
    Field(fieldname=FieldName.SHOP_COMMENT_NUM,css_selector='div.search_ticket_assess > span.grades', regex=r'^[^\(]*\(([\d]+)[^\)\d]*\)$', repl=r'\1'),
    Field(fieldname=FieldName.SHOP_FEATURE, css_selector='div.search_ticket_title > div.exercise'),
)

def get_shop_service(self, _str):
    p = PyQuery(_str)
    service_list = []
    for i in p('span').items():
        service_list.append(i.text().strip())
    return json.dumps(service_list, ensure_ascii=False)

def get_shop_ticket(self, _str):
    p = PyQuery(_str)
    # 门票
    p_ticket = p('#J-Ticket')
    # 一级标题
    for i in p_ticket('div.ticket-detail-title').items():
        if not i.attr('style'):  # 一级标题没有style
            i.replace_with("<ticket class='head-level-1'>%s</ticket>" % i.text())
    # 二级标题
    for i in p_ticket('div.ticket-detail-title').items():
        if i.attr('style'):  # 一级标题有style
            i.replace_with("<ticket class='head-level-2'>%s</ticket>" % i.text())
    # 三级标题
    for i in p_ticket('table.ttd-hairline-top').items():
        if 'ticket-table' not in i.attr('class'):
            info_list = i.text().split('\n')[:-1]
            info_dict = {'名称': info_list[0], '参考门市价': info_list[1], '价格': info_list[2]}
            i.replace_with("<ticket class='head-level-3'>%s</ticket>" % json.dumps(info_dict, ensure_ascii=False))
    # 正文
    for i in p_ticket('table.ticket-table').items():
        thead_list = []
        for j in i('thead').items('td'):
            thead_list.append(j.text())
        tbody_dict_list = []
        for j in i('tbody').items():
            tbody_dict = {}
            for k in range(1, len(thead_list) + 1):
                tbody_dict.setdefault(thead_list[k - 1], j('td:nth-child(%s)' % k).text())
            tbody_dict_list.append(tbody_dict)
        i.replace_with("<ticket class='content'>%s</ticket>" % json.dumps(tbody_dict_list, ensure_ascii=False))
    from lxml import etree
    root = etree.Element('ticket')
    pointer = root
    h1 = None
    h2 = None
    h3 = None
    for i in p_ticket('ticket').items():
        if i.attr('class') == 'head-level-1':
            pointer = root
            pointer = etree.SubElement(pointer, 'title')
            pointer.attrib['name'] = '%s' % i.text()
            h1 = pointer
        if i.attr('class') == 'head-level-2':
            pointer = h1
            pointer = etree.SubElement(pointer, 'title')
            pointer.attrib['name'] = '%s' % i.text()
            h2 = pointer
        if i.attr('class') == 'head-level-3':
            pointer = h2
            pointer = etree.SubElement(pointer, 'title')
            pointer.attrib['name'] = '%s' % i.text()
            h3 = pointer
        if i.attr('class') == 'content':
            pointer = etree.SubElement(pointer, 'content')
            pointer.text = "%s" % i.text()
            pointer = h3
    tickets = str(etree.tostring(root, pretty_print=True, encoding='utf-8'), 'utf-8')
    tickets = json.loads(json.dumps(xmltodict.parse(tickets), ensure_ascii=False))
    # 玩乐
    p_activity = p('#J-Activity')
    thead_list = []
    for i in p_activity('thead').items('td'):
        thead_list.append(i.text())
    tbody_list = []
    for i in p_activity('tbody').items('tr'):
        tbody = {}
        for j in range(1, len(thead_list)):
            tbody.setdefault(thead_list[j - 1], i('td:nth-child(%s)' % j).text().strip())
        tbody_list.append(tbody)
    activitys = tbody_list
    # 门票+酒店
    p_drainage = p('#J-Drainage')
    thead_list = []
    for i in p_drainage('thead').items('td'):
        thead_list.append(i.text())
    tbody_list = []
    for i in p_drainage('tbody').items('tr'):
        tbody = {}
        for j in range(1, len(thead_list)):
            tbody.setdefault(thead_list[j - 1], i('td:nth-child(%s)' % j).text().strip())
        tbody_list.append(tbody)
    drainages = tbody_list
    results = {'门票': tickets, '玩乐': activitys, '门票+酒店': drainages}
    return json.dumps(results, ensure_ascii=False)

def get_shop_info(self, _str):
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
            content = {'特色': i('ul.introduce-feature').text().split('\n'), '介绍': i('div.introduce-content').text()}
        elif '交通指南' in label:
            content = i('div.traffic-content').text().split('\n')
        else:
            continue
        info_dict.setdefault(label, content)
    return json.dumps(info_dict, ensure_ascii=False)

fl_shop2 = Fieldlist(
    # Field(fieldname=FieldName.SHOP_PRICE, css_selector='#root > div > div > div > div > div:nth-child(3) > div.main-bd > div > div.brief-box.clearfix > div.spot-price > div > span', pause_time=3, is_focus=True, is_info=True),
    # Field(fieldname=FieldName.SHOP_TIME, css_selector='#root > div > div > div > div > div:nth-child(3) > div.main-bd > div > div.brief-box.clearfix > div.brief-right > ul > li.time > span', is_focus=True),
    # Field(fieldname=FieldName.SHOP_SERVICE,css_selector='#root > div > div > div > div > div:nth-child(3) > div.main-bd > div > div.brief-box.clearfix > div.brief-right > ul > li.promise',attr='innerHTML', filter_func=get_shop_service, is_focus=True),
    # Field(fieldname=FieldName.SHOP_TICKET, css_selector='#booking-wrapper',attr='innerHTML', filter_func=get_shop_ticket, is_focus=True),
    # Field(fieldname=FieldName.SHOP_INFO, css_selector='div.main-bd > div.main-wrapper > div.clearfix > div.detail-left', attr='innerHTML', filter_func=get_shop_info, is_focus=True),
)

page_shop_1 = Page(name='携程景点店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='div > div.search-list-wrap > div > div.clearfix > div.spot-list > div', item_css_selector='div'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection),is_save=False)

page_shop_2 = Page(name='携程景点店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector=''), mongodb=Mongodb(db=TravelDriver.db,collection=TravelDriver.shop_collection))

def get_comment_user_name(self, _str):
    return _str.split(' ')[0]

def get_comment_time(self, _str):
    time =  re.findall(r'([\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2})',_str)[0]
    return time[0:10]

def get_comment_year(self,_str):
    time = re.findall(r'([\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2})', _str)[0]
    return time[0:4];

def get_comment_season(self, _str):
    time = re.findall(r'([\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2})', _str)[0]
    times = time.split('-');

    month = int(times[1])

    seasons = ['01', '02', '03', '04'];
    if (month % 3 == 0):
        return (times[0] + '-' + seasons[int(month / 3) - 1]);
    else:
        index = int(math.floor(month / 3));
        return (times[0] + '-' + seasons[index]);
def get_comment_month(self, _str):
    time = re.findall(r'([\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2})', _str)[0]
    return time[0:7];
def get_comment_week(self, _str):
    temp = re.findall(r'([\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2})', _str)[0]
    time = temp[0:10]
    times = time.split('-');
    return (times[0] + '-' + str(datetime.date(int(times[0]), int(times[1]), int(times[2])).isocalendar()[1]).zfill(2))

def get_data_region_search_key(self, _str):

    return  self.data_region_search_key
def get_shop_name_search_key(self,_str):

    return self.shop_name_search_key(_str);

fl_comment1 = Fieldlist(
    Field(fieldname=FieldName.COMMENT_USER_NAME, css_selector='div.user-date', filter_func=get_comment_user_name,is_info=True),
    Field(fieldname=FieldName.COMMENT_TIME, css_selector='div.user-date', filter_func=get_comment_time,is_info=True),
    Field(fieldname=FieldName.SHOP_NAME, css_selector='div.main-bd > div > div.brief-box.clearfix > div.brief-right > h2', is_isolated=True),
Field(fieldname=FieldName.SHOP_NAME_SEARCH_KEY,css_selector='div.main-bd > div > div.brief-box.clearfix > div.brief-right > h2',is_isolated=True,filter_func=get_shop_name_search_key, is_info=True),
    Field(fieldname=FieldName.COMMENT_CONTENT, css_selector='p',is_info=False),
    Field(fieldname=FieldName.COMMENT_SCORE, css_selector='h4', regex=r'[^\d.]*',is_info=False),
    Field(fieldname=FieldName.COMMENT_YEAR,css_selector='div.user-date',filter_func=get_comment_year,is_info=False),
    Field(fieldname=FieldName.COMMENT_SEASON,css_selector='div.user-date',filter_func=get_comment_season,is_info=False),
    Field(fieldname=FieldName.COMMENT_MONTH,css_selector='div.user-date',filter_func=get_comment_month,is_info=False),
    Field(fieldname=FieldName.COMMENT_WEEK,css_selector='div.user-date',filter_func=get_comment_week,is_info=False),
    Field(fieldname=FieldName.DATA_REGION_SEARCH_KEY,css_selector='',filter_func=get_data_region_search_key,is_info=True),

)

page_comment_1 = Page(name='携程景点评论列表', fieldlist=fl_comment1, listcssselector=ListCssSelector(list_css_selector='div.main-bd > div > div > div.detail-left > div.content-wrapper.clearfix > ul.comments > li'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)

class XiechengSpotSpider(TravelDriver):

    def shop_detail_page_unfold(self):
        try:
            for i in self.until_presence_of_all_elements_located_by_partial_link_text(link_text='展开', timeout=1):
                self.scroll_to_center(ele=i)
                i.click()
        except Exception:
            pass

    def get_shop_info(self):
        try:
            shop_data_list = self.from_page_get_data_list(page=page_shop_1)
            # root > div > div > div > div > div:nth-child(3) > div.main-bd > div > div:nth-child(5) > div.detail-left > div.content-wrapper.clearfix > ul.pkg_page > a.down
            # root > div > div > div > div > div:nth-child(3) > div.main-bd > div > div:nth-child(5) > div.detail-left > div.content-wrapper.clearfix > ul.pkg_page > a.down.disabled.nocurrent
            nextpagesetup = NextPageCssSelectorSetup(css_selector='div.detail-left > div.content-wrapper.clearfix > ul.pkg_page > a.down', stop_css_selector='div.detail-left > div.content-wrapper.clearfix > ul.pkg_page > a.down.disabled.nocurrent', page=page_comment_1, pause_time=2)
            extra_pagefunc = PageFunc(func=self.get_newest_comment_data_by_css_selector, nextpagesetup=nextpagesetup)
            self.from_page_add_data_to_data_list(page=page_shop_2, pre_page=page_shop_1, data_list=shop_data_list,extra_pagefunc=extra_pagefunc)
        except Exception as e:
            self.error_log(e=str(e))

    def get_shop_info_list(self):
        self.driver.get('https://www.baidu.com')
        self.fast_new_page(url='http://piao.ctrip.com/', is_scroll_to_bottom=False)
        self.driver.refresh()
        self.until_scroll_to_center_send_text_by_css_selector(css_selector="#mainInput", text=self.data_region)
        time.sleep(3)
        self.until_scroll_to_center_send_enter_by_css_selector(css_selector="#mainInput")
        self.until_click_no_next_page_by_css_selector(nextpagesetup=NextPageCssSelectorSetup(css_selector='#searchResultContainer > div.pkg_page.basefix > a.down', stop_css_selector='#searchResultContainer > div.pkg_page.basefix > a.down.down_nocurrent', pre_pagefunc=PageFunc(func=self.driver.refresh), main_pagefunc=PageFunc(func=self.get_shop_info)))
    def get_shop_comemnt(self):
       self.fast_new_page(url="http://www.baidu.com");
       shop_collcetion = Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection,
                                 host='localhost').get_collection()
       shop_name_url_list = list()
       for i in shop_collcetion.find(self.get_data_key()):
           if i.get('shop_url'):
               shop_name_url_list.append((i.get('shop_name'), i.get('shop_url')))
       for i in range(len(shop_name_url_list)):
           self.info_log(data='第%s个,%s' % (i + 1, shop_name_url_list[i][0]))
           # while (True):
           #     self.is_ready_by_proxy_ip()
           #     self.switch_window_by_index(index=-1)
           #     self.deal_with_failure_page()
           #     self.fast_new_page(url=shop_name_url_list[i][1])
           #     time.sleep(1)
           #     self.switch_window_by_index(index=-1)  # 页面选择
           #     if '请求数据错误' in self.driver.title:
           #         self.info_log(data='关闭验证页面!!!')
           #         self.close_curr_page()
           #     else:
           #         break
           self.fast_new_page("http://piao.ctrip.com")
           self.fast_new_page(url=shop_name_url_list[i][1])
           self.until_click_no_next_page_by_css_selector(nextpagesetup=NextPageCssSelectorSetup(
               css_selector='#root > div > div > div > div > div:nth-child(3) > div.main-bd > div > div:nth-child(5) > div.detail-left > div.content-wrapper.clearfix > ul.pkg_page > a.down',
               stop_css_selector='#root > div > div > div > div > div:nth-child(3) > div.main-bd > div > div:nth-child(5) > div.detail-left > div.content-wrapper.clearfix > ul.pkg_page > a.down.hidden',
               main_pagefunc=PageFunc(
                   func=self.from_page_get_data_list,
                   page=page_comment_1), pause_time=5))
           self.close_curr_page();
    def run_spider(self):
        try:
            self.data_region_search_key = self.get_data_region_search_key()
            #self.get_shop_info_list()
            self.get_shop_comemnt()
        except Exception as e:
            self.error_log(e=str(e))