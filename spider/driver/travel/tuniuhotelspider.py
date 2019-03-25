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
def get_shop_grade(self,_str):
    saveTo = round(float(_str[0:-1]) / 100 * 5, 1)
    return str(saveTo)

def get_shop_grade(self,_str):

    groups = re.findall(r'[\d]{1,3}', _str)

    saveTo = (float(groups[0]) / 100 * 5)

    return str(saveTo)
def get_shop_rate(self,_str):
    return ""
fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME,css_selector='div > div.hotel-info.fl > div.nameAndIcon > a',is_debug=True),

    Field(fieldname=FieldName.SHOP_URL,css_selector='div > div.hotel-info.fl > div.nameAndIcon > a',attr='href', is_info=True),
    Field(fieldname=FieldName.SHOP_IMG, css_selector='div > div.hotel-logo.fl.has-more-snapshots > img', attr='src',is_info=True),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='div > div.hotel-info.fl > div.addressInfo',
          is_info=True),

  Field(fieldname=FieldName.SHOP_GRADE,css_selector='div > div.hotel-brief.fl > div.satisfaction > span.highlight',is_info=True),
    #正则表达式不一样
#mainHotelLeft > div:nth-child(2) > div > div:nth-child(2) > ul > li:nth-child(2)
    Field(fieldname=FieldName.SHOP_COMMENT_NUM,css_selector='div > div.hotel-brief.fl > div.comment > a > span', is_info=True),

    Field(fieldname=FieldName.SHOP_FEATURE, css_selector='div > div.hotel-info.fl > div.nameAndIcon > span.decorate_year',is_info=True),
    Field(fieldname=FieldName.SHOP_PRICE, css_selector='div > div.hotel-brief.fl > div.startPrice > span.digit', is_info=True),
    Field(fieldname=FieldName.SHOP_RATE, css_selector='',filter_func=get_shop_rate,
          is_info=True),

)

fl_shop2 = Fieldlist()

page_shop_1 = Page(name='途牛酒店店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#main > div.hotel-list > div'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection),is_save=True)
page_shop_2 = Page()
page_shop_2 = Page(name='途牛酒店店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector='div > div.hotel-info.fl > div.nameAndIcon > a'), mongodb=Mongodb(db=TravelDriver.db,collection=TravelDriver.shop_collection))



def get_comment_user_name(self, _str):
    return _str.split(' ')[0]

def get_comment_time(self, _str):
    return re.findall(r'([\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2})',_str)[0]
def get_comment_grade(self,_str):
    #判断如果含有好 高
    if ('好' in _str) and ('但是' in _str) == False:
        return  str("5.0")
    elif ('好' in _str) and ('但是' in _str) == True:
        return  str("0.0")
    elif ('差' in _str) and ('但是' in _str) == False:
        return str("0.0")
    elif ('差' in _str) and ('但是' in _str) == True:
        return str("5.0")
    else:
        return str("2.5")
fl_comment1 = Fieldlist(

    Field(fieldname=FieldName.COMMENT_USER_NAME, css_selector='div.a1 > div.b2',is_info=True),
    Field(fieldname=FieldName.COMMENT_TIME, css_selector='div.a2 > div.b4 > span', is_info=True),
    Field(fieldname=FieldName.SHOP_NAME, css_selector='#hotelName', is_isolated=True,is_info=True),
    Field(fieldname=FieldName.COMMENT_CONTENT, css_selector='div.a2 > div.b2 > p',is_info=True),
    #有问题
    Field(fieldname=FieldName.COMMENT_SCORE, css_selector='div.a2 > div.b2 > p',filter_func=get_comment_grade,is_info=True),
)

page_comment_1 = Page(name='途牛酒店评论列表', fieldlist=fl_comment1, listcssselector=ListCssSelector(list_css_selector='#hotelUserComment > div.hotel_user_remark > div.user_remark_datail > div'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)


class TuNiuHotelSpider(TravelDriver):

        # try:
        #     for i in self.until_presence_of_all_elements_located_by_partial_link_text(link_text='展开', timeout=1):
        #         self.scroll_to_center(ele=i)
        #         i.click()
        # except Exception:
        #     pass

    def get_shop_info(self):
        try:
            print(1234567890)
            shop_data_list = self.from_page_get_data_list(page=page_shop_1)

            nextpagesetup = NextPageCssSelectorSetup(
                css_selector='#remarksPage > a.page-next'
                             ,
                stop_css_selector='#remarksPage > a.page-next.hidden',
                page=page_comment_1, pause_time=2)
            extra_pagefunc = PageFunc(func=self.get_newest_comment_data_by_css_selector, nextpagesetup=nextpagesetup)
            self.from_page_add_data_to_data_list(page=page_shop_2, pre_page=page_shop_1, data_list=shop_data_list,extra_pagefunc=extra_pagefunc
                                                )
        except Exception as e:
            print(0000000000000000)
            self.error_log(e=str(e))


    def get_shop_info_list(self):
            self.fast_get_page(url='http://hotel.tuniu.com/', is_scroll_to_bottom=False)

            city = self.get_city_from_region_CHN(self.data_region)

            self.until_send_text_by_css_selector(css_selector='#txtCity',text=city)
            time.sleep(5)
            self.fast_click_page_by_css_selector('#search_hotel')
            self.until_send_text_by_css_selector(css_selector='#keyWord', text=self.data_region)
            time.sleep(5)
            self.fast_click_page_by_css_selector('#search_hotel')
            # self.fast_click_page_by_css_selector(
            #     '#topContainer > div > div > div.box.clearfix.topnav.common > a:nth-child(14)',is_scroll_to_bottom=True)


            time.sleep(10)


            self.until_click_no_next_page_by_css_selector(
                nextpagesetup=NextPageCssSelectorSetup(css_selector='#main > div.pagination.clearfix > div > span.next',stop_css_selector='span.next > i.hidden',
                                                       main_pagefunc=PageFunc(func=self.get_shop_info)))
            # self.until_click_no_next_page_by_partial_link_text(nextpagesetup=NextPageLinkTextSetup(
            #     link_text=">",main_pagefunc=PageFunc(func=self.get_shop_info)
            # ))
    def run_spider(self):
        try:
            self.get_shop_info_list()
        except Exception:
            self.error_log()