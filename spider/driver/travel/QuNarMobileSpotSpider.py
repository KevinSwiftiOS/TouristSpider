from spider.driver.travel.core.traveldriver import TravelDriver
from spider.driver.base.page import Page,NextPageCssSelectorSetup,PageFunc
from spider.driver.base.field import Fieldlist,Field,FieldName
from spider.driver.base.tabsetup import TabSetup
from spider.driver.base.listcssselector import ListCssSelector
from spider.driver.base.page import Page,NextPageCssSelectorSetup,PageFunc,NextPageLinkTextSetup
from spider.driver.base.mongodb import Mongodb
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
import re
import time
import json
import math
import datetime
from pyquery import PyQuery
def get_comment_num(self,_str):
    return ""
def get_shop_address(self,_str):
    return ""
def get_shop_grade(self,_str):
    return ""
def get_shop_feature(self,_str):
    return ""
def get_shop_rate(self,_str):
    return ""
def get_comment_url(self,_str):
    return _str + "/comment"

def get_shop_name_search_key(self,_str):

    return self.shop_name_search_key(self.shop_name);
fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='div > div.mp-sight-info > a > div.mp-sight-detail > h3',is_info=True),
#\31 302 > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(1) > span:nth-child(2)
#\32 0808 > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(1) > span:nth-child(2)
    Field(fieldname=FieldName.SHOP_PRICE, css_selector='div > div.mp-sight-info > a > div.mp-sight-detail > div.mp-sight-pricecon > div.mp-sight-price > em',is_info=True),
    #稍微有点问题
    Field(fieldname=FieldName.SHOP_URL,css_selector='div > div.mp-sight-info > a',attr='href', is_debug=True,is_info=True),
    #img还有些许问题
#\33 6822720 > div:nth-child(1) > div
    Field(fieldname=FieldName.SHOP_IMG, css_selector='div > div.mp-sight-info > a > div.mp-sight-imgcon > img', attr='src', is_info=True),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector= 'div > div.mp-sight-info > a > div.mp-sight-detail > div.mp-sight-pricecon > div.mp-sight-location > span', is_info=True),
    #这里应该做一个转换
#\34 187 > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(2) > span:nth-child(1)
    Field(fieldname=FieldName.SHOP_GRADE,css_selector='div > div.mp-sight-info > a > div.mp-sight-detail > div.mp-sight-comments > span.mpf-starlevel > span.mpg-iconfont.mpf-starlevel-gain',attr='data-score', is_info=True),
    #正则表达式的使用有问题
    Field(fieldname=FieldName.SHOP_COMMENT_NUM,css_selector='div > div.mp-sight-info > a > div.mp-sight-detail > div.mp-sight-comments > span.mp-comments-totalnum', is_info=True),
    #无shop_feature

    Field(fieldname=FieldName.SHOP_FEATURE, css_selector='',filter_func=get_shop_feature, is_info=True),

    Field(fieldname=FieldName.SHOP_RATE,css_selector='',filter_func=get_shop_rate, is_info=True),
)
page_shop_1 = Page(name='去哪儿景点店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#main-page > div.mp-main > div:nth-child(2) > ul > li'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection), is_save=True)

fl_shop2 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='#main-page > div.mp-main > div.mp-headfigure > div.mp-headfeagure-info > div'),
    Field(fieldname=FieldName.SHOP_COMMENT_URL,css_selector='#main-page > div.mp-main > div.mp-baseinfo > div.mpg-flexbox.mp-flex-card > div:nth-child(1) > a',attr='href', is_info=True)
)

page_shop_2 = Page(name='去哪儿景点店铺详情页面',fieldlist=fl_shop2)


def get_shop_name(self,_str):
    return self.shop_name
def get_comment_grade(self,_str):
    witdth = re.findall(r'[\d]{1,3}',_str)[0]
    return str(float(witdth) / 100 * 5)

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

    return self.shop_name_search_key(self.shop_name);
fl_comment1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='#main-page > div.mp-comment-mpcon > div.mpm-comment-head > div > div > span.mp-sight-score',filter_func=get_shop_name, is_info=True,is_isolated=True),
Field(fieldname=FieldName.SHOP_NAME_SEARCH_KEY, css_selector='#main-page > div.mp-comment-mpcon > div.mpm-comment-head > div > div > span.mp-sight-score',filter_func=get_shop_name_search_key, is_info=True,is_isolated=True),
#app > div > div.poi-rate-container > div:nth-child(2) > div.rate-content-container > div
#app > div > div.poi-rate-container > div:nth-child(7) > div.rate-content-container > div
#main-page > div.mp-comment-mpcon > div:nth-child(3) > div.mpm-comment-info-outer.mpf-border-top > div > span:nth-child(1)
    Field(fieldname=FieldName.COMMENT_CONTENT, css_selector='p', is_info=True),
    Field(fieldname=FieldName.COMMENT_USER_NAME,
          css_selector='div.mpm-comment-info-outer.mpf-border-top > div > span:nth-child(1)', is_info=True),
    #comment_grade有待商榷
    Field(fieldname=FieldName.COMMENT_SCORE, css_selector='div.mpm-comment-info-outer.mpf-border-top > div > span.mpf-starlevel.comment-starwidth > i.mpg-iconfont.mpf-starlevel-gain', attr='style',filter_func=get_comment_grade, is_info=False),
    Field(fieldname=FieldName.COMMENT_TIME, css_selector=' div.mpm-comment-info-outer.mpf-border-top > div > span:nth-child(4)', is_info=True),
    Field(fieldname=FieldName.COMMENT_YEAR,
          css_selector=' div.mpm-comment-info-outer.mpf-border-top > div > span:nth-child(4)',
          filter_func=get_comment_year,
          is_info=False),
    Field(fieldname=FieldName.COMMENT_SEASON,
          css_selector=' div.mpm-comment-info-outer.mpf-border-top > div > span:nth-child(4)',
          filter_func=get_comment_season,
          is_info=False),
    Field(fieldname=FieldName.COMMENT_MONTH,
          css_selector=' div.mpm-comment-info-outer.mpf-border-top > div > span:nth-child(4)',
          filter_func=get_comment_month,
          is_info=False),
    Field(fieldname=FieldName.COMMENT_WEEK,
          css_selector=' div.mpm-comment-info-outer.mpf-border-top > div > span:nth-child(4)',
          filter_func=get_comment_week,
          is_info=False),
    Field(fieldname=FieldName.DATA_REGION_SEARCH_KEY,

          css_selector='',
          filter_func=get_data_region_search_key,
          is_info=True),
)
page_comment_1 = Page(name='去哪儿景点店铺评论列表页面', fieldlist=fl_comment1, listcssselector=ListCssSelector(list_css_selector='#main-page > div.mp-comment-mpcon > div'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)





















class QunarMobileSpotSpider(TravelDriver):

    def get_shop_info_list(self):
        self.fast_get_page(url='http://touch.piao.qunar.com/touch/list_%E5%8C%97%E4%BA%AC.html?isSearch=1&cityName=%E5%8C%97%E4%BA%AC')
        time.sleep(5)
        self.until_scroll_to_center_send_text_by_css_selector(css_selector='#search-input-bind',text=self.data_region)
        #睡得久一点 让整个页面都加载出来
        time.sleep(4)
        self.fast_click_page_by_css_selector(click_css_selector='#search-form-submit')
        time.sleep(8)
        #shop_data_list = self.from_page_get_data_list(page=page_shop_1)
        self.until_click_no_next_page_by_partial_link_text(
            nextpagesetup=NextPageLinkTextSetup(link_text='下一页', pause_time=5,
                                                main_pagefunc=PageFunc(func=self.from_page_get_data_list,
                                                                       page=page_shop_1)))
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
       shop_collcetion = Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection,
                                 host='localhost').get_collection()
       shop_name_url_list = list()
       for i in shop_collcetion.find(self.get_data_key()):
           if i.get('shop_comment_url'):
               shop_name_url_list.append((i.get('shop_name'), i.get('shop_comment_url')))
       self.fast_new_page(url="https://www.baidu.com");
       for i in range(len(shop_name_url_list)):
           # 可能会有反爬
           self.info_log(data='第%s个,%s' % (i + 1, shop_name_url_list[i][0]))
           self.shop_name = shop_name_url_list[i][0]
           self.fast_new_page(url=shop_name_url_list[i][1])
           time.sleep(5)

           # main-page > header > h2 > div:nth-child(2)
           try:
               #查看是否有顶部按钮 有就点击

              #若第一个不是点评 则需要点击第二个
             print(10102);
             print(self.driver.find_element_by_css_selector(css_selector='#main-page > header > h2 > div:nth-child(1)' ).text)
             if(self.driver.find_element_by_css_selector(css_selector='#main-page > header > h2 > div:nth-child(1)' ).text!= '点评'):
              self.fast_click_same_page_by_css_selector(click_css_selector='#main-page > header > h2 > div:nth-child(2)')


             time.sleep(6)
           except Exception as e:
                print(111)
           #点击最新的
           try:
            new = self.driver.find_element_by_xpath('//li[@data-tagtype="44"]')

            ActionChains(self.driver).click(new).perform()

            time.sleep(5)
           except Exception as e:
               print(222)

           #向下进行滚动
           try:
             button = self.driver.find_element_by_css_selector(
                   css_selector='#main-page > div.mp-comment-mpcon > div.mp-addcomment.mp-border-top > a > div')

             Action = TouchActions(self.driver)
             Action.scroll_from_element(on_element=button,xoffset=0,yoffset=int(30000)).perform()
             time.sleep(5)
           except Exception as e:
               print(333)
           self.fast_click_same_page_by_css_selector(click_css_selector='#main-page > div.mp-gotop > div')
           time.sleep(6)
           comment_data_list = self.from_page_get_data_list(page=page_comment_1)
           self.close_curr_page()



    def run_spider(self):
       #self.get_shop_info_list()
       #self.get_shop_detail()
       self.get_comment_info_list()