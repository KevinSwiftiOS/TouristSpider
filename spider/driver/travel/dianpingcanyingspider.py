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
import codecs
def get_comment_url(self,_str):
    return _str + "/review_all"
def get_shop_cookie_style(self,_str):
    return  self.shop_cook_style
def get_shop_score(self,_str):
    return (float(re.findall(r'([\d]{1,4})', _str)[0]) / 10)
def get_zero(self,_str):
    return 0.0



def get_shop_site(self,_str):
    return self.shop_site



fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='div.txt > div.tit > a > h4',is_info=True),
    Field(fieldname=FieldName.SHOP_URL, css_selector='div.txt > div.tit > a', attr='href',is_info=True),
    Field(fieldname=FieldName.SHOP_COMMENT_NUM, css_selector='div.txt > div.comment > a.review-num',attr='innerHTML',filter_func=get_zero, is_info=True),
Field(fieldname=FieldName.SHOP_PRICE, css_selector='div.txt > div.comment > a.mean-price > b',attr='innerHTML',filter_func=get_zero, is_info=True),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='div.txt > div.tag-addr > span.addr',is_info=True),
    Field(fieldname=FieldName.SHOP_IMG,css_selector='div.pic > a > img',attr='src', is_info=True),
    Field(fieldname=FieldName.SHOP_SCORE,css_selector='div.txt > div.comment > span',filter_func=get_zero,attr='class', is_info=True),
    Field(fieldname=FieldName.SHOP_COOK_STYLE,css_selector='',filter_func=get_shop_cookie_style, is_info=True),
    Field(fieldname=FieldName.SHOP_SITE,css_selector='',filter_func=get_shop_site, is_info=True),
Field(fieldname=FieldName.SHOP_COMMENT_URL, css_selector='div.txt > div.tit > a', attr='href',filter_func=get_comment_url, is_info=True),
Field(fieldname=FieldName.SHOP_LNG, css_selector='',filter_func=get_zero, is_info=True),
Field(fieldname=FieldName.SHOP_LAT, css_selector='',filter_func=get_zero, is_info=True),

Field(fieldname=FieldName.SHOP_SERVICE, css_selector='',filter_func=get_zero, is_info=True),
Field(fieldname=FieldName.SHOP_TASTE, css_selector='',filter_func=get_zero, is_info=True),

Field(fieldname=FieldName.SHOP_ENV, css_selector='',filter_func=get_zero, is_info=True),
)

page_shop_1 = Page(name='大众点评餐饮店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#shop-all-list > ul > li'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection), is_save=True)
# def get_shop_address(self,_str):
#     doc = _str.split('<br>')
#
#     return (re.sub(r'地址：', "", doc[0].strip()))
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
fl_shop2 = Fieldlist(


    Field(fieldname=FieldName.SHOP_LNG,
          css_selector='#pointInput',attr='data-clipboard-text', filter_func=get_shop_lng,
          is_info=True),
    Field(fieldname=FieldName.SHOP_LAT,
          css_selector='#pointInput',attr='data-clipboard-text', filter_func=get_shop_lat,
          is_info=True)
)
page_shop_2 = Page(name='大众点评获取经纬度页面', fieldlist=fl_shop2,is_save=True)

def get_span_text(span):
    if (span.attr('class') == 'zl-gc5M'):
     return '2';
    if (span.attr('class') == 'zl-giSW'):
        return '3';
    if (span.attr('class') == 'zl-Jvp2'):
        return '4';
    if (span.attr('class') == 'zl-Cg3x'):
        return '5';
    if (span.attr('class') == 'zl-TohQ'):
        return '6';
    if (span.attr('class') == 'zl-tvPf'):
        return '7';
    if (span.attr('class') == 'zl-htaN'):
        return '8';
    if (span.attr('class') == 'zl-FhcV'):
        return '9';
    if (span.attr('class') == 'zl-JTyc'):
        return '0';



def get_shop_price(self,html):
    temp = re.sub(r'(<d){1}', "&", html);
    res = "";
    for i,word in enumerate(temp):
        if (word == '&'):
            res += ('&');

        if (word == '1'):
            res += ('1');

    doc = PyQuery(html)
    spans = list(doc('d').items());
    # 进行匹配
    str = ""
    if (len(spans) == 0):
        return (html)

    else:
        for span in spans:

                res = re.sub(r'&', get_span_text(span), res, 1);

        return (res);




def get_comment_num(self,html):

    temp = re.sub(r'(<d){1}', "&", html);
    res = "";
    for i,word in enumerate(temp):
        if (word == '&'):
            res += ('&');

        if (word == '1'):
            res += ('1');

    doc = PyQuery(html)
    spans = list(doc('d').items());
    # 进行匹配
    str = ""
    if (len(spans) == 0):
        return (html)

    else:
        for span in spans:

                res = re.sub(r'&', get_span_text(span), res, 1);

        return (res);


def get_shop_taste(self,html):
    doc = PyQuery(html)
    spans = list(doc('d').items());
    # 进行匹配
    res = ""
    if (len(spans) == 0):
        return (0)

    else:
        for span in spans:
            res += get_span_text(span);
        if(len(res) == 2):
          return  res[0] + '.' + res[1]
        if(len(res) == 1):
            return res[0] + '.1'

def get_shop_address(self,_str):
    text = re.sub(r'window.shop_config=',"",_str);
    text = (demjson.decode(text))
    return (text['address'])


    # return (re.sub(r'地址：', "", doc[0].strip()))
# def get_shop_lng(self,_str):
#     text = re.sub(r'window.shop_config=', "", _str);
#     text = (demjson.decode(text))
#     return (text['shopGlng'])
# def get_shop_lat(self,_str):
#     text = re.sub(r'window.shop_config=', "", _str);
#     text = (demjson.decode(text))
    return (text['shopGlat'])
def get_shop_category_name(self,_str):
    text = re.sub(r'window.shop_config=', "", _str);
    text = (demjson.decode(text))
    return (text['mainCategoryName'])
def get_shop_flag(self,_str):

    if(_str != ""):

        return "1";
    return "0";
def get_target_text(_html_content, _css_content, _svg_content):
    # 构建词典
    height_text = {}
    p = PyQuery(_svg_content)
    # 格式1
    try:
        for item in p("path").items():
            max_height = int(item.attr("d").split()[1])
            text = p("textpath:nth-child(%s)" % item.attr("id")).text()
            height_text[max_height] = text
    except Exception:
        pass
    # 格式2
    try:
        for item in p("text").items():
            max_height = int(item.attr("y"))
            text = item.text()
            height_text[max_height] = text
    except Exception:
        pass

    def get_single_text(_class_name):
        """
        获得目标词
        """
        # 查找class对应的属性
        try:
            x, y = \
            re.findall("\.%s{background:[-]*([\d]+)[.]*[\d]+px [-]*([\d]+)[.]*[\d]+px;}" % _class_name, _css_content)[0]
            x = int(x)
            y = int(y)
        except Exception:
            return _class_name
        # 获得目标的文字的高度列表
        height_list = list(height_text.keys()) + [y]
        height_list.sort()
        # 获得目标文字
        target_text = list(height_text[height_list[height_list.index(y) + 1]])[x // 14]
        return target_text

    # 获得解密后的评论
    _html_content_list = PyQuery(re.sub(r"<[a-z]+ class=\"([a-zA-Z0-9]+)\"/>", r"|\1|", _html_content)).text().split("|")
    for i in range(len(_html_content_list)):
        _html_content_list[i] = get_single_text(_html_content_list[i])
    return re.sub("收起评论.*$", "", "".join(_html_content_list)).replace("\n", "").strip()

detail_fl_shop2 = Fieldlist(

    Field(fieldname=FieldName.SHOP_COMMENT_NUM,
#reviewCount
          css_selector='#reviewCount',attr='innerHTML', is_info=True),
    Field(fieldname=FieldName.SHOP_SCORE,
          css_selector='#basic-info > div.brief-info > span', attr='class', filter_func=get_shop_score,
          is_info=True),
Field(fieldname=FieldName.SHOP_PRICE,
          css_selector='#avgPriceTitle', attr='innerHTML', filter_func=get_shop_price,
          is_info=True),


Field(fieldname=FieldName.SHOP_ADDRESS,css_selector='#top > script:nth-child(4)',is_info=True),

)




detail_shop_2 = Page(name='大众点评获取评论分数和数量页面', fieldlist=detail_fl_shop2,is_save=True)
def get_rate(self, _str):
    try:
        return str(int(re.sub('[^\d]*','',_str))/10)
    except Exception:
        return 0

def get_comment_rate_tag(self, _str):
    p = PyQuery(_str)
    tag_list = []
    for i in p('span.item').items():
        tag_list.append(i.text().strip())
    return json.dumps(tag_list, ensure_ascii=False)

def get_content(self, _str):

    p = PyQuery(_str)
    if p('div.review-words.Hide'):

        html = p('div.review-words.Hide').html().strip()
        try:
         str =  (get_target_text(html,
                              open('/Users/caokaiqiang/Documents/sourceTree/TouristSpider/style.css', 'r').read(),
                              codecs.open('/Users/caokaiqiang/Documents/sourceTree/TouristSpider/zf.svg', 'r',
                                          encoding='utf-8').read()));


        except Exception:
            str = "";
    else:

        html = p('div.review-words').html().strip()
        # 表明没有字符
        try:
         str = (get_target_text(html,
                               open('/Users/caokaiqiang/Documents/sourceTree/TouristSpider/style.css', 'r').read(),
                               codecs.open('/Users/caokaiqiang/Documents/sourceTree/TouristSpider/zf.svg', 'r',
                                           encoding='utf-8').read()));



        except Exception:
            str = "";
    return str;



def get_comment_time(self,_str):


     return re.findall(r'([\d]{4}-[\d]{2}-[\d]{2})', _str)[0]
def get_comment_grade(self,_str):
    grade = re.findall(r'([\d]{1,4})',_str)[0]

    return str(round(float(grade) / 50 * 5,1))
def get_comment_year(self,_str):
    time = re.findall(r'([\d]{4}-[\d]{2}-[\d]{2})', _str)[0]
    return time[0:4];

def get_comment_season(self, _str):
    time = re.findall(r'([\d]{4}-[\d]{2}-[\d]{2})', _str)[0]
    times = time.split('-');

    month = int(times[1])

    seasons = ['01', '02', '03', '04'];
    if (month % 3 == 0):
        return (times[0] + '-' + seasons[int(month / 3) - 1]);
    else:
        index = int(math.floor(month / 3));
        return (times[0] + '-' + seasons[index]);
def get_comment_month(self, _str):
    time = re.findall(r'([\d]{4}-[\d]{2}-[\d]{2})', _str)[0]
    return time[0:7];
def get_comment_week(self, _str):
    temp = re.findall(r'([\d]{4}-[\d]{2}-[\d]{2})', _str)[0]
    time = temp[0:10]
    times = time.split('-');
    return (times[0] + '-' + str(datetime.date(int(times[0]), int(times[1]), int(times[2])).isocalendar()[1]).zfill(2))



def get_data_region_search_key(self, _str):

    return  self.data_region_search_key

def get_shop_name_search_key(self,_str):
    return self.get_shop_name_search_key(_str);
def get_shop_name_search_key(self,_str):

    return self.shop_name_search_key(_str);
def get_shop_area(self,_str):
    return "千岛湖东南湖区"
def get_shop_phone(self,_str):
    return re.findall(r'([\d]{1,20})', _str)[0]

def get_shop_service(self,_str):
    return re.findall(r'([\d].[\d])', _str)[0]
def get_comment_shop_score(self,_str):

    return (float(re.findall(r'([\d]{1,4})', _str)[0]) / 10)

def get_comment_user_name(self,_str):

    html = PyQuery(_str);
    if(html('span').filter('.name').text() == ""):
        return html('a').filter('.name').text()
    else:
        return html('span').filter('.name').text()

def get_comment_type(self,_str):
    grade = re.findall(r'([\d]{1,4})', _str)[0]
    if(grade >= "3.0"):
        return "好评";
    elif(grade == "3.0"):
        return "中评";
    else:
        return "差评";

def get_comment_taste_score(self,_str):
    html = PyQuery(_str)
    ##获取元素
    res = "";
    if (html('span.score')):
        items = (html('span.item'));
        # 获得字符串
        score = items.eq(0).text();
        # 返回分数
        res = (score[3:len(score)]);
    else:
        res = "";
    return res;

def get_comment_env_score(self,_str):
    html = PyQuery(_str)
    ##获取元素
    res = "";
    if (html('span.score')):
        items = (html('span.item'));
        # 获得字符串
        score = items.eq(1).text();
        # 返回分数
        res =  (score[3:len(score)]);
    else:
        res =  "";
    return res;

def get_comment_service_score(self,_str):
    html = PyQuery(_str)
    ##获取元素
    res = "";
    if (html('span.score')):
        items = (html('span.item'));
        # 获得字符串
        score = items.eq(2).text();
        # 返回分数
        res =  (score[3:len(score)]);
    else:
        res =  "";
    return res;


def get_comment_price_score(self,_str):
    html = PyQuery(_str)
    ##获取元素
    res = "";
    if (html('span.score')):
        items = (html('span.item'));
        # 获得字符串
        score = items.eq(3).text();
        if("元" in score):
        # 返回分数
         res =  (score[3:len(score) - 1]);
        else:
         res = "";
    else:
        res =  "";
    return res;
def get_comment_like_num(self,_str):
    if(_str == ""):
        return 0;
    else:
        return _str;
fl_comment1 = Fieldlist(

    Field(fieldname=FieldName.SHOP_NAME, css_selector='#review-list > div.review-list-container > div.review-shop-wrap > div.shop-info.clearfix > h1', is_isolated=True,is_info=True),

Field(fieldname=FieldName.SHOP_AREA,
          css_selector='#review-list > div.review-list-container > div.review-shop-wrap > div.shop-info.clearfix > h1',
          is_isolated=True,filter_func=get_shop_area, is_info=True),



Field(fieldname=FieldName.SHOP_NAME_SEARCH_KEY, css_selector='#review-list > div.review-list-container > div.review-shop-wrap > div.shop-info.clearfix > h1',filter_func=get_shop_name_search_key, is_isolated=True,is_info=False),
#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.reviews-items > ul > li:nth-child(1) > div > div.dper-info > a
#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.reviews-items > ul > li:nth-child(34) > div.main-review > div.dper-info > span

#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.reviews-items > ul > li:nth-child(26) > div.main-review > div.dper-info > span
    Field(fieldname=FieldName.COMMENT_USER_NAME, css_selector='div > div.dper-info',filter_func=get_comment_user_name, attr='innerHTML',is_info=True),
    Field(fieldname=FieldName.COMMENT_TIME, css_selector='div > div.misc-info.clearfix > span.time',filter_func=get_comment_time,is_info=True),

    Field(fieldname=FieldName.COMMENT_CONTENT, css_selector='div.main-review', attr='innerHTML',
          filter_func=get_content,is_info=True),

    Field(fieldname=FieldName.COMMENT_SCORE,css_selector='div > div.review-rank > span.sml-rank-stars',attr='class',filter_func=get_comment_grade, is_info=True),
    Field(fieldname=FieldName.COMMENT_YEAR, css_selector='div > div.misc-info.clearfix > span.time',
          filter_func=get_comment_year,
          is_info=False),
    Field(fieldname=FieldName.COMMENT_SEASON, css_selector='div > div.misc-info.clearfix > span.time',
          filter_func=get_comment_season,
          is_info=False),
    Field(fieldname=FieldName.COMMENT_MONTH, css_selector='div > div.misc-info.clearfix > span.time',
          filter_func=get_comment_month,
          is_info=False),
    Field(fieldname=FieldName.COMMENT_WEEK, css_selector='div > div.misc-info.clearfix > span.time',
          filter_func=get_comment_week,
          is_info=False),
    Field(fieldname=FieldName.DATA_REGION_SEARCH_KEY, css_selector='', filter_func=get_data_region_search_key,
          is_info=False),
    Field(fieldname=FieldName.COMMENT_TYPE,css_selector='div > div.review-rank > span.sml-rank-stars',attr='class',filter_func=get_comment_type,is_info=True),


    Field(fieldname=FieldName.COMMENT_TASTE_SCORE, css_selector='div > div.review-rank',attr='innerHTML',filter_func=get_comment_taste_score,is_info=True),

    Field(fieldname=FieldName.COMMENT_ENV_SCORE,attr='innerHTML',
          css_selector='div > div.review-rank',filter_func=get_comment_env_score,  is_info=True),

    Field(fieldname=FieldName.COMMENT_SERVICE_SCORE,attr='innerHTML',
          css_selector='div > div.review-rank',filter_func=get_comment_service_score, is_info=True),

    Field(fieldname=FieldName.COMMENT_AVERAGE_PRICE,attr='innerHTML',
          css_selector='div > div.review-rank',filter_func=get_comment_price_score, is_info=True),
    #
    #

    # Field(fieldname=FieldName.COMMENT_PIC_LIST, list_css_selector='div.main-review > div.review-pictures > ul', item_css_selector='li > a > img', attr='src', timeout=0),
)
page_comment_1 = Page(name='大众点评餐饮评论列表', fieldlist=fl_comment1, listcssselector=ListCssSelector(list_css_selector='#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.reviews-items > ul > li'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)


def get_comment_category(self,_str):
    return self.comment_category

fl_comment2 = Fieldlist(

    Field(fieldname=FieldName.COMMENT_USER_NAME, css_selector='div > div.dper-info', filter_func=get_comment_user_name,
          attr='innerHTML', is_info=True),
    Field(fieldname=FieldName.COMMENT_TIME, css_selector='div > div.misc-info.clearfix > span.time',
          filter_func=get_comment_time, is_info=True),
    Field(fieldname=FieldName.COMMENT_CATEGORY, css_selector='',
          filter_func=get_comment_category, is_info=True),
    Field(fieldname=FieldName.SHOP_NAME, css_selector='#review-list > div.review-list-container > div.review-shop-wrap > div.shop-info.clearfix > h1', is_isolated=True,is_info=True),

)





page_comment_2 = Page(name='大众点评餐饮评论列表', fieldlist=fl_comment2, listcssselector=ListCssSelector(list_css_selector='#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.reviews-items > ul > li'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)
class DianpingCanYingSpider(TravelDriver):



    def get_shop_info_list(self):

        self.fast_new_page(url = 'http://www.dianping.com/qiandaohu/food')
        #这里加一个循环即可
        shop_cooks = ['水果生鲜']

        for shop_cook in shop_cooks:
           # time.sleep(5)
            self.shop_cook_style = shop_cook
            for i in range(1,10):
                 #self.fast_new_page(url='http://www.dianping.com/qiandaohu/ch10/g118r85473')

                 self.fast_click_first_item_same_page_by_partial_link_text(link_text=shop_cook)
                 time.sleep(2)
                 try:

                  self.driver.find_element_by_css_selector(css_selector='#bussi-nav > a:nth-child(' + str(i) + ')').click()


                  time.sleep(2)
                  self.shop_site = self.driver.find_element_by_xpath('//*[@id="bussi-nav"]/a[' + str(i) + ']').text
                  #self.shop_site = '千岛湖风景区'
                  self.until_click_no_next_page_by_partial_link_text(NextPageLinkTextSetup(link_text='下一页', is_proxy=False,
                                                                                     main_pagefunc=PageFunc(
                                                                                         self.from_page_get_data_list,
                                                                                         page=page_shop_1)))
                  #self.close_curr_page()
                 except Exception:
                     print("无标签")


    def login(self):
       # self.fast_new_page(url='http://www.baidu.com')
        self.fast_new_page(url='http://www.dianping.com',is_scroll_to_bottom=False)
        time.sleep(2)
        # with open('./cookies/dianping_cookies.json', 'r', encoding='utf-8') as f:
        #     listCookies = json.loads(f.read())

        # for cookie in listCookies:
        #     self.driver.add_cookie(cookie)
        # self.close_curr_page()
        # self.fast_new_page(url='http://www.dianping.com')

        time.sleep(20)





    #获取经纬度和坐标
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

            if i.get('shop_url'):
                shop_name_url_list.append((i.get('shop_name'),i.get('shop_url')))

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
            if('千岛湖' in shop_name_url_list[i][0]):
             self.until_scroll_to_center_send_text_by_css_selector(css_selector='#localvalue',text=shop_name_url_list[i][0])
            else:
             self.until_scroll_to_center_send_text_by_css_selector(css_selector='#localvalue',
                                                                      text='千岛湖' + shop_name_url_list[i][0])
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

                data = self.from_fieldlist_get_data(page=page_shop_2)
                self.update_data_to_mongodb(shop_collcetion,
                                        self.merge_dict(self.get_data_key(),
                                                        {FieldName.SHOP_URL: shop_name_url_list[i][1]}), data)
            except Exception:
                print("改地址无经纬度")


    def get_shop_good_middle_bad_comment(self):
        # self.fast_new_page(url='http://www.baidu.com')
        # shop_collcetion = Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection,
        #                         ).get_collection()
        #  # shop_name_url_list = ['http://www.dianping.com/shop/23242707/review_all','http://www.dianping.com/shop/114535359/review_all','http://www.dianping.com/shop/107667835/review_all']
        # shop_name_url_list = list();
        # for i in shop_collcetion.find(self.get_data_key()):
        #    # if i.get('shop_comment_url'):
        #        if(i.get('shop_comment_num') > 1000):
        #
        #         shop_name_url_list.append((i.get('shop_name'),i.get('shop_comment_url')))
        # print(len(shop_name_url_list))
        # for i in range(len(shop_name_url_list)):
          try:
            # self.info_log(data='第%s个,%s' % (i + 1, shop_name_url_list[i][0]))
            # time.sleep(10)
            #self.fast_new_page(url="http://www.baidu.com", is_scroll_to_bottom=False)
            self.fast_new_page(url="http://www.dianping.com", is_scroll_to_bottom=False)
            time.sleep(20)
            self.fast_new_page(url="http://www.dianping.com/shop/19139636/review_all", is_scroll_to_bottom=False)

            time.sleep(30)
            # try:
            #  self.driver.find_element_by_link_text(link_text='默认排序').click();
            #  time.sleep(2)
            #  self.driver.find_element_by_link_text(link_text='最新点评').click();
            #  time.sleep(20)
            # except Exception:
            #     print("无最新点评")

                    ##随后进行点击标签和评阅
            self.until_click_no_next_page_by_partial_link_text(nextpagesetup=NextPageLinkTextSetup(link_text='下一页',
                        main_pagefunc=PageFunc(
                            func=self.from_page_get_data_list,
                            page=page_comment_1), pause_time=2))

            self.close_curr_page()

          except Exception:
            print("无元素")
            self.close_curr_page()

    def run_spider(self):
        try:
            #self.login()
            #self.get_shop_info_list()
            #self.get_shop_detail()
            #self.get_shop_address()
            self.get_shop_good_middle_bad_comment()


        except Exception:
            self.error_log(e='cookies失效!!!')