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
def get_shop_feature(self,_str):
    return ""
fl_shop1 = Fieldlist(

    Field(fieldname=FieldName.SHOP_NAME,css_selector=' a.e_title.js_list_name',is_debug=True),

    Field(fieldname=FieldName.SHOP_URL,css_selector='a.e_title.js_list_name',attr='href',is_info=True),
    Field(fieldname=FieldName.SHOP_IMG, css_selector='a > img:nth-child(1)', attr='src',is_info=True),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='div > div > div.clrfix > div.item_hotel_info > div.item_hotel_bsinfo > table > tbody > tr > td.item_hotel_name > div > p > span > em',
          is_info=True),

   Field(fieldname=FieldName.SHOP_PRICE,css_selector=' div > div > div.clrfix > div.item_hotel_info > div.hotel_price >  div > div > div > p > a > b', is_info=True),
    #正则表达式不一样 小问题
    Field(fieldname=FieldName.SHOP_COMMENT_NUM,css_selector=' div > div > div.clrfix > div.item_hotel_info > div.item_hotel_bsinfo > table > tbody > tr > td.item_hotel_name > div > div.level.levelmargin > a.level_comment.level_commentbd.js_list_usercomcount', is_info=True),


    Field(fieldname=FieldName.SHOP_GRADE,css_selector='div > div > div.clrfix > div.item_hotel_info > div.item_hotel_bsinfo > table > tbody > tr > td.item_hotel_name > div > div.level.levelmargin > a.level_score.js_list_score > strong',is_info=True),
    Field(fieldname=FieldName.SHOP_RATE,
          css_selector='',filter_func=get_shop_rate,
          is_info=True),
    Field(fieldname=FieldName.SHOP_FEATURE,filter_func=get_shop_feature,
          css_selector='',
          is_info=True)
)


fl_shop2 = Fieldlist(
)
page_shop_1 = Page(name='去哪儿酒店店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#jxContentPanel > div',), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection),is_save=True)

page_shop_2 = Page(name='去哪儿酒店店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector='a.e_title.js_list_name'), mongodb=Mongodb(db=TravelDriver.db,collection=TravelDriver.shop_collection))




def get_comment_grade(self,_str):
    return str(_str[-1])
def get_comment_time(self,_str):
    #时间格式统一为2018-12-08
    print(_str)
    return _str[0:10]
fl_comment1 = Fieldlist(
    Field(fieldname=FieldName.COMMENT_USER_NAME, css_selector=' div.l_user > div.usernickname.js-name > a',
          is_info=True),
    Field(fieldname=FieldName.COMMENT_TIME, css_selector='div.l_feed > ul > li:nth-child(2)', is_info=True,
          filter_func=get_comment_time),
#bnb_detail_pageHeader > div.b-baseinfo-title > h2 > span
#bnb_detail_pageHeader > div.b-baseinfo-title > h2 > span
# body > div.b_wrap > div.b-crumbs > div > span.bread-crumbs > span
    Field(fieldname=FieldName.SHOP_NAME, css_selector='#bnb_detail_pageHeader > div.b-baseinfo-title > h2 > span', is_isolated=True,
          is_info=True),
    Field(fieldname=FieldName.COMMENT_CONTENT, css_selector='div.l_feed > div.comment > div > p.js-full', is_info=True),
    # 有问题
    Field(fieldname=FieldName.COMMENT_SCORE, css_selector=' div.l_feed > div.grade.clrfix > div > div.m_star.m_star_mini.js-ref > div', attr='style',
           is_info=True),


)
fl_comment2 = Fieldlist(

)

page_comment_1 = Page(name='去哪儿酒店评论列表', fieldlist=fl_comment1, listcssselector=ListCssSelector(list_css_selector='div.js-feed-list > div'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)


class QunarHotelSpider(TravelDriver):

    def get_shop_info(self):
        try:
            shop_data_list = self.from_page_get_data_list(page=page_shop_1)

            nextpagesetup = NextPageCssSelectorSetup(
                css_selector='#comment_main > div > div.wrapper > div.b_ugcpager.clrfix.js-pager-container > div.js-pager > div > a.next > span'
                ,
                stop_css_selector='#comment_main > div > div.wrapper > div.b_ugcpager.clrfix.js-pager-container > div.js-pager > div > a.next > span.hidden',
                page=page_comment_1, pause_time=2)
            extra_pagefunc = PageFunc(func=self.get_newest_comment_data_by_css_selector, nextpagesetup=nextpagesetup)
            self.from_page_add_data_to_data_list(page=page_shop_2, pre_page=page_shop_1, data_list=shop_data_list,
                                                 extra_pagefunc=extra_pagefunc)



        except Exception as e:
            self.error_log(e=str(e))
    #获取评论详情


    def get_shop_info_list(self):
        city = self.get_city_from_region_ENG(self.data_region)
        self.fast_get_page('http://hotel.qunar.com/city' + city, is_max=False,is_scroll_to_bottom=False)
        time.sleep(2)

        self.until_send_text_by_css_selector(css_selector='#jxQ', text=self.data_region)
        self.until_send_enter_by_css_selector(css_selector='#jxQ')




        self.vertical_scroll_to(offset=1000000000)  # 滚动到页面底部
        # self.until_ismore_by_send_key_arrow_down_judge_by_len(list_css_selector='#search-list > div',
        #                                                       ele_css_selector='#loadingDiv > div')
        self.vertical_scroll_to()  # 滚动到页面底部
        time.sleep(5)
        self.until_click_no_next_page_by_partial_link_text(
            nextpagesetup=NextPageLinkTextSetup(link_text="下一页", main_pagefunc=PageFunc(func=self.get_shop_info)))
    def run_spider(self):
        try:
            self.get_shop_info_list()
        except Exception:
            self.error_log()
