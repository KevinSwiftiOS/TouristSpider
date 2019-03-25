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


def get_shop_rate(self,_str):
    return ""
def get_shop_feature(self,_str):
    return ""
fl_shop1 = Fieldlist(



    Field(fieldname=FieldName.SHOP_NAME,css_selector=' div > div.h_info > div.h_info_text > div.h_info_base > p.h_info_b1 > a > span.info_cn',attr='innerHTML', is_info=True),

    Field(fieldname=FieldName.SHOP_URL,css_selector='div > div.h_info_text > div.h_info_base > p.h_info_b1 > a',attr='href',is_info=True),
    Field(fieldname=FieldName.SHOP_IMG, css_selector='div.h_info_pic > a > img', attr='big-src',is_info=True),
    #有些问题
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='div > div.h_info_text > div.h_info_base > p.h_info_b2',is_info=True),
    Field(fieldname=FieldName.SHOP_PRICE,css_selector='div > div.h_info_text > div.h_info_pri > p:nth-child(1) > a > span.h_pri_num',is_info=True),
    #稍许有些问题
    Field(fieldname=FieldName.SHOP_COMMENT_NUM,css_selector='div > div.h_info_text > div.h_info_comt > a > span.c555.block.mt5'),
    Field(fieldname=FieldName.SHOP_GRADE, css_selector=' div > div.h_info_text > div.h_info_comt > a > span.h_info_comt_bg > i.c37e',is_info=True),
    Field(fieldname=FieldName.SHOP_RATE,css_selector='',filter_func=get_shop_rate, is_info=True),
    Field(fieldname=FieldName.SHOP_FEATURE,css_selector='',filter_func=get_shop_feature, is_info=True)

)
fl_shop2 = Fieldlist()
page_shop_1 = Page(name='艺龙酒店店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#hotelContainer > div > div'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection),is_save=True)
# page_shop_2 = Page()
#
page_shop_2 = Page(name='艺龙酒店店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector='div > div.h_info_text > div.h_info_base > p.h_info_b1 > a'), mongodb=Mongodb(db=TravelDriver.db,collection=TravelDriver.shop_collection))
fl_comment1 = Fieldlist(
    Field(fieldname=FieldName.COMMENT_USER_NAME, css_selector=' div.cmt_userinfo > div > p.cmt_un',is_info=True),
    Field(fieldname=FieldName.COMMENT_TIME, css_selector='div.cmt_info_mn > div > div.if_hd_r > span.cmt_con_time', is_info=True),
    Field(fieldname=FieldName.SHOP_NAME,
          css_selector='body > div.hdetail_rela_wrap > div > div.hrela_ns_wrap.clearfix > div.hdetail_main.hrela_name > div > h1',
          is_isolated=True, is_info=True),
    Field(fieldname=FieldName.COMMENT_CONTENT, css_selector='div.cmt_info_mn > p.cmt_txt',is_info=True),
    #有问题
    Field(fieldname=FieldName.COMMENT_SCORE, css_selector='div.cmt_info_mn > div > div.if_hd > b',is_info=True),
)

page_comment_1 = Page(name='艺龙酒店评论列表', fieldlist=fl_comment1, listcssselector=ListCssSelector(list_css_selector='#review > ul > li'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)


class ELongHotelSpider(TravelDriver):




    def get_shop_info(self):
        try:

            shop_data_list = self.from_page_get_data_list(page=page_shop_1)
            nextpagesetup = NextPageCssSelectorSetup(
                css_selector='#comment_paging > a.page_next'
                ,
                stop_css_selector='#comment_paging > a.page_next.hidden',
                page=page_comment_1, pause_time=2)
            extra_pagefunc = PageFunc(func=self.get_newest_comment_data_by_css_selector, nextpagesetup=nextpagesetup)
            self.from_page_add_data_to_data_list(page=page_shop_2, pre_page=page_shop_1, data_list=shop_data_list,
                                                 extra_pagefunc=extra_pagefunc
                                                 )
        except Exception as e:
            self.error_log(e=str(e))

    def get_shop_info_list(self):
        #获取城市
        #cityName = self.get_city_from_region_CHN(self.data_region)
        cityName = self.get_city_from_region_ENG(self.data_region)
        self.fast_get_page('http://hotel.elong.com' + cityName, is_scroll_to_bottom=False)


        # self.until_scroll_to_center_send_text_by_css_selector(css_selector='#domesticDiv > dl:nth-child(1) > dd > input', text='')
        # self.until_scroll_to_center_send_text_by_css_selector(css_selector='#domesticDiv > dl:nth-child(1) > dd > input',text=city)

        self.until_scroll_to_center_send_text_by_css_selector(css_selector='#m_searchBox > div.search_item.search_keywords > label > input', text=self.data_region)

        self.until_scroll_to_center_send_enter_by_css_selector(css_selector="#m_searchBox > div.search_item.search_keywords > label > input")
      #  self.fast_click_page_by_css_selector('#domesticDiv > div > span:nth-child(1)')
        time.sleep(2)

        self.until_click_no_next_page_by_partial_link_text(nextpagesetup=NextPageLinkTextSetup(link_text="下一页", main_pagefunc=PageFunc(func=self.get_shop_info)))

    def run_spider(self):
        try:

            self.get_shop_info_list()
        except Exception as e:
            self.error_log(e=str(e))