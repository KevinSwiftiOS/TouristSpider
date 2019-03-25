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
def get_shop_url(self,_str):

    matchObj = re.search(r'http.*html', _str, re.M|re.I)

    return str(matchObj.group())
def get_shop_rate(self,_str):
    return ""
fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME,css_selector=' dl > dt > a',is_debug=True),

    Field(fieldname=FieldName.SHOP_URL,css_selector='dl > dt > a',attr='onclick',filter_func=get_shop_url, is_info=True),
    Field(fieldname=FieldName.SHOP_IMG, css_selector=' a > img', attr='src',is_info=True),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='dl > dd.proInfo-address > i',
          is_info=True),


    Field(fieldname=FieldName.SHOP_COMMENT_NUM,css_selector='  div > div:nth-child(2) > ul > li:nth-child(2) > a', is_info=True),

    Field(fieldname=FieldName.SHOP_FEATURE, css_selector=' dl > dd:nth-child(4)',is_info=True),
    Field(fieldname=FieldName.SHOP_PRICE, css_selector='div > div.priceInfo-price > dfn > span', is_info=True),
Field(fieldname=FieldName.SHOP_GRADE, css_selector='div > div:nth-child(2) > ul > li:nth-child(1) > a > b',filter_func=get_shop_grade,  is_info=True),
Field(fieldname=FieldName.SHOP_RATE, css_selector='',filter_func=get_shop_rate,  is_info=True),
)

fl_shop2 = Fieldlist(

)
page_shop_1 = Page(name='驴妈妈景点店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#mainHotelLeft > div',), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection),is_save=True)
page_shop_2 = Page()
page_shop_2 = Page(name='驴妈妈景点店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector='dl > dt > a'), mongodb=Mongodb(db=TravelDriver.db,collection=TravelDriver.shop_collection))



def get_comment_user_name(self, _str):
    return _str.split(' ')[0]

def get_comment_time(self, _str):
    return re.findall(r'([\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2})',_str)[0]
def get_comment_grade(self,_str):

    return str(_str[-1])
fl_comment1 = Fieldlist(
    Field(fieldname=FieldName.COMMENT_USER_NAME, css_selector='div.com-userinfo > p > a:nth-child(1)',is_info=True),
    Field(fieldname=FieldName.COMMENT_TIME, css_selector='div.com-userinfo > p > em', is_info=True),
    Field(fieldname=FieldName.SHOP_NAME, css_selector='body > div.body_bg > div > div.detailHeader > div.header-titInfo.clearfix > div.titInfo-topL > div.titInfo-tit.clearfix > h1', is_isolated=True,is_info=True),
    Field(fieldname=FieldName.COMMENT_CONTENT, css_selector='div.ufeed-content',is_info=True),
    #有问题
    Field(fieldname=FieldName.COMMENT_SCORE, css_selector='div.ufeed-info > p > span.ufeed-level > i',attr='data-level',is_info=True),
)

page_comment_1 = Page(name='驴妈妈酒店评论列表', fieldlist=fl_comment1, listcssselector=ListCssSelector(list_css_selector='#allCmtComment > div'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)


class LvmamaHotelSpider(TravelDriver):



    def get_shop_info(self):
        try:
            shop_data_list = self.from_page_get_data_list(page=page_shop_1)

            nextpagesetup = NextPageCssSelectorSetup(
                css_selector='#allCmtComment > div.paging.orangestyle > div > a.nextpage'
                             ,
                stop_css_selector='#allCmtComment > div.paging.orangestyle > div > a.nextpage.hidden',
                page=page_comment_1, pause_time=2)
            extra_pagefunc = PageFunc(func=self.get_newest_comment_data_by_css_selector, nextpagesetup=nextpagesetup)
            self.from_page_add_data_to_data_list(page=page_shop_2, pre_page=page_shop_1, data_list=shop_data_list,extra_pagefunc=extra_pagefunc
                                                )
        except Exception as e:
            self.error_log(e=str(e))
    def get_shop_info_list(self):
        self.fast_get_page('http://s.lvmama.com/hotel/U69C20180919O20180920?mdd=%E8%AF%B7%E8%BE%93%E5%85%A5%E7%9B%AE%E7%9A%84%E5%9C%B0#list', is_max=False)
        time.sleep(2)

        city = self.get_city_from_region_CHN(self.data_region)
        self.until_scroll_to_center_send_enter_by_css_selector(css_selector='#js_destination',text=city)
        self.until_scroll_to_center_send_enter_by_css_selector(css_selector='#js_keyword', text=self.data_region)
        time.sleep(1)
       # self.until_send_enter_by_css_selector(css_selector='#js_keyword')
        self.fast_click_page_by_css_selector('#btn_search')
        # self.fast_click_page_by_css_selector('body > div.lv-ban > div.lv_s_all > div > div:nth-child(1) > div.lv_s_search > span')
        #这里根据字段的不同重新进行编写
        #千岛湖
        # self.fast_click_page_by_css_selector('#search-params > div.search-nav-box.clearfix > p > a:nth-child(7)')
        #千岛湖森林氧吧
        # self.fast_click_page_by_css_selector('body > div.banWrap.pr > div.hotelSeach.fix.pa.yh.f14 > div.hotelSeachbtn.fl.pr.tc.f18')
        # self.fast_click_page_by_css_selector('#_j_mfw_search_main > div.s-nav > div > div > a:nth-child(4)')
        time.sleep(1)

        #self.vertical_scroll_to()  # 滚动到页面底部
        self.until_click_no_next_page_by_partial_link_text(
            nextpagesetup=NextPageLinkTextSetup(link_text="下一页", main_pagefunc=PageFunc(func=self.get_shop_info)))
    def run_spider(self):
        try:
            self.get_shop_info_list()
        except Exception:
            self.error_log()
