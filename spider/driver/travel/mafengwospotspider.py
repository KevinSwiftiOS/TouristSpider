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
import datetime
import math
def get_comment_num(self,_str):
    num = re.findall(r'[\d]{1,10}',_str)
    return str(num[0])
def get_shop_grade(self,_str):
    return "0.0"
def get_shop_price(self,_str):
    return "0.0"
def get_shop_rate(self,_str):
    return ""
fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME,css_selector='div > div.ct-text > h3 > a',is_debug=True),
    Field(fieldname=FieldName.SHOP_RATE,css_selector='',is_info=True,filter_func=get_shop_rate),
    Field(fieldname=FieldName.SHOP_URL,css_selector='div > div.ct-text > h3 > a',attr='href',is_info=True),
    Field(fieldname=FieldName.SHOP_IMG, css_selector=' div > div.flt1 > a > img', attr='src',is_info=True),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='div > div.ct-text > ul > li:nth-child(1) > a',
          is_info=True),

    Field(fieldname=FieldName.SHOP_GRADE,css_selector='',filter_func=get_shop_grade),
    #正则表达式不一样
    Field(fieldname=FieldName.SHOP_COMMENT_NUM,css_selector='div > div.ct-text > ul > li:nth-child(2) > a',filter_func=get_comment_num, is_info=True),

    Field(fieldname=FieldName.SHOP_FEATURE, css_selector='div > div.ct-text > p',is_info=True),
    Field(fieldname=FieldName.SHOP_PRICE,css_selector= '',filter_func=get_shop_price, is_info=True)
)


fl_shop2 = Fieldlist(
)
page_shop_1 = Page(name='马蜂窝景点店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#_j_search_result_left > div:nth-child(1) > div > ul > li',), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection),is_save=True)
page_shop_2 = Page()
page_shop_2 = Page(name='马蜂窝景点店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector='div > div.ct-text > h3 > a'), mongodb=Mongodb(db=TravelDriver.db,collection=TravelDriver.shop_collection))




def get_comment_grade(self,_str):
    return str(_str[-1])
def get_comment_time(self,_str):
    #时间格式统一为2018-12-08

    return _str[0:10]
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

    return self.shop_name_search_key(_str);




fl_comment1 = Fieldlist(
    Field(fieldname=FieldName.COMMENT_USER_NAME, css_selector='a.name',is_info=True),
    Field(fieldname=FieldName.COMMENT_TIME, css_selector='div.info.clearfix > span', is_info=True,filter_func=get_comment_time),
    Field(fieldname=FieldName.SHOP_NAME, css_selector='body > div.container > div.row.row-top > div > div.title > h1', second_css_selector='body > div.wrapper > div.col-main > div.m-box.m-details.clearfix > div.title.clearfix > div > h1', is_isolated=True,is_info=True),
    Field(fieldname=FieldName.SHOP_NAME_SEARCH_KEY, css_selector='body > div.container > div.row.row-top > div > div.title > h1',
          second_css_selector='body > div.wrapper > div.col-main > div.m-box.m-details.clearfix > div.title.clearfix > div > h1',filter_func=get_shop_name_search_key,
          is_isolated=True, is_info=True),
    Field(fieldname=FieldName.COMMENT_CONTENT, css_selector='p',is_info=False),
    #有问题
    Field(fieldname=FieldName.COMMENT_SCORE, css_selector='span.s-star',attr='class',filter_func=get_comment_grade,is_info=False),
    Field(fieldname=FieldName.COMMENT_YEAR, css_selector='div.info.clearfix > span', filter_func=get_comment_year, is_info=False),
    Field(fieldname=FieldName.COMMENT_SEASON, css_selector='div.info.clearfix > span', filter_func=get_comment_season,
          is_info=False),
    Field(fieldname=FieldName.COMMENT_MONTH, css_selector='div.info.clearfix > span', filter_func=get_comment_month, is_info=False),
    Field(fieldname=FieldName.COMMENT_WEEK, css_selector='div.info.clearfix > span', filter_func=get_comment_week, is_info=False),
    Field(fieldname=FieldName.DATA_REGION_SEARCH_KEY, css_selector='', filter_func=get_data_region_search_key,
          is_info=True),
)
#comment_no_151904132 > div.comment-info > div > div.c-content > p
#comment_header > div.poi-comment.tab-div > div._j_commentlist
page_comment_1 = Page(name='马蜂窝景点评论列表', fieldlist=fl_comment1, listcssselector=ListCssSelector(list_css_selector='div._j_commentlist > div.rev-list > ul > li'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)


class MafengwoSpotSpider(TravelDriver):



    def get_shop_info(self):
        try:
            shop_data_list = self.from_page_get_data_list(page=page_shop_1)


            nextpagesetup = NextPageCssSelectorSetup(
                css_selector='div._j_commentlist > div.m-pagination > a.pi.pg-next'
                             ,
                stop_css_selector='div._j_commentlist > div.m-pagination > a.pi.pg-next.hidden',
                page=page_comment_1, pause_time=2)
            extra_pagefunc = PageFunc(func=self.get_newest_comment_data_by_css_selector, nextpagesetup=nextpagesetup)
            self.from_page_add_data_to_data_list(page=page_shop_2, pre_page=page_shop_1, data_list=shop_data_list,extra_pagefunc=extra_pagefunc
                                                )
        except Exception as e:
            self.error_log(e=str(e))
    def get_shop_info_list(self):
        self.fast_get_page('http://www.mafengwo.cn/', is_max=False)
        time.sleep(2)
        self.until_send_text_by_css_selector(css_selector='#_j_index_search_input_all', text=self.data_region)
        self.until_send_enter_by_css_selector(css_selector='#_j_index_search_input_all')
        self.fast_click_first_item_same_page_by_partial_link_text('景点')
        self.fast_click_page_by_css_selector('#_j_mfw_search_main > div.s-nav > div > div > a:nth-child(4)')
        time.sleep(1)

        self.vertical_scroll_to()  # 滚动到页面底部
        self.until_click_no_next_page_by_partial_link_text(
            nextpagesetup=NextPageLinkTextSetup(link_text="下一页", main_pagefunc=PageFunc(func=self.get_shop_info)))
    def run_spider(self):
        try:
            self.get_shop_info_list()
        except Exception:
            self.error_log()
