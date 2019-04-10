# -*- coding:utf-8 -*-

from spider.driver.travel.core.traveldriver import TravelDriver
from spider.driver.base.page import Page,NextPageCssSelectorSetup,PageFunc
from spider.driver.base.field import Fieldlist,Field,FieldName
from spider.driver.base.tabsetup import TabSetup
from spider.driver.base.listcssselector import ListCssSelector
from spider.driver.base.mongodb import Mongodb
from pyquery import PyQuery as pq
from selenium import webdriver
import re
import time
import json
from pyquery import PyQuery
import datetime
import math
def get_shop_address(self,_str):
    return ""
def _get_shop_comment_num(self,_str):
    return ""
def get_shop_url(self,_str):
    return 'https://market.m.taobao.com/apps/market/travelticket/detail.html?wh_weex=true&scenicId=' + str(_str) + '&gsCallback=' + str(_str)
def get_shop_img(self,_str):
    return ""
fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='div:nth-child(2) > span'),
#\31 302 > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(1) > span:nth-child(2)
#\32 0808 > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(1) > span:nth-child(2)
    Field(fieldname=FieldName.SHOP_PRICE, css_selector='div:nth-child(2) > div:nth-child(3) > div > div:nth-child(1) > span:nth-child(2)',is_info=True),
    #稍微有点问题
    Field(fieldname=FieldName.SHOP_URL,css_selector='',attr='id',filter_func=get_shop_url, is_debug=True,is_info=True),
    #img还有些许问题
#\33 6822720 > div:nth-child(1) > div
    Field(fieldname=FieldName.SHOP_IMG, css_selector='', attr='',filter_func=get_shop_img, is_info=True),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector= '',filter_func=get_shop_address, is_info=True),
    #这里应该做一个转换
#\34 187 > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(2) > span:nth-child(1)
    Field(fieldname=FieldName.SHOP_GRADE,css_selector='div:nth-child(2) > div:nth-child(3) > div > div:nth-child(2) > span:nth-child(1)',is_info=True),
    #正则表达式的使用有问题
    Field(fieldname=FieldName.SHOP_COMMENT_NUM,css_selector='',filter_func=_get_shop_comment_num,is_info=True),
    #无shop_feature

    Field(fieldname=FieldName.SHOP_FEATURE, css_selector='div:nth-child(2) > div:nth-child(2) > span',is_info=True),

    Field(fieldname=FieldName.SHOP_RATE,css_selector='div:nth-child(2) > div:nth-child(3) > span',is_info=True)
)

page_shop_1 = Page(name='飞猪景点店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#tus-recycleview > div > div', item_css_selector='div', item_start=4), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection), is_save=True)

fl_shop2 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='body > div > div.rax-scrollview > div > div:nth-child(1) > div > div:nth-child(1) > span'),
    Field(fieldname=FieldName.SHOP_COMMENT_URL,css_selector='body > div > div.rax-scrollview > div > div:nth-child(1) > div > div:nth-child(3) > div:nth-child(2)',attr='href', is_info=True)
)

page_shop_2 = Page(name='飞猪景点店铺详情页面',fieldlist=fl_shop2)



def get_comment_grade(self,_str):

    html = pq(_str)

    return str(html('.star-full').length)
def get_shop_name(self,_str):
    return self.shop_name
def get_comment_year(self,_str):
    time = _str[0:10]
    return time[0:4];

def get_comment_season(self, _str):
    time = _str[0:10]
    times = time.split('-');

    month = int(times[1])

    seasons = ['01', '02', '03', '04'];
    if (month % 3 == 0):
        return (times[0] + '-' + seasons[int(month / 3) - 1]);
    else:
        index = int(math.floor(month / 3));
        return (times[0] + '-' + seasons[index]);
def get_comment_month(self, _str):
    time = _str[0:10]
    return time[0:7];
def get_comment_week(self, _str):

    time = _str[0:10]
    times = time.split('-');
    return (times[0] + '-' + str(datetime.date(int(times[0]), int(times[1]), int(times[2])).isocalendar()[1]).zfill(2))

def get_data_region_search_key(self, _str):

    return  self.data_region_search_key
def get_shop_name_search_key(self,_str):

    return self.shop_name_search_key(self.shop_name);


fl_comment1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='#app > div > div.rate-info-container > div.rate-info > div.rate-score > div.rate-cnt',filter_func=get_shop_name, is_info=True,is_isolated=True),
    Field(fieldname=FieldName.SHOP_NAME_SEARCH_KEY,
          css_selector='#app > div > div.rate-info-container > div.rate-info > div.rate-score > div.rate-cnt',
          filter_func=get_shop_name_search_key, is_info=True, is_isolated=True),
#app > div > div.poi-rate-container > div:nth-child(2) > div.rate-content-container > div
#app > div > div.poi-rate-container > div:nth-child(7) > div.rate-content-container > div
    Field(fieldname=FieldName.COMMENT_CONTENT, css_selector='div.rate-content-container > div.rate-content.fold', is_info=True),
    Field(fieldname=FieldName.COMMENT_USER_NAME, css_selector='div.rate-info > div.avatar-info > div:nth-child(1) > div', is_info=True),
    #comment_grade有待商榷
    Field(fieldname=FieldName.COMMENT_SCORE, css_selector='div.rate-info > div.avatar-info > div:nth-child(2) > div.left > div > div', attr='innerHTML',filter_func=get_comment_grade, is_info=True),
    Field(fieldname=FieldName.COMMENT_TIME, css_selector='div.rate-info > div.avatar-info > div:nth-child(2) > div.time', is_info=True),
    Field(fieldname=FieldName.COMMENT_YEAR, css_selector='div.rate-info > div.avatar-info > div:nth-child(2) > div.time', filter_func=get_comment_year,
          is_info=False),
    Field(fieldname=FieldName.COMMENT_SEASON, css_selector='div.rate-info > div.avatar-info > div:nth-child(2) > div.time', filter_func=get_comment_season,
          is_info=False),
    Field(fieldname=FieldName.COMMENT_MONTH, css_selector='div.rate-info > div.avatar-info > div:nth-child(2) > div.time', filter_func=get_comment_month,
          is_info=False),
    Field(fieldname=FieldName.COMMENT_WEEK, css_selector='div.rate-info > div.avatar-info > div:nth-child(2) > div.time', filter_func=get_comment_week,
          is_info=False),
    Field(fieldname=FieldName.DATA_REGION_SEARCH_KEY, css_selector='', filter_func=get_data_region_search_key,
          is_info=False),
)
page_comment_1 = Page(name='飞猪景点店铺评论列表页面', fieldlist=fl_comment1, listcssselector=ListCssSelector(list_css_selector='#app > div > div.poi-rate-container > div'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)


class FliggySpotSpider(TravelDriver):

    def get_shop_info_list(self):
        self.fast_get_page(url='https://h5.m.taobao.com/trip/rx-search/travel-list/index.html?keyword=' + self.data_region + '&nav=SCENIC')
        time.sleep(30)
        shop_data_list = self.from_page_get_data_list(page=page_shop_1)
        # action = webdriver.TouchActions(self.driver)

        # action = webdriver.TouchActions(self.driver)
        #
        # action.tap(self.driver.find_element_by_css_selector('body > div > div:nth-child(4) > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(4)')).perform()
        # print(223)
    def get_shop_detail(self):
        shop_collcetion = Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection,
                                  host='localhost').get_collection()

        shop_url_set = set()
        for i in shop_collcetion.find(self.get_data_key()):
            shop_url_set.add(i.get(FieldName.SHOP_URL))

        for url in shop_url_set:
            self.fast_new_page(url=url)
            time.sleep(5)
            data = self.from_fieldlist_get_data(page=page_shop_2)
            self.update_data_to_mongodb(shop_collcetion,
                                        self.merge_dict(self.get_data_key(), {FieldName.SHOP_URL: url}), data)
            self.close_curr_page()

    def get_comment_info_list(self):
        #打开知道
        self.fast_new_page('http://www.baidu.com')
        shop_collcetion = Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection,
                                  host='localhost').get_collection()
        shop_name_url_list = list()
        for i in shop_collcetion.find(self.get_data_key()):
            if i.get('shop_comment_url'):
                shop_name_url_list.append((i.get('shop_name'), i.get('shop_comment_url')))

        for i in range(len(shop_name_url_list)):
            #可能会有反爬
            self.info_log(data='第%s个,%s' % (i + 1, shop_name_url_list[i][0]))
            self.fast_new_page('http://www.baidu.com')
            self.fast_new_page(url=shop_name_url_list[i][1])
            self.shop_name =  shop_name_url_list[i][0]
            comment_data_list = self.from_page_get_data_list(page=page_comment_1)
            # for j in range(0,len(comment_data_list)):
            #     comment_data_list[j]['shop_name'] = shop_name_url_list[i][0]
            #     self.save_data_to_mongodb(fieldlist= fl_comment1, mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), data=comment_data_list[j])
            # print(comment_data_list)
            self.close_curr_page()

        #从数据库中读取
        # body > div > div.rax - scrollview > div > div: nth - child(6) > div > div:nth - child(2) > div: nth - child(5) > span


        # comment_data_list = self.from_page_get_data_list(page=page_comment_1)
    def login(self):
        #进行登录
        self.fast_new_page(url='http://www.baidu.com')
        self.fast_new_page(url='https://h5.m.taobao.com')
        time.sleep(2)
        # self.until_scroll_to_center_send_text_by_css_selector(css_selector='#kw', text=self.data_region + self.data_website)
        # self.until_scroll_to_center_send_enter_by_css_selector(css_selector='#kw')
        # self.fast_click_first_item_page_by_partial_link_text(link_text=self.data_website)
        with open('./cookies/fliggy_cookies.json', 'r', encoding='utf-8') as f:
            listCookies = json.loads(f.read())

        for cookie in listCookies:
            self.driver.add_cookie(cookie)
        self.close_curr_page()
        self.fast_new_page(url="https://h5.m.taobao.com")
        #  self.fast_click_first_item_page_by_partial_link_text(link_text=self.data_website)
        time.sleep(10)

    def run_spider(self):
        #进行登录
        self.login();
        #self.get_shop_info_list()
        #self.get_shop_detail()
        self.data_region_search_key  =self.get_data_region_search_key()
        self.get_comment_info_list()


