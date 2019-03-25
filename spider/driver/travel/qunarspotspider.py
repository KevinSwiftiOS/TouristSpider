# -*- coding:utf-8 -*-
from spider.driver.travel.core.traveldriver import TravelDriver
from spider.driver.base.page import Page,NextPageCssSelectorSetup,PageFunc,NextPageLinkTextSetup
from spider.driver.base.field import Fieldlist,Field,FieldName
from spider.driver.base.tabsetup import TabSetup
from spider.driver.base.listcssselector import ListCssSelector
from spider.driver.base.mongodb import Mongodb
import re
import time
import math
import datetime


def get_shop_grade(self,_str):

    groups = re.findall(r'[\d]{1,3}', _str)

    saveTo = (float(groups[0]) / 100 * 5)

    return str(saveTo)
def get_shop_rate(self,_str):
    return ""
fl_shop1 = Fieldlist(

    Field(fieldname=FieldName.SHOP_NAME,css_selector='div > div.sight_item_about > h3 > a',is_info=True),
    Field(fieldname=FieldName.SHOP_URL, css_selector='div > div.sight_item_about > h3 > a',
          attr='href', is_info=True),
    Field(fieldname=FieldName.SHOP_RATE,css_selector='',is_info=True,filter_func=get_shop_rate),
    Field(fieldname=FieldName.SHOP_IMG, css_selector='div > div.sight_item_show > div > a > img',
          attr='src', is_info=True),
    Field(fieldname=FieldName.SHOP_ADDRESS,
          css_selector='div > div.sight_item_about > div > p > span', is_info=True),
    Field(fieldname=FieldName.SHOP_PRICE, css_selector='div > div.sight_item_pop > table > tbody > tr:nth-child(1) > td > span > em',
          is_info=True),
    Field(fieldname=FieldName.SHOP_COMMENT_NUM,
          css_selector='div > ul > li:nth-child(1) > div > div.ct-text > ul > li:nth-child(2) > a',is_info=True),
    Field(fieldname=FieldName.SHOP_FEATURE,
          css_selector='div > div.sight_item_about > div > div.intro.color999'),
    Field(fieldname=FieldName.SHOP_GRADE,
          css_selector='div > div.sight_item_about > div > div.clrfix > div > span.product_star_level > em > span', attr='style',filter_func=get_shop_grade,
         is_info=True),

)
fl_shop2 = Fieldlist()
page_shop_1 = Page(name='去哪儿景点店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#search-list > div' ), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection),is_save=True)
page_shop_2 = ()

page_shop_2 = Page(name='去哪儿景点店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector='div > div.sight_item_about > h3 > a'), mongodb=Mongodb(db=TravelDriver.db,collection=TravelDriver.shop_collection), is_save=True)
def get_comment_grade(self,_str):

    groups = re.findall(r'[\d]{1,3}', _str)

    saveTo = (float(groups[0]) / 100 * 5)

    return str(saveTo)
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
    Field(fieldname=FieldName.COMMENT_USER_NAME, css_selector='div.mp-comments-title > span.mp-comments-username',is_info=True),
    Field(fieldname=FieldName.COMMENT_TIME, css_selector='div.mp-comments-title > span.mp-comments-time', is_info=True),
    Field(fieldname=FieldName.SHOP_NAME, css_selector='body > div.piao_wrap.redraw > div.mp-description.pngfix > div.mp-description-detail > div.mp-description-view > span', is_isolated=True,is_info=True),
    Field(fieldname=FieldName.SHOP_NAME_SEARCH_KEY,
          css_selector='body > div.piao_wrap.redraw > div.mp-description.pngfix > div.mp-description-detail > div.mp-description-view > span',filter_func=get_shop_name_search_key,
          is_isolated=True, is_info=True),
    Field(fieldname=FieldName.COMMENT_CONTENT, css_selector='p',is_info=False),
    #有问题
    Field(fieldname=FieldName.COMMENT_SCORE, css_selector='div.mp-comments-title > span.mp-star-level > em > span',attr='style',filter_func=get_comment_grade, is_info=False),
    Field(fieldname=FieldName.COMMENT_YEAR, css_selector='div.mp-comments-title > span.mp-comments-time', filter_func=get_comment_year,
          is_info=False),
    Field(fieldname=FieldName.COMMENT_SEASON, css_selector='div.mp-comments-title > span.mp-comments-time', filter_func=get_comment_season,
          is_info=False),
    Field(fieldname=FieldName.COMMENT_MONTH, css_selector='div.mp-comments-title > span.mp-comments-time', filter_func=get_comment_month,
          is_info=False),
    Field(fieldname=FieldName.COMMENT_WEEK, css_selector='div.mp-comments-title > span.mp-comments-time', filter_func=get_comment_week,
          is_info=False),
    Field(fieldname=FieldName.DATA_REGION_SEARCH_KEY, css_selector='', filter_func=get_data_region_search_key,
          is_info=True),
)
#commentList > div:nth-child(2)
#commentList > li:nth-child(2) > p
#commentList > div:nth-child(1) > p

page_comment_1 = Page(name='去哪儿景点评论列表', fieldlist=fl_comment1,
                      listcssselector=ListCssSelector(list_css_selector='#commentList > div'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)


class QunarSpotSpider(TravelDriver):

    # def get_shop_info(self):
    #
    #     try:
    #
    #         self.vertical_scroll_to()
    #         shop_data_list = self.from_page_get_data_list(page=page_shop_1)
    #         nextpagesetup = NextPageCssSelectorSetup(
    #             css_selector='#pageContainer > div > a.mp-pager-next.mp-pager-item'
    #             ,
    #             stop_css_selector='#pageContainer > div > a.mp-pager-next.mp-pager-item.hidden',
    #             page=page_comment_1, pause_time=2)
    #         extra_pagefunc = PageFunc(func=self.get_newest_comment_data_by_css_selector, nextpagesetup=nextpagesetup)
    #         self.from_page_add_data_to_data_list(page=page_shop_2, pre_page=page_shop_1, data_list=shop_data_list,
    #                                              extra_pagefunc=extra_pagefunc
    #                                              )
    #     except Exception as e:
    #         self.error_log(e=str(e))

    def get_shop_info_list(self):
        self.fast_get_page('http://piao.qunar.com/', is_max=False)
        time.sleep(2)
      #  self.fast_click_page_by_css_selector('#js_nva_cgy > li.c_piao.js-searchnav.cur > a')
        self.until_send_text_by_css_selector(css_selector='#searchValue', text=self.data_region)
       # self.until_send_enter_by_css_selector(css_selector='#searchValue')

        self.fast_click_page_by_css_selector('#searchBtn')
        # self.until_send_enter_by_css_selector(css_selector='#js-piao-ticket > div.qcbox > div.qunar-qcbox > input')


        time.sleep(10)
        self.until_click_no_next_page_by_css_selector(nextpagesetup=NextPageCssSelectorSetup(css_selector='#pager-container > div > a.next',stop_css_selector='#pager-container > div > a.next.hidden',main_pagefunc=PageFunc(func=self.from_page_get_data_list,  page=page_shop_1)))



    def get_comment_list(self):
        self.fast_new_page(url='http://www.baidu.com');
        shop_collcetion = Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection,
                                 ).get_collection()
        shop_name_url_list = list()
        for i in shop_collcetion.find(self.get_data_key()):
            if i.get('shop_url'):
                shop_name_url_list.append((i.get('shop_name'),i.get('shop_url')))
        for i in range(len(shop_name_url_list)):
            first = True
            self.info_log(data='第%s个,%s'%(i+1, shop_name_url_list[i][0]))
            # self.switch_window_by_index(index=-1)
            #
            # self.fast_new_page(url=shop_name_url_list[i][1])
            # self.deal_with_failure_page()

            while (True):
                self.is_ready_by_proxy_ip()
                self.switch_window_by_index(index=-1)
                self.deal_with_failure_page()
                self.fast_new_page(url=shop_name_url_list[i][1])
                time.sleep(1)
                self.switch_window_by_index(index=-1)  # 页面选择
                if '请求数据错误，请稍后再试' in self.driver.title:

                   self.info_log(data='关闭错误页面!!!')
                   self.close_curr_page()
                else:
                   break
            self.until_click_no_next_page_by_partial_link_text(
            nextpagesetup=NextPageLinkTextSetup(link_text='下一页', pause_time=3,
                                                main_pagefunc=PageFunc(func=self.from_page_get_data_list,
                                                                       page=page_comment_1)))
            self.close_curr_page()


    def run_spider(self):
        try:
            #self.get_shop_info_list()
            self.get_comment_list()
        except Exception:
            self.error_log()