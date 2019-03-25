from spider.driver.travel.core.traveldriver import TravelDriver
from spider.driver.base.page import Page,NextPageCssSelectorSetup,PageFunc
from spider.driver.base.field import Fieldlist,Field,FieldName
from spider.driver.base.tabsetup import TabSetup
from spider.driver.base.listcssselector import ListCssSelector
from spider.driver.base.mongodb import Mongodb
from pyquery import PyQuery as pq
from selenium import webdriver
import re
import time
import json
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
fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='a > div.ml-pro-info > p'),
#\31 302 > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(1) > span:nth-child(2)
#\32 0808 > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(1) > span:nth-child(2)
    Field(fieldname=FieldName.SHOP_PRICE, css_selector=' a > div.ml-pro-info > div.ml-pro-price > span.price > i:nth-child(2)',is_info=True),
    #稍微有点问题
    Field(fieldname=FieldName.SHOP_URL,css_selector='a',attr='href', is_debug=True,is_info=True),
    #img还有些许问题
#\33 6822720 > div:nth-child(1) > div
    Field(fieldname=FieldName.SHOP_IMG, css_selector='a > div.ml-pro-img > img', attr='src', is_info=True),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector= 'a > div.ml-pro-info > div.orderNum.adress > span:nth-child(1)', is_info=True),
    #这里应该做一个转换
#\34 187 > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(2) > span:nth-child(1)
    Field(fieldname=FieldName.SHOP_GRADE,css_selector='a > div.ml-pro-info > div:nth-child(3) > span', is_info=True),
    #正则表达式的使用有问题
    Field(fieldname=FieldName.SHOP_COMMENT_NUM,css_selector='',filter_func=get_comment_num, is_info=True),
    #无shop_feature

    Field(fieldname=FieldName.SHOP_FEATURE, css_selector='',filter_func=get_shop_feature, is_info=True),

    Field(fieldname=FieldName.SHOP_RATE,css_selector='',filter_func=get_shop_rate, is_info=True),
    Field(fieldname=FieldName.SHOP_COMMENT_URL,css_selector='a',attr='href',filter_func=get_comment_url,is_info=True)
)
page_shop_1 = Page(name='驴妈妈景点店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#ticket_searchListUl1 > li'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection), is_save=True)


def get_comment_time(self,_str):
    return _str[0:10]
def get_comment_grade(self,_str):
    print(_str)
    width = re.findall(r'[\d]{1,3}', _str)[0]
    print(float(width) / 150 * 5)
    return str(float(width) / 150 * 5)
fl_comment1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='#view > div.prolink > a > span', is_info=True,is_isolated=True),
#app > div > div.poi-rate-container > div:nth-child(2) > div.rate-content-container > div
#app > div > div.poi-rate-container > div:nth-child(7) > div.rate-content-container > div
    Field(fieldname=FieldName.COMMENT_CONTENT, css_selector= 'div.comment-txt.line-clamp3 > div > p', is_info=True),
    Field(fieldname=FieldName.COMMENT_USER_NAME, css_selector='div.top > div.tourist > div > p', is_info=True),
    #comment_grade有待商榷
    Field(fieldname=FieldName.COMMENT_SCORE, css_selector='div.top > div.tourist > div > span', attr='style',filter_func=get_comment_grade, is_info=True),
    Field(fieldname=FieldName.COMMENT_TIME, css_selector='div.comment-bottom > p',filter_func=get_comment_time, is_info=True),
)
page_comment_1 = Page(name='驴妈妈景点店铺评论列表页面', fieldlist=fl_comment1, listcssselector=ListCssSelector(list_css_selector='#view > div.comment > div > div',item_start=10), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)














class LvmamaMobileSpotSpider(TravelDriver):

    def get_shop_info_list(self):
        self.fast_get_page(url='https://m.lvmama.com/ticket/search')
        time.sleep(5)
        self.until_scroll_to_center_send_text_by_css_selector(css_selector='#searchInput',text=self.data_region)
        self.until_scroll_to_center_send_enter_by_css_selector(css_selector='#searchInput')
        shop_data_list = self.from_page_get_data_list(page=page_shop_1)

    def get_comment_info_list(self):
       shop_collcetion = Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection,
                                 host='localhost').get_collection()
       shop_name_url_list = list()
       for i in shop_collcetion.find(self.get_data_key()):
           if i.get('shop_comment_url'):
               shop_name_url_list.append((i.get('shop_name'), i.get('shop_comment_url')))

       for i in range(len(shop_name_url_list)):
           # 可能会有反爬
           self.info_log(data='第%s个,%s' % (i + 1, shop_name_url_list[i][0]))
           self.fast_new_page(url=shop_name_url_list[i][1])
           time.sleep(5)


           comment_data_list = self.from_page_get_data_list(page=page_comment_1)
           self.close_curr_page()



    def run_spider(self):
       #self.get_shop_info_list()
       #self.get_shop_detail()
       self.get_comment_info_list()