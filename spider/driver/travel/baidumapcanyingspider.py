# -*- coding:utf-8 -*-

from spider.driver.travel.core.traveldriver import TravelDriver
from spider.driver.base.page import Page,NextPageCssSelectorSetup,PageFunc,NextPageLinkTextSetup
from spider.driver.base.field import Fieldlist,Field,FieldName
from spider.driver.base.tabsetup import TabSetup
from spider.driver.base.listcssselector import ListCssSelector
from spider.driver.base.mongodb import Mongodb
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
import re
import time
import json
from pyquery import PyQuery
import xmltodict
import math
import datetime
def get_zero(self,_str):
    return 0.0
def get_shop_area(self,_str):
    return '千岛湖东北湖区';
def get_baidu_spider_step(self,_str):
    return "2";

fl_shop1 = Fieldlist(
#card-56 > div > ul > li:nth-child(3) > div.cf.mb_5 > div.ml_30.mr_85 > div:nth-child(1) > span > a
#card-56 > div > ul > li.search-item.base-item > div.cf > div.ml_30.mr_90 > div:nth-child(1) > span:nth-child(1) > a
    Field(fieldname=FieldName.SHOP_NAME,css_selector='div.cf > div.ml_30 > div:nth-child(1) > span > a',is_info=True),
#card-56 > div > ul > li.search-item.base-item > div.cf > div.ml_30.mr_90 > div.row.addr > span
#card-56 > div > ul > li:nth-child(3) > div.cf.mb_5 > div.ml_30.mr_85 > div.row.addr > span
    Field(fieldname=FieldName.SHOP_ADDRESS,css_selector='div.cf > div.ml_30 > div.row.addr > span',is_info=True),
    Field(fieldname=FieldName.SHOP_IMG, css_selector='div.cf > div.col-r > div.img-wrap > a > img', attr='src',is_info=True),
    Field(fieldname=FieldName.SHOP_LNG, css_selector='',filter_func=get_zero, is_info=True),
    Field(fieldname=FieldName.SHOP_LAT, css_selector='',filter_func=get_zero, is_info=True),
    Field(fieldname=FieldName.SHOP_AREA,css_selector='',filter_func=get_shop_area,is_info=True),
    Field(fieldname=FieldName.BAIDU_SPIDER_STEP,css_selector='',filter_func=get_baidu_spider_step,is_info=True)
)

def get_shop_name(self,_str):
    self.shop_name = _str;
    return _str;

fl_shop2 = Fieldlist(

#phoenix_dom_3_0 > div > div.head-wrapper.c-title.c-color.c-flexbox.c-line-bottom > div.left > span
#phoenix_dom_3_1 > div > div.head-wrapper.c-title.c-color.c-flexbox.c-line-bottom > div.left > span
Field(fieldname=FieldName.SHOP_COMMENT_NUM, css_selector='div.card-box.special2-box.c-container >div.head-wrapper.c-title.c-color.c-flexbox.c-line-bottom > div.left > span',is_info=True),
Field(fieldname=FieldName.SHOP_SCORE, css_selector='span.left-header-visit',is_info=True),
Field(fieldname=FieldName.SHOP_CATEGORY_NAME,css_selector='span.left-header-stdtag',is_info=True),
    Field(fieldname=FieldName.SHOP_PRICE,css_selector='span.left-header-reference-price',is_info=True),
    Field(fieldname=FieldName.SHOP_NAME_SEARCH_KEY,css_selector='div.generalHead-left-header-title > span',filter_func=get_shop_name,is_info=True),
Field(fieldname=FieldName.SHOP_PHONE,css_selector='#generalinfo > div.generalInfo-address-telnum > div.generalInfo-telnum.item > span.clampword.generalInfo-telnum-text',is_info=True)
#generalheader > div.generalHead-left-header.animation-common > div.generalHead-left-header-title > span
)
#card-1 > div > ul > li:nth-child(1) > div.cf.mb_5 > div.ml_30.mr_85 > div:nth-child(2)
page_shop_1 = Page(name='百度餐饮店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='ul.poilist > li'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection),is_save=True)

page_shop_2 = Page(name='百度餐饮店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector='div.cf > div.ml_30 > div:nth-child(1) > span > a'),  mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection),is_save=True)


def get_shop_lng(self,_str):

    doc = _str.split(',')
    #再某一个经度范围内

    if(float(doc[0]) <= 119.243071 and float(doc[0]) >= 118.650908):

     return  doc[0]
    else:

     return 119.051491
def get_shop_lat(self,_str):
    doc = _str.split(',')
    if (float(doc[1]) <= 29.767007 and float(doc[1]) >= 29.366916):

        return doc[1]
    else:

        return 29.61644
address_shop2_field = Fieldlist(


    Field(fieldname=FieldName.SHOP_LNG,
          css_selector='#pointInput',attr='data-clipboard-text', filter_func=get_shop_lng,
          is_info=True),
    Field(fieldname=FieldName.SHOP_LAT,
          css_selector='#pointInput',attr='data-clipboard-text', filter_func=get_shop_lat,
          is_info=True)
)
address_shop_2 = Page(name='百度地图获取经纬度页面', fieldlist=address_shop2_field,is_save=True)
def get_comment_shop_name(self,_str):
    return self.shop_name;


def get_comment_time(self,_str):
    if ('年' in _str):
        year = _str.split('年')[0];
        month_and_day = _str.split('年')[1];

        month = month_and_day.split('月')[0];
        day = month_and_day.split('月')[1].split('日')[0];
        month = month.zfill(2);
        day = day.zfill(2);
        return str(year) + "-" + str(month) + "-" + str(day);
    else:
        return _str;

def get_comment_year(self,_str):
    if ('年' in _str):
        year = _str.split('年')[0];
        month_and_day = _str.split('年')[1];

        month = month_and_day.split('月')[0];
        day = month_and_day.split('月')[1].split('日')[0];
        month = month.zfill(2);
        day = day.zfill(2);
        in_db_str =  str(year) + "-" + str(month) + "-" + str(day);
    else:
        in_db_str = _str;

    return in_db_str[0:4];

def get_comment_season(self, _str):
    if ('年' in _str):
        year = _str.split('年')[0];
        month_and_day = _str.split('年')[1];

        month = month_and_day.split('月')[0];
        day = month_and_day.split('月')[1].split('日')[0];
        month = month.zfill(2);
        day = day.zfill(2);
        in_db_str =  str(year) + "-" + str(month) + "-" + str(day);
    else:
        in_db_str = _str;
    time = in_db_str[0:10];
    times = time.split('-');

    month = int(times[1])

    seasons = ['01', '02', '03', '04'];
    if (month % 3 == 0):
        return (times[0] + '-' + seasons[int(month / 3) - 1]);
    else:
        index = int(math.floor(month / 3));
        return (times[0] + '-' + seasons[index]);
def get_comment_month(self, _str):
    if ('年' in _str):
        year = _str.split('年')[0];
        month_and_day = _str.split('年')[1];

        month = month_and_day.split('月')[0];
        day = month_and_day.split('月')[1].split('日')[0];
        month = month.zfill(2);
        day = day.zfill(2);
        in_db_str = str(year) + "-" + str(month) + "-" + str(day);
    else:
        in_db_str = _str;
    return in_db_str[0:7];
def get_comment_week(self, _str):
    if ('年' in _str):
        year = _str.split('年')[0];
        month_and_day = _str.split('年')[1];

        month = month_and_day.split('月')[0];
        day = month_and_day.split('月')[1].split('日')[0];
        month = month.zfill(2);
        day = day.zfill(2);
        in_db_str = str(year) + "-" + str(month) + "-" + str(day);
    else:
        in_db_str = _str;
    time = in_db_str[0:10]
    times = in_db_str.split('-');
    return (times[0] + '-' + str(datetime.date(int(times[0]), int(times[1]), int(times[2])).isocalendar()[1]).zfill(2))
#
# def get_data_region_search_key(self,_str):
def get_comment_score(self,_str):
    cnt = 0;

    pq = PyQuery(_str)
    for i in range(0, 5):
        percent_on = pq('.star' + str(i) + '-percent')
        if (percent_on.attr('style') == 'width: 100%'):
            cnt += 1;

    return str(cnt);

fl_comment1 = Fieldlist(
    Field(fieldname=FieldName.COMMENT_USER_NAME,css_selector='div.comment-main.c-flexitem1.c-auxiliary > div.c-main.c-flexbox',is_info=True),
    Field(fieldname=FieldName.SHOP_NAME,css_selector='',filter_func=get_comment_shop_name,is_info=True),

    Field(fieldname=FieldName.COMMENT_TIME, css_selector='div.comment-main.c-flexitem1.c-auxiliary > div.item-score.c-flexbox > div.c-annotation.c-color-auxi',filter_func=get_comment_time,is_info=True),
    Field(fieldname=FieldName.COMMENT_CONTENT, css_selector='div.comment-main.c-flexitem1.c-auxiliary > div.comment-text > p', attr='innerHTML',is_info=True),
#phoenix_dom_1002 > div > div.commit-container > div.content-container > ul.commit-wrapper-0 > li:nth-child(1) > div.comment-main.c-flexitem1.c-auxiliary > div.item-score.c-flexbox > div:nth-child(1) > div
#phoenix_dom_1002 > div > div.commit-container > div.content-container > ul.commit-wrapper-0 > li:nth-child(8) > div.comment-main.c-flexitem1.c-auxiliary > div.item-score.c-flexbox > div:nth-child(1) > div
#phoenix_dom_1000 > div > div.commit-container > div.content-container > ul.commit-wrapper-0 > li:nth-child(1) > div.comment-main.c-flexitem1.c-auxiliary > div.item-score.c-flexbox > div:nth-child(1) > div

    Field(fieldname=FieldName.COMMENT_SCORE,css_selector='div.comment-main.c-flexitem1.c-auxiliary > div.item-score.c-flexbox > div:nth-child(1) > div',attr='innerHTML',filter_func=get_comment_score, is_info=True),
    Field(fieldname=FieldName.COMMENT_YEAR, css_selector='div.comment-main.c-flexitem1.c-auxiliary > div.item-score.c-flexbox > div.c-annotation.c-color-auxi',
          filter_func=get_comment_year,
          is_info=True),
    Field(fieldname=FieldName.COMMENT_SEASON, css_selector='div.comment-main.c-flexitem1.c-auxiliary > div.item-score.c-flexbox > div.c-annotation.c-color-auxi',
          filter_func=get_comment_season,
          is_info=True),
    Field(fieldname=FieldName.COMMENT_MONTH, css_selector='div.comment-main.c-flexitem1.c-auxiliary > div.item-score.c-flexbox > div.c-annotation.c-color-auxi',
          filter_func=get_comment_month,
          is_info=True),
    Field(fieldname=FieldName.COMMENT_WEEK, css_selector='div.comment-main.c-flexitem1.c-auxiliary > div.item-score.c-flexbox > div.c-annotation.c-color-auxi',
          filter_func=get_comment_week,
          is_info=True),
    Field(fieldname=FieldName.SHOP_AREA, css_selector='', filter_func=get_shop_area, is_info=True),
    Field(fieldname=FieldName.BAIDU_SPIDER_STEP, css_selector='', filter_func=get_baidu_spider_step, is_info=True)

)

page_comment_1 = Page(name='百度地图餐饮评论列表', fieldlist=fl_comment1,listcssselector=ListCssSelector(list_css_selector='ul.commit-wrapper-0 > li'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)



class BaiduMapCanYingSpider(TravelDriver):

    def shop_detail_page_unfold(self):
        try:
            for i in self.until_presence_of_all_elements_located_by_partial_link_text(link_text='展开', timeout=1):
                self.scroll_to_center(ele=i)
                i.click()
        except Exception:
            pass
    def get_comment(self):
        try:
            self.fast_click_first_item_same_page_by_partial_link_text(link_text='查看全部')
            time.sleep(5)
            button = self.driver.find_element_by_css_selector(
                css_selector='ul.commit-wrapper-0 > li:nth-child(1)')

            Action = TouchActions(self.driver)
            Action.scroll_from_element(on_element=button, xoffset=0, yoffset=int(10000)).perform()
            Action.scroll_from_element(on_element=button, xoffset=0, yoffset=int(0)).perform()
            time.sleep(5)
            self.from_page_get_data_list(page=page_comment_1)
        except Exception:
            print("没有评论")






        time.sleep(5)
        try:
         self.fast_click_page_by_css_selector(click_css_selector='li.card.status-return.fold')
        except Exception as e:
            print("无元素")
    def get_shop_info(self):
        try:

            shop_data_list = self.from_page_get_data_list(page=page_shop_1)
            # root > div > div > div > div > div:nth-child(3) > div.main-bd > div > div:nth-child(5) > div.detail-left > div.content-wrapper.clearfix > ul.pkg_page > a.down
            # root > div > div > div > div > div:nth-child(3) > div.main-bd > div > div:nth-child(5) > div.detail-left > div.content-wrapper.clearfix > ul.pkg_page > a.down.disabled.nocurrent
            # nextpagesetup = NextPageCssSelectorSetup(css_selector='div.detail-left > div.content-wrapper.clearfix > ul.pkg_page > a.down', stop_css_selector='div.detail-left > div.content-wrapper.clearfix > ul.pkg_page > a.down.disabled.nocurrent', page=page_comment_1, pause_time=2)
            extra_pagefunc = PageFunc(func=self.get_comment)
            self.from_page_add_data_to_data_list(page=page_shop_2, pre_page=page_shop_1, data_list=shop_data_list,extra_pagefunc=extra_pagefunc)
        except Exception as e:
            self.error_log(e=str(e))

    def get_shop_info_list(self):
        self.driver.get('https://www.baidu.com')
        self.fast_new_page(url='http://map.baidu.com', is_scroll_to_bottom=False)
        #self.driver.refresh()
        # self.until_scroll_to_center_send_text_by_css_selector(css_selector="#sole-input", text='千岛湖附近美食')
        # time.sleep(3)
        # self.until_scroll_to_center_send_enter_by_css_selector(css_selector='#sole-input')
        time.sleep(20)
        # poi_page > p > span:nth-child(5) > a
        self.until_click_no_next_page_by_partial_link_text(nextpagesetup=NextPageLinkTextSetup(link_text='下一页',main_pagefunc=PageFunc(func=self.get_shop_info)))
        # NextPageCssSelectorSetup(css_selector='#poi_page > p > span:nth-child(5) > a',
        #                          stop_css_selector='#poi_page > p > span:nth-child(5) > a.hidden',
    def get_shop_address(self):

        #self.fast_new_page(url="http://www.baidu.com");
        self.fast_new_page(url='http://api.map.baidu.com/lbsapi/getpoint/index.html');
        self.fast_click_first_item_same_page_by_partial_link_text(link_text='更换城市')
        self.until_scroll_to_center_send_text_by_css_selector(css_selector='#selCityInput', text='淳安')
        time.sleep(2)
        self.fast_click_same_page_by_css_selector(click_css_selector='#selCityButton')
        time.sleep(2)
        shop_collcetion = Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection,
                                  host='localhost').get_collection()

        shop_name_url_list = list()

        for i in shop_collcetion.find(self.get_data_key()):

            if i.get('shop_name'):
                shop_name_url_list.append((i.get('shop_name'),i.get('shop_address')))
        print(len(shop_name_url_list))
        for i in range(len(shop_name_url_list)):
            #self.fast_new_page(url='https://www.baidu.com');

            self.info_log(data='第%s个,%s' % (i + 1, shop_name_url_list[i][0]))

            self.fast_click_first_item_same_page_by_partial_link_text(link_text='更换城市')
            self.until_scroll_to_center_send_text_by_css_selector(css_selector='#selCityInput', text='淳安')
            time.sleep(2)
            self.fast_click_same_page_by_css_selector(click_css_selector='#selCityButton')
            time.sleep(2)

            # while (True):
            #     self.is_ready_by_proxy_ip()
            #     self.switch_window_by_index(index=-1)
            #     self.deal_with_failure_page()
            #     self.fast_new_page(url=shop_name_url_list[i][1])
            #     time.sleep(1)
            #     self.switch_window_by_index(index=-1)  # 页面选择
            #     if '请求数据错误' in self.driver.title:
            #         self.info_log(data='关闭验证页面!!!')
            #         self.close_curr_page()
            #     else:
            #         break

            self.until_scroll_to_center_send_text_by_css_selector(css_selector='#localvalue', text = shop_name_url_list[i][1])
            time.sleep(2)
            self.fast_click_same_page_by_css_selector(click_css_selector='#localsearch')
            time.sleep(2)
            try:
                self.driver.find_element_by_css_selector(css_selector='#no_0 > a').click()
                time.sleep(2)
            # while (True):
            #     self.is_ready_by_proxy_ip()
            #     self.switch_window_by_index(index=-1)
            #     self.deal_with_failure_page()
            #     self.fast_new_page(url=shop_name_url_list[i][1])
            #     time.sleep(1)
            #     self.switch_window_by_index(index=-1)  # 页面选择
            #     if '请求数据错误' in self.driver.title:
            #         self.info_log(data='关闭验证页面!!!')
            #         self.close_curr_page()
            #     else:
            #         break

                data = self.from_fieldlist_get_data(page=address_shop_2)
                self.update_data_to_mongodb(shop_collcetion,
                                        self.merge_dict(self.get_data_key(),
                                                        {FieldName.SHOP_NAME: shop_name_url_list[i][0]}), data)
            except Exception:
                print("该地址无经纬度")



    def run_spider(self):
        try:
            #self.data_region_search_key = self.get_data_region_search_key()
            self.get_shop_info_list()
            #self.get_shop_address()


        except Exception as e:
            self.error_log(e=str(e))