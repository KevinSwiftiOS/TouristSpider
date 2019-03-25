# -*- coding:utf-8 -*-

from spider.driver.travel.core.traveldriver import TravelDriver
from spider.driver.base.page import Page,NextPageCssSelectorSetup,PageFunc
from spider.driver.base.page import Page,NextPageCssSelectorSetup,PageFunc,NextPageLinkTextSetup
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
    #数据库中保存进一位小数


    saveTo =  round(float(_str[0:-1]) / 100 * 5,1)
    return str(saveTo)
def get_shop_feature(self,_str):
    return ""
def get_shop_rate(self,_str):
    return ""
fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME,css_selector='div.theinfo.ticket.clearfix > a > dl > dt > p > span',is_info=True),
    Field(fieldname=FieldName.SHOP_PRICE, css_selector='div.theinfo.ticket.clearfix > a > div.priceinfo > span > em',is_info=False),
    #稍微有点问题
    Field(fieldname=FieldName.SHOP_URL,css_selector='div.theinfo.ticket.clearfix > a',attr='href',is_debug=True,is_info=False),
    #img还有些许问题
    Field(fieldname=FieldName.SHOP_IMG, css_selector='div.theinfo.ticket.clearfix > a > div.imgbox > div > img', attr='data-src',is_info=False),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector= 'div.theinfo.ticket.clearfix > a > dl > dd:nth-child(2)',is_info=False),
    #这里应该做一个转换
    Field(fieldname=FieldName.SHOP_GRADE,css_selector='div.theinfo.ticket.clearfix > a > div.priceinfo > div > p > i',filter_func=get_shop_grade,is_info=False),
    #正则表达式的使用有问题
    Field(fieldname=FieldName.SHOP_COMMENT_NUM,css_selector='div.theinfo.ticket.clearfix > a > div.priceinfo > div > p > span',is_info=False),
    #无shop_feature
    Field(fieldname=FieldName.SHOP_FEATURE, css_selector='',is_info=True,filter_func=get_shop_feature),
    Field(fieldname=FieldName.SHOP_RATE,css_selector='',is_info=True,filter_func=get_shop_rate)
)

fl_shop2 = Fieldlist(

)






page_shop_1 = Page(name='途牛景点店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#niuren_list > div.contentcontainer.clearfix > div.content_bottom > div.main.fl > div.thelist > ul > li',), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection),is_save=True)
page_shop_2 = Page()
page_shop_2 = Page(name='途牛景点店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector=' div.theinfo.ticket.clearfix > a > dl > dt > p > span'), mongodb=Mongodb(db=TravelDriver.db,collection=TravelDriver.shop_collection), is_save=True)


def get_comment_grade(self,_str):


    if _str == 'icon_manyi':
        return '5'
    elif _str =='icon_yiban':
        return '2.5'
    else:
        return '0'
def get_comment_time(self,_str):
    #时间格式统一为2018-12-08
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

def get_shop_name_search_key(self,_str):

    return self.shop_name_search_key(_str);





fl_comment1 = Fieldlist(
    Field(fieldname=FieldName.COMMENT_USER_NAME, css_selector='dl > dt > p.trav_name > a',is_info=True),
    Field(fieldname=FieldName.COMMENT_TIME, css_selector='dl > dd > dl > dt > a',filter_func=get_comment_time, is_info=True),
    Field(fieldname=FieldName.SHOP_NAME, css_selector='body > div.v2_body > div.v2_wrap.clearfix > div.v2_w1189 > div.v2_ticket_proinf.clearfix > div.v2_tp_text > div.v2_ct_title',is_isolated=True,is_info=True),
    Field(fieldname=FieldName.SHOP_NAME_SEARCH_KEY,
          css_selector='body > div.v2_body > div.v2_wrap.clearfix > div.v2_w1189 > div.v2_ticket_proinf.clearfix > div.v2_tp_text > div.v2_ct_title',filter_func=get_shop_name_search_key,
          is_isolated=True, is_info=True),
    Field(fieldname=FieldName.COMMENT_CONTENT, css_selector='dl > dd > div > p.comment_detail',is_info=False),
    #有问题
    Field(fieldname=FieldName.COMMENT_SCORE, css_selector='dl > dd > div > p.clists_words.clearfix > span:nth-child(1)',attr='class',filter_func=get_comment_grade, is_info=False),
    Field(fieldname=FieldName.COMMENT_YEAR, css_selector='dl > dd > dl > dt > a',
          filter_func=get_comment_year,
          is_info=False),
    Field(fieldname=FieldName.COMMENT_SEASON, css_selector='dl > dd > dl > dt > a',
          filter_func=get_comment_season,
          is_info=False),
    Field(fieldname=FieldName.COMMENT_MONTH, css_selector='dl > dd > dl > dt > a',
          filter_func=get_comment_month,
          is_info=False),
    Field(fieldname=FieldName.COMMENT_WEEK, css_selector='dl > dd > dl > dt > a',
          filter_func=get_comment_week,
          is_info=False),
    Field(fieldname=FieldName.DATA_REGION_SEARCH_KEY, css_selector='', filter_func=get_data_region_search_key,
          is_info=True),
)

page_comment_1 = Page(name='途牛景点评论列表', fieldlist=fl_comment1, listcssselector=ListCssSelector(list_css_selector='#remarkFlag > div.detail_infor > div > ul.v2_comment_lists.comment_lists > li'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)

class TuNiuSpotSpider(TravelDriver):

    def get_shop_comment(self):
        self.fast_new_page(url='http://www.baidu.com');
        shop_collcetion = Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection,
                                  host='10.1.17.15').get_collection()
        shop_name_url_list = list()
        for i in shop_collcetion.find(self.get_data_key()):
            if i.get('shop_url'):
                shop_name_url_list.append((i.get('shop_name'), i.get('shop_url')))
        for i in range(len(shop_name_url_list)):

            self.info_log(data='第%s个,%s' % (i + 1, shop_name_url_list[i][0]))
            #第一次打开的时候进行验证 后面都不需要

            while (True):
                    self.is_ready_by_proxy_ip()
                    self.switch_window_by_index(index=-1)
                    self.deal_with_failure_page()
                    self.fast_new_page(url=shop_name_url_list[i][1])
                    time.sleep(1)
                    self.switch_window_by_index(index=-1)  # 页面选择
                    if '验证中心' in self.driver.title:
                        self.info_log(data='关闭验证页面!!!')
                        self.close_curr_page()
                    else:

                        break
            self.until_click_no_next_page_by_css_selector(nextpagesetup=NextPageCssSelectorSetup(css_selector='#remark_page > a.page-next',stop_css_selector='#remark_page > a.page-next.hidden',
                                                                                                   main_pagefunc=PageFunc(
                                                                                                       func=self.from_page_get_data_list,
                                                                                                       page=page_comment_1)))
            self.close_curr_page()
    def get_shop_info_list(self):
        self.fast_new_page(url='http://www.baidu.com');
        self.fast_new_page(url='http://menpiao.tuniu.com/')
        time.sleep(2)
        self.until_send_text_by_css_selector(css_selector='#keyword-input', text=self.data_region)
        self.until_send_enter_by_css_selector(css_selector='#keyword-input')


        time.sleep(10)
        self.from_page_get_data_list(page=page_shop_1)
        # self.vertical_scroll_to()  # 滚动到页面底部
        # self.until_click_no_next_page_by_partial_link_text(
        #     nextpagesetup=NextPageLinkTextSetup(link_text="后一页", main_pagefunc=PageFunc(func=self.get_shop_info)))

    def run_spider(self):
        try:

            #self.get_shop_info_list()
            self.get_shop_comment()
        except Exception:
            self.error_log()
