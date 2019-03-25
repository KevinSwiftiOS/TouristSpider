# -*- coding:utf-8 -*-

from spider.driver.base.field import Fieldlist,Field,FieldName
from spider.driver.base.tabsetup import TabSetup
from spider.driver.base.page import Page
from spider.driver.base.listcssselector import ListCssSelector
from spider.driver.base.mongodb import Mongodb
from spider.driver.travel.core.traveldriver import TravelDriver
import time
from pyquery import PyQuery
import json

fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='div > div.row-center > div > h5 > a'),
    Field(fieldname=FieldName.SHOP_CURR_URL, css_selector='div > div.row-center > div > h5 > a', attr='href'),
    Field(fieldname=FieldName.SHOP_IMG, css_selector='div > div.row-left.fleft > a > img', attr='src'),
    Field(fieldname=FieldName.SHOP_RATE, css_selector='div > div.row-center > div > h5 > span.row-subtitle', attr='title', regex=r'[^\d]*'),
    Field(fieldname=FieldName.SHOP_ACTIVE_STATUS, css_selector='div > div.row-center > div > p.row-someone-book > span'),
    Field(fieldname=FieldName.SHOP_GRADE, css_selector='div > div.row-sub-right.fright > a > p.score > span.value'),
    Field(fieldname=FieldName.SHOP_COMMENT_NUM, css_selector='div > div.row-sub-right.fright > a > p.comment > span'),
    Field(fieldname=FieldName.SHOP_PRICE, css_selector='div > div.row-right.fright > div.box-price > p > span.pi-price.pi-price-lg', regex=r'[^\d]*'),
)

def get_room_all(self, _str):
    p = PyQuery(_str)
    room_list = []
    for i in p('div.room-item-wrapper > div.room-item-inner > div:nth-child(1)').items():
        room_list.append(i.text().split()[1:])
    return json.dumps(room_list, ensure_ascii=False)

def get_shop_intro(self, _str):
    p = PyQuery(_str)
    info_list = p.text().split('\n')
    intro = {info_list[0]: ' '.join(info_list[1:]).replace('展开全部', '')}
    return json.dumps(intro, ensure_ascii=False)

def get_shop_facility(self, _str):
    p = PyQuery(_str)
    facility_list = []
    for i in p('ul > li').items():
        info_list = i.text().split('\n')
        facility = {info_list[0]: info_list[1].split(' ')}
        facility_list.append(facility)
    return json.dumps(facility_list, ensure_ascii=False)

def get_shop_traffic(self, _str):
    p = PyQuery(_str)
    around_traffic = {}
    count = 0
    for i in p('div.J_RichCon > div.tabs > ul > li').items():
        count += 1
        around_traffic.setdefault(i.text(),
                                  p('div.J_RichCon > div.cons > div:nth-child(%s)' % count).text().split('驾车\n')[
                                      -1].split('\n'))
    return json.dumps(around_traffic, ensure_ascii=False)

def get_shop_statistics(self, _str):
    p = PyQuery(_str)
    return json.dumps({'grade_list': p(
        'div:nth-child(3) > div.review-filter > ul.ta-list.clearfix > li.taService').text().split('\n'),
                      'comment_num_list': p(
                          'div:nth-child(3) > div.review-filter > ul.filter-list.clearfix').text().split('\n')[1:]},
                     ensure_ascii=False)

fl_shop2 = Fieldlist(
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='#hotel-page > div > div.hotel-box.hotel-baseinfo > div.info > div.base > p.address', offset=6, try_times=10, pause_time=5),
    Field(fieldname=FieldName.SHOP_ROOM_RECOMMEND_ALL, css_selector='#J_RoomList', attr='innerHTML', filter_func=get_room_all),
    Field(fieldname=FieldName.SHOP_INTRO, css_selector='#hotel-desc', attr='innerHTML', filter_func=get_shop_intro),
    Field(fieldname=FieldName.SHOP_FACILITIES, css_selector='#hotel-facility', attr='innerHTML', filter_func=get_shop_facility),
    Field(fieldname=FieldName.SHOP_TRAFFIC, css_selector='#rich-map-wrap', attr='innerHTML', filter_func=get_shop_traffic),
    Field(fieldname=FieldName.SHOP_STATISTICS, css_selector='#hotel-review', attr='innerHTML', filter_func=get_shop_statistics),
)

page_shop_1 = Page(name='飞猪酒店店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#J_List > div'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection))

page_shop_2 = Page(name='飞猪酒店店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector='div > div.row-center > div > h5 > a'),mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection), is_save=True)

class FliggyHotelSpider(TravelDriver):

    def page_shop_2_func(self):
        try:
            self.move_to_element_by_css_selector(css_selector='#rich-map-wrap > div.J_RichCon > div.tabs > ul')
            self.vertical_scroll_by(offset=-200)
            for i in self.until_presence_of_all_elements_located_by_css_selector(css_selector='#rich-map-wrap > div.J_RichCon > div.tabs > ul > li.J_Tab'):
                i.click()
        except Exception:
            self.error_log(e='找不到元素')
        time.sleep(3)

    def get_shop_info(self):
        try:
            shop_data_list = self.from_page_get_data_list(page=page_shop_1)
            self.from_page_add_data_to_data_list(page=page_shop_2, data_list=shop_data_list, pre_page=page_shop_1, page_func=self.page_shop_2_func)
        except Exception as e:
            self.error_log(e=e)

    def get_shop_info_list(self):
        self.fast_get_page('http://www.baidu.com/')
        time.sleep(1)
        self.until_send_text_by_css_selector(css_selector='#kw', text=self.data_website)
        self.until_send_enter_by_css_selector(css_selector='#kw')
        time.sleep(2)
        self.until_presence_of_all_elements_located_by_partial_link_text(link_text='：国内外机票、酒店、火车票、旅游度假预订！')[0].click()
        self.close_pre_page()
        time.sleep(1)
        self.until_presence_of_all_elements_located_by_partial_link_text(link_text='酒店')[0].click()
        time.sleep(1)
        self.until_send_text_by_css_selector(css_selector='#J_HotelForm > ul > li:nth-child(1) > input.pi-input.J_ArrCity.ks-autocomplete-input', text=self.data_region)
        time.sleep(1)
        self.until_send_text_by_css_selector(css_selector='#J_HotelForm > ul > li:nth-child(2) > input', text=self.data_region)
        self.fast_enter_page_by_css_selector(css_selector='#J_HotelForm > ul > li:nth-child(1) > input.pi-input.J_ArrCity.ks-autocomplete-input')
        self.close_pre_page()
        time.sleep(1)
        self.vertical_scroll_to()  # 滚动到页面底部
        self.until_click_no_next_page_by_partial_link_text(link_text='下一页', func=self.get_shop_info)

    def run_spider(self):
        try:
            self.get_shop_info_list()
        except Exception:
            self.error_log()

