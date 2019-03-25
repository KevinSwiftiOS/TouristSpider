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
from urllib import request
import demjson
import json




def get_shop_area(self,_str):
    return '千岛湖乡村游景点'



fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='dl > dd > a > h2',is_info=True),
    Field(fieldname=FieldName.SHOP_URL, css_selector='dl > dd > a', attr='href',is_info=True),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='dl > dd > div.tourListLeftListMsg > span:nth-child(1)', is_info=True),

    Field(fieldname=FieldName.SHOP_PHONE,css_selector='dl > dd > div.tourListLeftListMsg > span:nth-child(2)', is_info=True),
    Field(fieldname=FieldName.SHOP_AREA, css_selector='dl > dd > div.tourListLeftListMsg > span:nth-child(2)',filter_func=get_shop_area,
          is_info=True)
)

page_shop_1 = Page(name='大众点评餐饮店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='body > div.mainLayout.newsMainLayout > div.newsLeftLayout.sceneRightLayout > div'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection), is_save=True)



detail_fl_shop2 = Fieldlist(



Field(fieldname=FieldName.SHOP_DES,css_selector='body > div.mainLayout.newsMainLayout > div.newsLeftLayout.sceneRightLayout > div.newsDetailContent > div.newsDetailConNote > div',is_info=True),

)




detail_shop_2 = Page(name='大众点评获取评论分数和数量页面', fieldlist=detail_fl_shop2,is_save=True)

class GuanWangSpotSpider(TravelDriver):



    def get_shop_info_list(self):

        self.fast_new_page(url = 'http://www.qiandaohu.cc/qdhfg/jqjd/xcyjd/#wzqdh')

        time.sleep(60)
        self.until_click_no_next_page_by_partial_link_text(NextPageLinkTextSetup(link_text='下一页', is_proxy=False,
                                                                                     main_pagefunc=PageFunc(
                                                                                         self.from_page_get_data_list,
                                                                                         page=page_shop_1)))
                  #self.close_curr_page()


    def get_shop_des(self):
        self.fast_new_page(url="http://www.baidu.com");
        shop_collcetion = Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection,

                                  host='localhost').get_collection()
        shop_name_url_list = list()
        for i in shop_collcetion.find(self.get_data_key()):
            # if i.get('shop_url') and (i.get('shop_flag') == None or i.get("shop_flag") == "0" or i.get("shop_flag") == ""
            #
            # or( i.get("shop_comment_num") == 0 and i.get("shop_score") > 0)
            # ):

             shop_name_url_list.append((i.get('shop_name'), i.get('shop_url')))
        for i in range(len(shop_name_url_list)):
            # self.fast_new_page(url='https://www.baidu.com');

            self.info_log(data='第%s个,%s' % (i + 1, shop_name_url_list[i][0]))
            self.fast_new_page(url=shop_name_url_list[i][1], is_scroll_to_bottom=True);
            time.sleep(5)
            data = self.from_fieldlist_get_data(page=detail_shop_2)
            self.update_data_to_mongodb(shop_collcetion,
                                        self.merge_dict(self.get_data_key(),
                                                        {FieldName.SHOP_URL: shop_name_url_list[i][1]}), data)
            self.close_curr_page();

    def run_spider(self):
        try:


            #elf.get_shop_info_list()
            self.get_shop_des() #获取景点描述
        except Exception:
            self.error_log(e='cookies失效!!!')