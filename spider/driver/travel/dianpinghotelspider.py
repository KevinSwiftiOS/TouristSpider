# -*- coding:utf-8 -*-

from spider.driver.base.field import Fieldlist,Field,FieldName
from spider.driver.base.tabsetup import TabSetup
from spider.driver.base.page import Page,NextPageCssSelectorSetup,PageFunc
from spider.driver.base.listcssselector import ListCssSelector
from spider.driver.base.mongodb import Mongodb
from spider.driver.travel.core.traveldriver import TravelDriver
import time
from pyquery import PyQuery
import json
import re
import random

def get_shop_tag(self, _str):
    p = PyQuery(_str)
    tag_list = []
    for i in list(p('span').items())[1:]:
        tag_list.append(i.text())
    return json.dumps(tag_list, ensure_ascii=False)

def get_shop_rate(self, _str):
    return str(float((int(_str)/10)))

fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_PRICE, css_selector='div.hotel-info-ctn > div.hotel-remark > div.price > p > strong'),
    Field(fieldname=FieldName.SHOP_NAME, css_selector='div.hotel-info-ctn > div.hotel-info-main > h2 > a.hotel-name-link'),
    Field(fieldname=FieldName.SHOP_RATE, css_selector='div.hotel-info-ctn > div.hotel-remark > div.remark > div > div > span', attr='class', regex=r'[^\d]*', filter_func=get_shop_rate),
    # Field(fieldname=FieldName.SHOP_TAG, css_selector='div.hotel-info-ctn > div.hotel-info-main > p.hotel-tags', attr='innerHTML', filter_func=get_shop_tag, pause_time=3),
    Field(fieldname=FieldName.SHOP_URL,css_selector='',attr='href',is_info=True),
    Field(fieldname=FieldName.SHOP_IMG,css_selector='',attr='src',is_info=True),
    Field(fieldname=FieldName.SHOP_ADDRESS,css_selector='',is_info=True),
    Field(fieldname=FieldName.SHOP_GRADE,css_selector='',is_info=True),
    Field(fieldname=FieldName.SHOP_COMMENT_NUM,css_selector='',is_info=True),
    Field(fieldname=FieldName.SHOP_FEATURE,css_selector='',is_info=True)

)

def get_shop_room_all(self, _str):
    p = PyQuery(_str)
    sale_dict = {}
    room_list = []
    for i in p('div.hotel-rooms > div.hotel-rooms-list > div.hotel-rooms-list-cont > ul > li').items():
        room = {'room_name': i('div.title-info.clearfix.dph-col.dph-col1 > div.title > h3').text()}
        for j in i('div.h-item-more.h-hide').text().split('\n'):
            room.update((lambda x: {x[0].strip(): x[1].strip()} if len(x) == 2 else {})(j.split(':')))
        item_list = []
        for j in i('div.roomlist > div').items():
            item_list.append(j.text().split('\n'))
        room.setdefault('room_list', item_list)
        room_list.append(room)
    sale_dict.setdefault('房型预定', room_list)
    package_list = []
    for i in p('div > ul.group-deal > li').items():
        info_list = i.text().split('￥')
        if len(info_list) == 2:
            package_list.append({info_list[0].strip(): info_list[1].strip()})
    sale_dict.setdefault('套餐预定', package_list)
    return json.dumps(sale_dict, ensure_ascii=False)

def get_shop_intro(self, _str):
    p = PyQuery(_str)
    info_dict = {}
    for i in p('ul.list-info > li').items():
        info = i.text().split('\n')
        if len(info) == 2:
            items = list(i('div > span').items())
            item_list = []
            if len(items) >= 2:
                for j in items:
                    item_list.append(j.text())
                info[1] = item_list
            info_dict.setdefault(info[0], info[1])
    return json.dumps(info_dict, ensure_ascii=False)

def get_shop_statistics(self, _str):
    p = PyQuery(_str)
    tag_star_dict = {}
    tags = {}
    for i in p('div.tags > ul > li').items():
        tags.setdefault(re.sub('[^\u4e00-\u9fa5]*', '', i.text()), re.sub('[^\d]*', '', i.text()))
    tag_star_dict.setdefault('tags', tags)
    stars = {}
    for i in p('#comment > div > h2 > span > a').items():
        star = i.text().split('星')
        if len(star) == 2:
            stars.setdefault(star[0], re.sub(r'[^\d]*', '', star[1]))
    tag_star_dict.setdefault('star', stars)
    return json.dumps(tag_star_dict, ensure_ascii=False)

fl_shop2 = Fieldlist(
    Field(fieldname=FieldName.SHOP_GRADE, css_selector='#poi-detail > div.container > div.base-info > div.main-detail.clearfix > div.main-detail-right > div.hotel-appraise > div.hotel-scope > span', pause_time=5, is_focus=True),
    Field(fieldname=FieldName.SHOP_PHONE, css_selector='#poi-detail > div.container > div.base-info > div.main-detail.clearfix > div.main-detail-left > div.main-detail-left-top.clearfix > div.hotel-detail-info > div > div.call-info > div > span.call-number', is_focus=True),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='#poi-detail > div.container > div.base-info > div.main-detail.clearfix > div.main-detail-left > div.main-detail-left-top.clearfix > div.hotel-detail-price > div.hotel-address-box.clearfix > span.hotel-address', is_focus=True),
    Field(fieldname=FieldName.SHOP_ROOM_RECOMMEND_ALL, css_selector='#deal', attr='innerHTML', filter_func=get_shop_room_all, is_focus=True),
    Field(fieldname=FieldName.SHOP_INTRO, css_selector='#poi-detail > div.container > div.sub-content.clearfix > div.main > div> div.hotel-info', attr='innerHTML', filter_func=get_shop_intro, is_focus=True),
    Field(fieldname=FieldName.SHOP_STATISTICS, css_selector='#poi-detail > div.container > div.sub-content.clearfix > div.main > div.user-comment-info', attr='innerHTML', filter_func=get_shop_statistics, is_focus=True),
    Field(fieldname=FieldName.SHOP_COMMENT_NUM, css_selector='#comment > div > h2 > a > span.count', regex=r'[^\d]*'),
)

page_shop_1 = Page(name='大众点评酒店店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#poi-list > div.content-wrap > div > div.list-wrapper > div.content > ul > li',item_start=11,item_end=12), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection))

page_shop_2 = Page(name='大众点评酒店店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector='div.hotel-info-ctn > div.hotel-info-main > h2 > a.hotel-name-link'),mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection), is_save=True)

def get_rate(self, _str):
    return str(int(re.sub('[^\d]*','',_str))/10)

def get_comment_rate_tag(self, _str):
    p = PyQuery(_str)
    tag_list = []
    for i in p('span.item').items():
        tag_list.append(i.text().strip())
    return json.dumps(tag_list, ensure_ascii=False)

def get_comment_content(self, _str):
    return PyQuery(_str).text().replace('收起评论','')

fl_comment1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='#review-list > div.review-list-container > div.review-list-main > div.review-list-header > h1 > a', is_isolated=True),
    Field(fieldname=FieldName.COMMENT_USER_NAME, css_selector='div > div.dper-info > a'),
    Field(fieldname=FieldName.COMMENT_TIME, css_selector='div > div.misc-info.clearfix > span.time'),
    Field(fieldname=FieldName.COMMENT_USER_RATE, css_selector='div > div.dper-info > span', attr='class', filter_func=get_rate),
    Field(fieldname=FieldName.COMMENT_RATE, css_selector='div > div.review-rank > span.sml-rank-stars', attr='class', filter_func=get_rate),
    Field(fieldname=FieldName.COMMENT_RATE_TAG, css_selector='div > div.review-rank > span.score', attr='innerHTML', filter_func=get_comment_rate_tag),
    Field(fieldname=FieldName.COMMENT_CONTENT, css_selector='div > div.review-words.Hide', attr='innerHTML', filter_func=get_comment_content),
    Field(fieldname=FieldName.COMMENT_PIC_LIST, list_css_selector='div > div.review-pictures > ul', item_css_selector='li > a > img', attr='src', timeout=0),
)

page_comment_1 = Page(name='大众点评酒店评论列表', fieldlist=fl_comment1, listcssselector=ListCssSelector(list_css_selector='#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.reviews-items > ul > li'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)

class DianpingHotelSpider(TravelDriver):

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

    def get_shop_info(self):
        try:
            shop_data_list = self.from_page_get_data_list(page=page_shop_1)
            nextpagesetup = NextPageCssSelectorSetup(css_selector='#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.bottom-area.clearfix > div > a.NextPage',page=page_comment_1, pause_time=2, pre_pagefunc=PageFunc(func=self.more_comment), after_pagefunc=PageFunc(func=self.close_curr_page))
            extra_pagefunc = PageFunc(func=self.get_newest_comment_data_by_css_selector, nextpagesetup=nextpagesetup, shop_name_css_selector='#poi-detail > div.container > div.base-info > div.main-detail.clearfix > div.main-detail-left > div.main-detail-left-top.clearfix > div.hotel-detail-info > div > h1', is_effective=False)
            self.from_page_add_data_to_data_list(page=page_shop_2, pre_page=page_shop_1, data_list=shop_data_list, extra_pagefunc=extra_pagefunc)
        except Exception as e:
            self.error_log(e=str(e))

    def get_shop_info_list(self):
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
        time.sleep(2)
        self.fast_click_first_item_page_by_partial_link_text(link_text='酒店')
        self.debug_log(data='暂停20秒......')
        time.sleep(5)
        self.until_click_no_next_page_by_css_selector(nextpagesetup=NextPageCssSelectorSetup(css_selector='#poi-list > div.content-wrap > div > div.page > a.next', main_pagefunc=PageFunc(func=self.get_shop_info), is_next=False))

    def run_spider(self):
        try:
            self.get_shop_info_list()
        except Exception as e:
            self.error_log(e=str(e))