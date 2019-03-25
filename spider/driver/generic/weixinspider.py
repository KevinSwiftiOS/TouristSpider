# -*- coding:utf-8 -*-
from spider.driver.base.driver import Driver
from spider.driver.base.mysql import Mysql
import time
from pyquery import PyQuery
from spider.driver.base.field import Field,FieldName,Fieldlist,FieldType
from spider.driver.base.page import Page
from spider.driver.base.listcssselector import ListCssSelector
from spider.driver.base.mongodb import Mongodb
from spider.driver.base.tabsetup import TabSetup

fl_weixin1 = Fieldlist(
    Field(fieldname='public_name', css_selector='div > div.txt-box > p.tit > a', regex=r'[^\u4e00-\u9fa5]*'),
)

fl_weixin2 = Fieldlist(
    Field(fieldname='article_name', css_selector='div > div > h4'),
    Field(fieldname='article_time', css_selector='div > div > p.weui_media_extra_info'),
)

page_weixin_1 = Page(name='微信公众号列表页面', fieldlist=fl_weixin1, listcssselector=ListCssSelector(list_css_selector='#main > div.news-box > ul > li'))

page_weixin_2 = Page(name='微信公众号文章列表页面', fieldlist=fl_weixin2, tabsetup=TabSetup(click_css_selector='div > div.txt-box > p.tit > a'), listcssselector=ListCssSelector(list_css_selector='#history > div'))

class WeixinSpider(Driver):

    def __init__(self,isheadless=False,ismobile=False,isvirtualdisplay=False,spider_id='',name=''):
        Driver.__init__(self, log_file_name=spider_id, ismobile=ismobile, isvirtualdisplay=isvirtualdisplay,
                        isheadless=isheadless)
        self.name = name
        self.debug_log(name=name)

    def get_article(self, data_list=[]):
        article_list = self.until_presence_of_all_elements_located_by_css_selector(css_selector=page_weixin_2.listcssselector.list_css_selector)
        for i in range(1, len(article_list)+1):
            self.until_scroll_to_center_click_by_css_selector(css_selector='%s:nth-child(%s)'%(page_weixin_2.listcssselector.list_css_selector,i))
            time.sleep(3)
            self.driver.back()

    def run_spider(self):
        for public in Mysql().query_data(table='weixin_public', field='public_name')[:1]:
            self.fast_get_page(url='http://weixin.sogou.com/', min_time_to_wait=15,max_time_to_wait=30)
            self.until_send_text_by_css_selector(css_selector='#query', text=public[0])
            time.sleep(3)
            self.fast_enter_page_by_css_selector(css_selector='#query')
            time.sleep(2)
            self.fast_click_same_page_by_css_selector(click_css_selector='#scroll-header > form > div > input.swz2')
            public_name_list = self.from_page_get_data_list(page=page_weixin_1)
            article_name_list = self.from_page_add_data_list_to_data_list(page=page_weixin_2, pre_page=page_weixin_1,data_list=public_name_list, extra_page_func=self.get_article)
                # self.fast_click_page_by_css_selector(ele=item, click_css_selector='div > div.txt-box > p.tit > a')
                # self.driver.switch_to.window(self.driver.window_handles[-1])
                # shop_data_list = self.from_page_get_data_list(page=page_weixin_1)
                # self.driver.close()
                # self.driver.switch_to.window(self.driver.window_handles[-1])