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
def get_shop_rate(self,_str):
    return ""
def get_shop_grade(self,_str):
    return "0.0"
fl_shop1 = Fieldlist(
    ##_j_search_result_left > div:nth-child(1) > div > div:nth-child(1) > div.ct-text > h3 > a
    Field(fieldname=FieldName.SHOP_NAME, css_selector='div.ct-text > h3 > a', is_debug=True),
#_j_search_result_left > div:nth-child(1) > div > div:nth-child(2) > div.ct-text > h3 > a

    Field(fieldname=FieldName.SHOP_URL, css_selector='div > div.ct-text > h3 > a', attr='href', is_info=True),
    Field(fieldname=FieldName.SHOP_IMG, css_selector='div.flt1 > a > img', attr='src', is_info=True),
#_j_search_result_left > div:nth-child(1) > div > div:nth-child(1) > div.ct-text > div > p:nth-child(1)
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='div.ct-text > ul > li:nth-child(1) > a',
          is_info=True),

     Field(fieldname=FieldName.SHOP_PRICE,css_selector='div.ct-text > ul > li.frt._j_hotel_ota > a > span.seg-price'),
    # 正则表达式不一样
#_j_search_result_left > div:nth-child(1) > div > div:nth-child(2) > div.ct-text > ul > li:nth-child(2) > a
    Field(fieldname=FieldName.SHOP_COMMENT_NUM, css_selector='div.ct-text > ul > li:nth-child(2) > a',
          is_info=True),
    Field(fieldname=FieldName.SHOP_FEATURE, css_selector='div.ct-text > div > p:nth-child(1)',
          is_info=True),
    Field(fieldname=FieldName.SHOP_GRADE, css_selector='',filter_func=get_shop_grade,
          is_info=True),
    Field(fieldname=FieldName.SHOP_RATE, css_selector='',filter_func=get_shop_rate,
          is_info=True),

)





fl_shop2 = Fieldlist()

page_shop_1 = Page(name='马蜂窝酒店店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#_j_search_result_left > div:nth-child(1) > div > div'),mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection),is_save=True)

page_shop_2 = Page(name='马蜂窝酒店店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector='div > div.ct-text > h3 > a'),mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection))
#获取评论得分
def get_comment_grade(self,_str):

    return str(_str[-1])
def get_comment_time(self,_str):
    #时间格式统一为2018-12-08

    return _str[0:10]
fl_comment1 = Fieldlist(
#_j_comment_list > div:nth-child(1) > div.user > a.name
    Field(fieldname=FieldName.COMMENT_USER_NAME, css_selector='div.user > a.name',is_info=True),
    Field(fieldname=FieldName.COMMENT_TIME, css_selector='div.comm-meta > span.time', is_info=True,filter_func=get_comment_time),
    Field(fieldname=FieldName.SHOP_NAME, css_selector='body > div:nth-child(2) > div.hotel-intro > div.intro-hd > div.main-title > h1', is_isolated=True,is_info=True),
    Field(fieldname=FieldName.COMMENT_CONTENT, css_selector=' div.txt',is_info=True),
    #有问题
    Field(fieldname=FieldName.COMMENT_SCORE, css_selector=' div.comm-meta > span.comm-star', attr='class',filter_func=get_comment_grade,  regex=r'[^\d.]*',is_info=True),
)
#_j_comment_list
page_comment_1 = Page(name='马蜂窝酒店评论列表', fieldlist=fl_comment1, listcssselector=ListCssSelector(list_css_selector='#_j_comment_list > div'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)
class MafengwoHotelSpider(TravelDriver):
    def get_shop_info(self):
        try:

            shop_data_list = self.from_page_get_data_list(page=page_shop_1)

            nextpagesetup = NextPageCssSelectorSetup(
                css_selector='#_j_comment_pagination > a.pg-next._j_pageitem'
                ,
                stop_css_selector='#_j_comment_pagination > a.pg-next._j_pageitem.hidden',
                page=page_comment_1, pause_time=2)
            extra_pagefunc = PageFunc(func=self.get_newest_comment_data_by_css_selector, nextpagesetup=nextpagesetup)
            self.from_page_add_data_to_data_list(page=page_shop_2, pre_page=page_shop_1, data_list=shop_data_list,
                                                 extra_pagefunc=extra_pagefunc
                                                 )
        except Exception as e:
            self.error_log(e=str(e))

    def get_shop_info_list(self):
        self.fast_get_page('http://www.mafengwo.cn/', is_max=False)
        time.sleep(2)
        self.until_send_text_by_css_selector(css_selector='#_j_index_search_input_all', text=self.data_region)
        self.until_send_enter_by_css_selector(css_selector='#_j_index_search_input_all')
        self.fast_click_first_item_same_page_by_partial_link_text('酒店')
        self.fast_click_page_by_css_selector('#_j_mfw_search_main > div.s-nav > div > div > a:nth-child(6)')
        time.sleep(1)

        self.vertical_scroll_to()  # 滚动到页面底部
        self.until_click_no_next_page_by_partial_link_text(

            nextpagesetup=NextPageLinkTextSetup(link_text="下一页", main_pagefunc=PageFunc(func=self.get_shop_info)))

    def run_spider(self):
        try:
            self.get_shop_info_list()
        except Exception:
            self.error_log()
