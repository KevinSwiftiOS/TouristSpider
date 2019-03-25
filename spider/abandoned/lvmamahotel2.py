# -*- coding:utf-8 -*-

from spider.driver.spider.base.lvmamahotelspider import LvmamaHotelSpider
import sys
from spider.driver.spider.base.travel.field import *
from spider.driver.spider.base.travel.runningparams import *

fields_shop1 = [
    Field(name=FieldName.SHOP_NAME,css_selector='div.ml-pro-info > p'),
    Field(name=FieldName.SHOP_URL,attr='href'),
    Field(name=FieldName.SHOP_ID,attr='href',regex='[^\d]*'),
    Field(name=FieldName.SHOP_IMG,css_selector='div.ml-pro-img > img',attr='src'),
    Field(name=FieldName.SHOP_PRICE,css_selector='div.ml-pro-info > div.t_price > span.pri_right'),
    Field(name=FieldName.SHOP_ACTIVE_STATUS,css_selector='div.ml-pro-info > div.ml-pro-time'),
    Field(name=FieldName.SHOP_GRADE,css_selector='div.ml-pro-info > div.t_price > span.pri_left',
          regex='^([\d.]*).*$',repl='\\1'),
    Field(name=FieldName.SHOP_COMMENT_NUM,
          css_selector='div.ml-pro-info > div.t_price > span.pri_left > span.line1 > i',
          regex='^[ ]*([\d.]*).*$',repl='\\1'),
    Field(name=FieldName.SHOP_TITLE,
          css_selector='div.ml-pro-info > div.t_price > span.pri_left > span.line1 > i',
          regex='^[^\|]*\|(.*)$', repl='\\1'),
    Field(name=FieldName.SHOP_ADDRESS,
          css_selector='div.ml-pro-info > div.t_price > span.pri_left > span.line2'),
]

fields_shop2 = [
    Field(name=FieldName.SHOP_STATISFACTION_PERCENT,
          css_selector='#body-padtop > div > div.container > div.m-comments > div > div.left',offset=100),
    Field(name=FieldName.SHOP_STATISTICS,
          css_selector='#body-padtop > div > div.container > div.m-comments > div > div.right',offset=100),
    Field(name=FieldName.SHOP_TIME,
          css_selector='#body-padtop > div > div.container > div.m-detail-tips', offset=100),
]

fields_comment1 = [
    Field(name=FieldName.COMMENT_USER_NAME,css_selector='div.top > div.tourist > div'),
    Field(name=FieldName.COMMENT_TIME,css_selector='div.comment-bottom > p'),
    Field(name=FieldName.COMMENT_CONTENT,css_selector='div.comment-txt.line-clamp3'),
    ListField(name=FieldName.COMMENT_PIC_LIST,list_css_selector='div.comment-pic',
              item_css_selector='img',attr='src'),
    Field(name=FieldName.COMMENT_LIKE_NUM,css_selector='div.comment-bottom > div.usefulCount.ticket'),
    Field(name=FieldName.COMMENT_REPLY_NUM,css_selector='div.comment-bottom > div.chatReply'),
]

params_dict = {
    ParamType.SHOP_INFO_1 : Params_list(type=ParamType.SHOP_INFO_1,
    list_css_selector='#hotel_searchListUl1 > li',
    item_css_selector='a',field_list=fields_shop1),
    ParamType.SHOP_INFO_2 : Params(type=ParamType.SHOP_INFO_2,field_list=fields_shop2),
    ParamType.COMMENT_INFO_1 : Params_list(type=ParamType.COMMENT_INFO_1,
    list_css_selector='#view > div.comment > div.wrap2 > div',
    field_list=fields_comment1),
}

if __name__ == '__main__':
    spider = LvmamaHotelSpider(isheadless=False,ismobile=True,params_dict=params_dict,
                              id=sys.argv[1],
                              data_website=sys.argv[2],
                              data_region=sys.argv[3],
                              data_source=sys.argv[4])
    spider.run_spider()