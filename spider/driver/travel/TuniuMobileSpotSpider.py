from spider.driver.travel.core.traveldriver import TravelDriver
from spider.driver.base.page import Page,NextPageCssSelectorSetup,PageFunc,NextPageLinkTextSetup
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
import math
import datetime

def get_shop_address(self,_str):
    return ""
def get_shop_grade(self,_str):
    return ""
def get_shop_feature(self,_str):
    return ""
def get_shop_rate(self,_str):
    return ""

def get_shop_comment_url(self,_str):
    shop_id = re.findall(r'([\d]{1,10})',_str)[0];
    shop_comment_url = "https://m.tuniu.com/h5/tour/comment/" + shop_id + "/4"
    return shop_comment_url


fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='a > div.search-scenic-content > h3'),
#\31 302 > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(1) > span:nth-child(2)
#\32 0808 > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(1) > span:nth-child(2)
    Field(fieldname=FieldName.SHOP_PRICE, css_selector='a > div.search-scenic-content > div.search-scenic-wrapper > div.search-scenic-price > span',is_info=True),
    #稍微有点问题
    Field(fieldname=FieldName.SHOP_URL,css_selector='a',attr='href', is_debug=True,is_info=True),
    #img还有些许问题
#\33 6822720 > div:nth-child(1) > div
    Field(fieldname=FieldName.SHOP_IMG, css_selector='a > div.img-container.lazy-img-box.fl > img', attr='src', is_info=True),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector= '',filter_func=get_shop_address, is_info=True),
    #这里应该做一个转换
#\34 187 > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(2) > span:nth-child(1)
    Field(fieldname=FieldName.SHOP_GRADE,css_selector='',filter_func=get_shop_grade, is_info=True),
    #正则表达式的使用有问题
    Field(fieldname=FieldName.SHOP_COMMENT_NUM,css_selector='a > div.search-scenic-content > div.search-scenic-wrapper > div.search-scenic-detail > p',is_info=True),
    #无shop_feature

    Field(fieldname=FieldName.SHOP_FEATURE, css_selector='',filter_func=get_shop_feature, is_info=True),

    Field(fieldname=FieldName.SHOP_RATE,css_selector='',filter_func=get_shop_rate, is_info=True),
Field(fieldname=FieldName.SHOP_COMMENT_URL,css_selector='a',attr='href',filter_func=get_shop_comment_url, is_info=True)
)
page_shop_1 = Page(name='途牛景点店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#search-container > section > div > ul > li'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection), is_save=True)
fl_shop2 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME,
          css_selector='#main-page > div.mp-main > div.mp-headfigure > div.mp-headfeagure-info > div'),
    Field(fieldname=FieldName.SHOP_COMMENT_URL,
          css_selector='#main-page > div.mp-main > div.mp-baseinfo > div.mpg-flexbox.mp-flex-card > div:nth-child(1) > a',
          attr='href', is_info=True)
)

page_shop_2 = Page(name='途牛景点店铺详情页面', fieldlist=fl_shop2)

def get_comment_user_name(self,_str):
    comment_user_name = _str.split(' ')[0];
    return comment_user_name;


def get_comment_score(self,_str):

    if(_str == '满意'):
        return "5.0"
    elif(_str == '一般'):
        return "2.5"
    else:
        return "0"
def get_comment_time(self,_str):
    # 时间格式统一为2018-12-08
    return _str[0:10]

def get_comment_year(self,_str):
    time =_str[0:10]
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
def get_shop_name(self,_str):
    return self.shop_name

def get_shop_name_search_key(self,_str):

    return self.shop_name_search_key(self.shop_name);






fl_comment1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='',filter_func=get_shop_name, is_info=True),
#app > div > div.poi-rate-container > div:nth-child(2) > div.rate-content-container > div
#app > div > div.poi-rate-container > div:nth-child(7) > div.rate-content-container > div
    Field(fieldname=FieldName.SHOP_NAME_SEARCH_KEY,
          css_selector='',
        filter_func=get_shop_name_search_key,  is_info=True),
    Field(fieldname=FieldName.COMMENT_USER_NAME,filter_func=get_comment_user_name,
          css_selector="div.header > div > span.username", is_info=True),
Field(fieldname=FieldName.COMMENT_TIME, css_selector='div.header > div > span.date',filter_func=get_comment_time, is_info=True),
Field(fieldname=FieldName.COMMENT_YEAR, css_selector='div.header > div > span.date',filter_func=get_comment_year, is_info=False),
Field(fieldname=FieldName.COMMENT_SEASON, css_selector='div.header > div > span.date',filter_func=get_comment_season, is_info=False),
Field(fieldname=FieldName.COMMENT_MONTH, css_selector='div.header > div > span.date',filter_func=get_comment_month, is_info=False),
    Field(fieldname=FieldName.COMMENT_WEEK, css_selector='div.header > div > span.date',filter_func=get_comment_week, is_info=False),
    Field(fieldname=FieldName.DATA_REGION_SEARCH_KEY, css_selector='', filter_func=get_data_region_search_key,
          is_info=True),


    Field(fieldname=FieldName.COMMENT_CONTENT, css_selector='div.desc.dt-item-des > div.desc-container > p', is_info=False),

    #comment_grade有待商榷
    Field(fieldname=FieldName.COMMENT_SCORE, css_selector='div.header > div > span.username > p',filter_func=get_comment_score, is_info=False),

)
page_comment_1 = Page(name='途牛景点店铺评论列表页面', fieldlist=fl_comment1, listcssselector=ListCssSelector(list_css_selector='#J_app > div > div.page-body > div > div'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)

class TuniuMobileSpotSpider(TravelDriver):

    def get_shop_info_list(self):


        self.fast_get_page(url='https://m.tuniu.com/m2015/mpChannel/search?searchType=1&catId=0&poiId=0&productType=4&keyword=' + self.data_region)
        shop_data_list = self.from_page_get_data_list(page=page_shop_1)


    def get_comment_info_list(self):
       shop_collcetion = Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection,
                                 host='localhost').get_collection()
       shop_name_url_list = list()
       for i in shop_collcetion.find(self.get_data_key()):
           if i.get('shop_url'):
               shop_name_url_list.append((i.get('shop_name'), i.get('shop_comment_url')))

       for i in range(len(shop_name_url_list)):
           self.fast_new_page(url="https://www.baidu.com");
           # 可能会有反爬
           self.info_log(data='第%s个,%s' % (i + 1, shop_name_url_list[i][0]))
           self.fast_new_page(url=shop_name_url_list[i][1])

           self.shop_name = shop_name_url_list[i][0];

           time.sleep(5)

           self.until_click_no_next_page_by_partial_link_text(nextpagesetup=NextPageLinkTextSetup(link_text='下一页',
               main_pagefunc=PageFunc(
                   func=self.from_page_get_data_list,
                   page=page_comment_1), pause_time=5))
           self.close_curr_page()


    def run_spider(self):
       #self.get_shop_info_list()

       self.get_comment_info_list()