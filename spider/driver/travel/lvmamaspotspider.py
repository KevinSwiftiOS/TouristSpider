# -*- coding:utf-8 -*-

from spider.driver.travel.core.traveldriver import TravelDriver
from spider.driver.base.page import Page,NextPageCssSelectorSetup,NextPageLinkTextSetup,PageFunc
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


def get_shop_grade(self,_str):
    saveTo = round(float(_str[0:-1]) / 100 * 5, 1)
    return str(saveTo)
def get_shop_rate(self,_str):
    return ""
fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME,css_selector='div.product-regular.clearfix > div.product-section > h3 > a',is_info=True),
    Field(fieldname=FieldName.SHOP_RATE,css_selector='',is_info=True,filter_func=get_shop_rate),
    Field(fieldname=FieldName.SHOP_URL,css_selector='div.product-regular.clearfix > div.product-section > h3 > a',attr='href',is_info=True),
    Field(fieldname=FieldName.SHOP_IMG, css_selector='div.product-regular.clearfix > div.product-left > a > img', attr='src',is_info=True),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector=' div.product-regular.clearfix > div.product-section > dl:nth-child(3) > dd',is_info=True),
    Field(fieldname=FieldName.SHOP_PRICE,css_selector='div.product-regular.clearfix > div.product-info > div > em',is_info=True),
    Field(fieldname=FieldName.SHOP_COMMENT_NUM,css_selector=' div.product-regular.clearfix > div.product-info > ul > li:nth-child(2) > a '),
    Field(fieldname=FieldName.SHOP_FEATURE, css_selector=' div.product-regular.clearfix > div.product-section > dl:nth-child(6) > dd > div'),
    Field(fieldname=FieldName.SHOP_GRADE,
          css_selector='div.product-regular.clearfix > div.product-info > ul > li:nth-child(1) > b',filter_func=get_shop_grade,is_info=True),
)



fl_shop2 = Fieldlist(

)

page_shop_1 = Page(name='驴妈妈景点店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector=' div.product-list > div',item_css_selector='div'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection),is_save=True)
page_shop_2 = Page()
page_shop_2 = Page(name='驴妈妈景点店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector='div.product-regular.clearfix > div.product-section > h3 > a'), mongodb=Mongodb(db=TravelDriver.db,collection=TravelDriver.shop_collection), is_save=False)



def get_comment_year(self,_str):

    return _str[0:4];

def get_comment_season(self, _str):
    time = _str[0:10];
    times = time.split('-');

    month = int(times[1])

    seasons = ['01', '02', '03', '04'];
    if (month % 3 == 0):
        return (times[0] + '-' + seasons[int(month / 3) - 1]);
    else:
        index = int(math.floor(month / 3));
        return (times[0] + '-' + seasons[index]);
def get_comment_month(self, _str):

    return _str[0:7];
def get_comment_week(self, _str):

    time = _str[0:10]
    times = time.split('-');
    return (times[0] + '-' + str(datetime.date(int(times[0]), int(times[1]), int(times[2])).isocalendar()[1]).zfill(2))

def get_data_region_search_key(self, _str):

    return  self.data_region_search_key

def get_shop_name_search_key(self,_str):

    return self.shop_name_search_key(_str);





fl_comment1 = Fieldlist(
    Field(fieldname=FieldName.COMMENT_USER_NAME, css_selector='div.com-userinfo > p > a:nth-child(1)',is_info=True, attr='title'),
    Field(fieldname=FieldName.COMMENT_TIME, css_selector='div.com-userinfo > p > em',is_info=True),
    Field(fieldname=FieldName.SHOP_NAME, css_selector='body > div.body_bg > div > div.overview > div.dtitle.clearfix > div > h1', is_isolated=True,is_info=True),
Field(fieldname=FieldName.SHOP_NAME_SEARCH_KEY, css_selector='body > div.body_bg > div > div.overview > div.dtitle.clearfix > div > h1',filter_func=get_shop_name_search_key, is_isolated=True,is_info=True),
    Field(fieldname=FieldName.COMMENT_CONTENT, css_selector='div.ufeed-content',is_info=True),
    Field(fieldname=FieldName.COMMENT_SCORE, css_selector='div.ufeed-info > p > span.ufeed-level > i',attr='data-level', regex=r'[^\d.]*',is_info=True),
    Field(fieldname=FieldName.COMMENT_YEAR, css_selector='div.com-userinfo > p > em', filter_func=get_comment_year,
          is_info=False),
    Field(fieldname=FieldName.COMMENT_SEASON, css_selector='div.com-userinfo > p > em', filter_func=get_comment_season,
          is_info=False),
    Field(fieldname=FieldName.COMMENT_MONTH, css_selector='div.com-userinfo > p > em', filter_func=get_comment_month,
          is_info=False),
    Field(fieldname=FieldName.COMMENT_WEEK, css_selector='div.com-userinfo > p > em', filter_func=get_comment_week,
          is_info=False),
    Field(fieldname=FieldName.DATA_REGION_SEARCH_KEY, css_selector='', filter_func=get_data_region_search_key,
          is_info=True),
)

page_comment_1 = Page(name='驴妈妈景点评论列表', fieldlist=fl_comment1, listcssselector=ListCssSelector(list_css_selector='#allCmtComment > div'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)


class LvmamaSpotSpider(TravelDriver):




    def get_shop_info_list(self):
        self.driver.get('https://www.baidu.com')
        self.fast_new_page(url='http://ticket.lvmama.com/', is_scroll_to_bottom=False)
        #self.driver.refresh()
        self.until_scroll_to_center_send_text_by_css_selector(css_selector="body > div.banWrap > div > div.lv_s_box > div.lv_s_all > div.lv_s_input_box > input", text=self.data_region)
        self.until_send_enter_by_css_selector(css_selector='body > div.banWrap > div > div.lv_s_box > div.lv_s_all > div.lv_s_input_box > input')
        time.sleep(5)
        self.until_click_no_next_page_by_partial_link_text(NextPageLinkTextSetup(link_text='下一页', is_proxy=False,
                                                                                 main_pagefunc=PageFunc(
                                                                                     self.from_page_get_data_list,
                                                                                     page=page_shop_1)))


    def get_comment_list(self):
        self.fast_new_page(url="http://www.baidu.com");
        shop_collcetion = Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection,
                                  host='localhost').get_collection()
        shop_name_url_list = list()
        for i in shop_collcetion.find(self.get_data_key()):
            if i.get('shop_url'):
                shop_name_url_list.append((i.get('shop_name'), i.get('shop_url')))
        for i in range(len(shop_name_url_list)):
            self.info_log(data='第%s个,%s'%(i+1, shop_name_url_list[i][0]))
            self.shop_name = shop_name_url_list[i][0];
            self.fast_new_page("http://www.baidu.com")
            self.fast_new_page(url=shop_name_url_list[i][1])
            self.until_click_no_next_page_by_css_selector(nextpagesetup=NextPageCssSelectorSetup(css_selector='#allCmtComment > div.paging.orangestyle > div > a.nextpage',stop_css_selector='#allCmtComment > div.paging.orangestyle > div > a.nextpage.hidden',
                                                                                                   main_pagefunc=PageFunc(
                                                                                                       func=self.from_page_get_data_list,
                                                                                                       page=page_comment_1),pause_time=2))
            self.close_curr_page();

    def run_spider(self):
        try:
            #self.get_shop_info_list()
            self.data_region_search_key = self.get_data_region_search_key()
            self.get_comment_list()

        except Exception as e:
            self.error_log(e=str(e))