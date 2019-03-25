# -*- coding:utf-8 -*-

from spider.driver.base.field import Fieldlist,Field,FieldName
from spider.driver.base.tabsetup import TabSetup
from spider.driver.base.page import Page,NextPageCssSelectorSetup,PageFunc,NextPageLinkTextSetup
from spider.driver.base.listcssselector import ListCssSelector
from spider.driver.base.mongodb import Mongodb
from spider.driver.travel.core.traveldriver import TravelDriver
import time
from pyquery import PyQuery
import json
import re
import random

def get_shop_tag(self, _str):
    try:
        p = PyQuery(_str)
    except Exception:
        return None
    return json.dumps([i.text() for i in p('span').items()][1:], ensure_ascii=False)

def get_shop_rate(self, _str):
    return str(float((int(_str)/10)))

def get_shop_subtype_name(self, _str):
    return _str.strip()

fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='div.txt > div.tit > a > h4'),
    Field(fieldname=FieldName.SHOP_URL, css_selector='div.txt > div.tit > a', attr='href'),
    Field(fieldname=FieldName.SHOP_COMMENT_NUM, css_selector='div.txt > div.comment > a.review-num'),
    Field(fieldname=FieldName.SHOP_PRICE, css_selector='div.txt > div.comment > a.mean-price'),
    Field(fieldname=FieldName.SHOP_RATE, css_selector='div.txt > div.comment > span', attr='class', regex=r'[^\d]*', filter_func=get_shop_rate),
    Field(fieldname=FieldName.SHOP_TAG, css_selector='div.txt > span.comment-list', attr='innerHTML', filter_func=get_shop_tag, pause_time=1),
    Field(fieldname=FieldName.SUBTYPE_NAME, css_selector='div.txt > div.tag-addr > a:nth-child(1)', filter_func=get_shop_subtype_name),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='div.txt > div.tag-addr > span.addr')
)

page_shop_1 = Page(name='大众点评爱车店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#shop-all-list > ul > li'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection), is_save=True)

def get_shop_time(self, _str):
    try:
        p = PyQuery(_str)
        shop_time = ''
        for i in p('p.info.info-indent').items():
            if '营业时间' in i.text():
                shop_time = i.text()
        return shop_time
    except Exception:
        return ''

def get_shop_promotion(self, _str):
    try:
        p = PyQuery(_str)
    except Exception:
        return None
    promotion = {}
    for i in p('div.group > div.item').items():
        info_list = i.text().split('\n')
        promotion.setdefault(info_list[0],info_list[1:])
    for i in p('div.group > a').items():
        info_list = i.text().split('\n')
        promotion.setdefault(info_list[-1],info_list[:-1])
    return json.dumps(promotion, ensure_ascii=False)

def get_shop_menu(self, _str):
    try:
        p = PyQuery(_str)
    except Exception:
        return None
    menu = {}
    tab_name_list = p('#shop-tabs > h2.mod-title > a').text().split(' ')
    count = 0
    for i in p('#shop-tabs > div').items():
        tab_content_list = []
        if 'shop-tab-recommend' in i.attr('class'):
            dish_recommend = {}
            for j in i('p.recommend-name > a.item').items():
                dish_recommend.setdefault(re.sub(r'([^(]+)\([^)]+\)', r'\1', j.text()).strip(), {'推荐数': re.sub(r'[^(]+\(([^)]+)\)', r'\1', j.text()).strip()})
            for j in i('ul.recommend-photo > li.item').items():
                try:
                    item = dish_recommend.get(j('p.name').text().strip())
                    item.setdefault('价格', j('span.price').text())
                    item.setdefault('图片', j('img').attr('src'))
                except Exception:
                    print('%s不存在'%j('p.name').text().strip())
            menu.setdefault(tab_name_list[count], dish_recommend)
        else:
            for j in p('div.container > a.item').items():
                tab_content_list.append({'标题': j.attr('title'), '链接': j.attr('href'), '图片': j('img').attr('data-src')})
            menu.setdefault(tab_name_list[count], tab_content_list)
        count += 1
    return json.dumps(menu, ensure_ascii=False)

def get_shop_statistics(self, _str):
    try:
        p = PyQuery(_str)
    except Exception:
        return None
    statistics_dict = dict()
    everyone = dict()
    for i in p('div.comment-condition.J-comment-condition.Fix > div.content > span.good.J-summary').items():
        everyone.setdefault(re.sub(r'[\d()]*', '', i.text()), int(re.sub(r'[^\d]*', '', i.text())))
    statistics_dict.setdefault('大家认为', everyone)
    evaluation = dict()
    for i in p('div.comment-filter-box.clearfix.J-filter > label.filter-item').items():
        if '全部' not in i.text():
            evaluation.setdefault(re.sub(r'[\d()]*', '', i.text()), int(re.sub(r'[^\d]*', '', i.text())))
    statistics_dict.setdefault('评价', evaluation)
    return json.dumps(statistics_dict, ensure_ascii=False)

fl_shop2 = Fieldlist(
    Field(fieldname=FieldName.SHOP_PHONE, css_selector='#basic-info > p', is_focus=True, is_info=True),
    Field(fieldname=FieldName.SHOP_TIME, css_selector='#basic-info > div.other.J-other.Hide', filter_func=get_shop_time,attr='innerHTML', is_focus=True, is_info=True),
    Field(fieldname=FieldName.SHOP_PROMOTION, css_selector='#promoinfo-wrapper', attr='innerHTML', filter_func=get_shop_promotion, is_focus=True),
    Field(fieldname=FieldName.SHOP_MENU, css_selector='#shoptabs-wrapper', attr='innerHTML', filter_func=get_shop_menu, is_focus=True),
    Field(fieldname=FieldName.SHOP_STATISTICS, css_selector='#summaryfilter-wrapper', attr='innerHTML', filter_func=get_shop_statistics, is_focus=True),
    Field(fieldname=FieldName.SHOP_COMMENT_URL, css_selector='#morelink-wrapper > p > a', attr='href', is_focus=True, is_info=True),
)

page_shop_2 = Page(name='大众点评爱车店铺详情页面', fieldlist=fl_shop2)

def get_rate(self, _str):
    try:
        return str(int(re.sub('[^\d]*','',_str))/10)
    except Exception:
        return 0

def get_comment_rate_tag(self, _str):
    p = PyQuery(_str)
    tag_list = []
    for i in p('span.item').items():
        tag_list.append(i.text().strip())
    return json.dumps(tag_list, ensure_ascii=False)

def get_comment_content(self, _str):
    p = PyQuery(_str)
    if p('div.review-words.Hide'):
        return p('div.review-words.Hide').text()
    else:
        return p('div.review-words').text()

fl_comment1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='#review-list > div.review-list-container > div.review-list-main > div.review-list-header > h1 > a', is_isolated=True),
Field(fieldname=FieldName.SHOP_URL, css_selector='#review-list > div.review-list-container > div.review-list-main > div.review-list-header > h1 > a', attr='href', is_isolated=True),
    Field(fieldname=FieldName.COMMENT_USER_NAME, css_selector='div.main-review > div.dper-info'),
    Field(fieldname=FieldName.COMMENT_TIME, css_selector='div.main-review > div.misc-info.clearfix > span.time'),
    Field(fieldname=FieldName.COMMENT_USER_RATE, css_selector='div > div.dper-info > span', attr='class', filter_func=get_rate, is_info=True),
    Field(fieldname=FieldName.COMMENT_RATE, css_selector='div.main-review > div.review-rank > span', attr='class', filter_func=get_rate, is_info=True),
    Field(fieldname=FieldName.COMMENT_RATE_TAG, css_selector='div.main-review > div.review-rank > span.score', attr='innerHTML', filter_func=get_comment_rate_tag),
    Field(fieldname=FieldName.COMMENT_CONTENT, css_selector='div.main-review', attr='innerHTML', filter_func=get_comment_content),
    Field(fieldname=FieldName.COMMENT_PIC_LIST, list_css_selector='div.main-review > div.review-pictures > ul', item_css_selector='li > a > img', attr='src', timeout=0),
)

page_comment_1 = Page(name='大众点评爱车评论列表', fieldlist=fl_comment1, listcssselector=ListCssSelector(list_css_selector='#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.reviews-items > ul > li'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)

class DianpingCarSpider(TravelDriver):

    def more_comment(self):
        while(True):
            self.is_ready_by_proxy_ip()
            self.switch_window_by_index(index=-1)
            self.deal_with_failure_page()
            self.until_scroll_to_center_click_by_css_selector(css_selector='#comment > div > div.comment > div.more-comment > a.dp-link')
            time.sleep(2)
            self.switch_window_by_index(index=-1)  # 页面选择
            if '验证中心' in self.driver.title:
                self.info_log(data='关闭验证页面!!!')
                self.close_curr_page()
            else:
                break
        # time.sleep(1)
        # while(True):
        #     self.until_scroll_to_center_click_by_css_selector(css_selector='#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.reviews-filter.clearfix > div.sort > a')
        #     time.sleep(1)
        #     self.is_ready_by_proxy_ip()
        #     self.until_scroll_to_center_click_by_css_selector(css_selector='#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.reviews-filter.clearfix > div.sort-selection-list > a')
        #     time.sleep(1)
        #     self.switch_window_by_index(index=-1)
        #     if '验证' in self.driver.title:#如果是验证页面
        #         self.driver.back()
        #     else:
        #         break

    def get_shop_comment(self):
        shop_collcetion = Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection,
                                  host='10.1.17.15').get_collection()
        shop_name_url_list = list()
        for i in shop_collcetion.find(self.get_data_key()):
            if i.get('shop_comment_url'):
                shop_name_url_list.append((i.get('shop_name'),i.get('shop_comment_url')))
        for i in range(len(shop_name_url_list)):
            self.info_log(data='第%s个,%s'%(i+1, shop_name_url_list[i][0]))
            while (True):
                self.is_ready_by_proxy_ip()
                self.switch_window_by_index(index=-1)
                self.deal_with_failure_page()
                self.fast_new_page(url=shop_name_url_list[i][1])
                time.sleep(1)
                self.switch_window_by_index(index=-1)  # 页面选择
                if '验证中心' in self.driver.title:
                    self.info_log(data='关闭验证页面!!!')
                    self.close_curr_page()
                else:
                    break
            self.until_click_no_next_page_by_partial_link_text(nextpagesetup=NextPageLinkTextSetup(link_text='下一页', main_pagefunc=PageFunc(func=self.from_page_get_data_list, page=page_comment_1)))
            self.close_curr_page()

    def get_shop_detail(self):
        shop_collcetion = Mongodb(db=TravelDriver.db,collection=TravelDriver.shop_collection, host='10.1.17.15').get_collection()
        shop_url_set = set()
        for i in shop_collcetion.find(self.get_data_key()):
            shop_url_set.add(i.get(FieldName.SHOP_URL))
        count = 0
        for url in shop_url_set:
            print(count)
            count += 1
            while (True):
                self.is_ready_by_proxy_ip()
                self.switch_window_by_index(index=-1)
                self.deal_with_failure_page()
                self.fast_new_page(url=url)
                time.sleep(1)
                self.switch_window_by_index(index=-1)  # 页面选择
                if '验证中心' in self.driver.title:
                    self.info_log(data='关闭验证页面!!!')
                    self.close_curr_page()
                else:
                    break
            data = self.from_fieldlist_get_data(page=page_shop_2)
            self.update_data_to_mongodb(shop_collcetion,self.merge_dict(self.get_data_key(),{FieldName.SHOP_URL:url}), data)
            self.close_curr_page()

    def get_shop_info_list(self):
        self.fast_click_first_item_page_by_partial_link_text(link_text='爱车')
        time.sleep(2)
        while (True):
            self.is_ready_by_proxy_ip()
            self.switch_window_by_index(index=-1)
            self.deal_with_failure_page()
            self.until_scroll_to_center_click_by_css_selector(css_selector='#J_qs-btn')
            time.sleep(1)
            self.switch_window_by_index(index=-1)  # 页面选择
            if '验证中心' in self.driver.title:
                self.info_log(data='关闭验证页面!!!')
                self.close_curr_page()
            else:
                break
        time.sleep(2)
        self.until_click_no_next_page_by_partial_link_text(NextPageLinkTextSetup(link_text='下一页',is_proxy=False, main_pagefunc=PageFunc(self.from_page_get_data_list, page=page_shop_1)))

    def login(self):
        self.fast_get_page(url='https://www.baidu.com')
        time.sleep(2)
        self.until_scroll_to_center_send_text_by_css_selector(css_selector='#kw', text=self.data_region + self.data_website)
        self.until_scroll_to_center_send_enter_by_css_selector(css_selector='#kw')
        self.fast_click_first_item_page_by_partial_link_text(link_text=self.data_website)
        with open('./cookies/dianping_cookies.json', 'r', encoding='utf-8') as f:
            listCookies = json.loads(f.read())
        for cookie in listCookies:
            self.driver.add_cookie(cookie)
        self.close_curr_page()
        self.fast_click_first_item_page_by_partial_link_text(link_text=self.data_website)

    def run_spider(self):
        try:
            self.login()
            # self.get_shop_info_list()
            # self.get_shop_detail()
            self.get_shop_comment()
        except Exception:
            self.error_log(e='cookies失效!!!')