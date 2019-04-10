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
import codecs
def get_shop_tag(self, _str):
    try:
        p = PyQuery(_str)
    except Exception:
        return None
    return json.dumps([i.text() for i in p('span').items()][1:], ensure_ascii=False)

def get_shop_rate(self, _str):
    return str(float((int(_str)/10)))

def get_shop_subtype_name(self, _str):
    return _str.strip()
def get_shop_feature(self,_str):
    return ""
def get_comment_url(self,_str):
    return _str + "/review_all"
fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='div.txt > div.tit > a > h4'),
    Field(fieldname=FieldName.SHOP_URL, css_selector='div.txt > div.tit > a', attr='href'),
    Field(fieldname=FieldName.SHOP_COMMENT_NUM, css_selector='div.txt > div.comment > a.review-num'),
    Field(fieldname=FieldName.SHOP_PRICE, css_selector='div.txt > div.comment > a.mean-price'),
    Field(fieldname=FieldName.SHOP_RATE, css_selector='div.txt > div.comment > span', attr='class', regex=r'[^\d]*', filter_func=get_shop_rate),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='div.txt > div.tag-addr > span.addr'),
    Field(fieldname=FieldName.SHOP_IMG,css_selector='div.pic > a > img',is_info=True),
    Field(fieldname=FieldName.SHOP_FEATURE,css_selector='',filter_func=get_shop_feature, is_info=True),
    Field(fieldname=FieldName.SHOP_GRADE,css_selector='div.txt > span > span:nth-child(1) > b',is_info=True),
Field(fieldname=FieldName.SHOP_COMMENT_URL, css_selector='div.txt > div.tit > a', attr='href',filter_func=get_comment_url, is_info=True)
)

page_shop_1 = Page(name='大众点评景点店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#shop-all-list > ul > li'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection), is_save=True)

def get_shop_time(self, _str):
    try:
        p = PyQuery(_str)
        shop_time = ''
        for i in p('p.info.info-indent').items():
            if '营业时间' in i.text():
                shop_time = i.text()
        return shop_time
    except Exception:
        return ''

def get_shop_promotion(self, _str):
    try:
        p = PyQuery(_str)
    except Exception:
        return None
    promotion = {}
    for i in p('div.group > div.item').items():
        info_list = i.text().split('\n')
        promotion.setdefault(info_list[0],info_list[1:])
    for i in p('div.group > a').items():
        info_list = i.text().split('\n')
        promotion.setdefault(info_list[-1],info_list[:-1])
    return json.dumps(promotion, ensure_ascii=False)

def get_shop_menu(self, _str):
    try:
        p = PyQuery(_str)
    except Exception:
        return None
    menu = {}
    tab_name_list = p('#shop-tabs > h2.mod-title > a').text().split(' ')
    count = 0
    for i in p('#shop-tabs > div').items():
        tab_content_list = []
        if 'shop-tab-recommend' in i.attr('class'):
            dish_recommend = {}
            for j in i('p.recommend-name > a.item').items():
                dish_recommend.setdefault(re.sub(r'([^(]+)\([^)]+\)', r'\1', j.text()).strip(), {'推荐数': re.sub(r'[^(]+\(([^)]+)\)', r'\1', j.text()).strip()})
            for j in i('ul.recommend-photo > li.item').items():
                try:
                    item = dish_recommend.get(j('p.name').text().strip())
                    item.setdefault('价格', j('span.price').text())
                    item.setdefault('图片', j('img').attr('src'))
                except Exception:
                    print('%s不存在'%j('p.name').text().strip())
            menu.setdefault(tab_name_list[count], dish_recommend)
        else:
            for j in p('div.container > a.item').items():
                tab_content_list.append({'标题': j.attr('title'), '链接': j.attr('href'), '图片': j('img').attr('data-src')})
            menu.setdefault(tab_name_list[count], tab_content_list)
        count += 1
    return json.dumps(menu, ensure_ascii=False)

def get_shop_statistics(self, _str):
    try:
        p = PyQuery(_str)
    except Exception:
        return None
    statistics_dict = dict()
    everyone = dict()
    for i in p('div.comment-condition.J-comment-condition.Fix > div.content > span.good.J-summary').items():
        everyone.setdefault(re.sub(r'[\d()]*', '', i.text()), int(re.sub(r'[^\d]*', '', i.text())))
    statistics_dict.setdefault('大家认为', everyone)
    evaluation = dict()
    for i in p('div.comment-filter-box.clearfix.J-filter > label.filter-item').items():
        if '全部' not in i.text():
            evaluation.setdefault(re.sub(r'[\d()]*', '', i.text()), int(re.sub(r'[^\d]*', '', i.text())))
    statistics_dict.setdefault('评价', evaluation)
    return json.dumps(statistics_dict, ensure_ascii=False)

fl_shop2 = Fieldlist(
    Field(fieldname=FieldName.SHOP_PHONE, css_selector='#basic-info > p', is_focus=True, is_info=True),
    Field(fieldname=FieldName.SHOP_TIME, css_selector='#basic-info > div.other.J-other.Hide', filter_func=get_shop_time,attr='innerHTML', is_focus=True, is_info=True),
    Field(fieldname=FieldName.SHOP_PROMOTION, css_selector='#promoinfo-wrapper', attr='innerHTML', filter_func=get_shop_promotion, is_focus=True),
    Field(fieldname=FieldName.SHOP_MENU, css_selector='#shoptabs-wrapper', attr='innerHTML', filter_func=get_shop_menu, is_focus=True),
    Field(fieldname=FieldName.SHOP_STATISTICS, css_selector='#summaryfilter-wrapper', attr='innerHTML', filter_func=get_shop_statistics, is_focus=True),
    Field(fieldname=FieldName.SHOP_COMMENT_URL, css_selector='#morelink-wrapper > p > a', attr='href', is_focus=True, is_info=True),
)

page_shop_2 = Page(name='大众点评景点店铺详情页面', fieldlist=fl_shop2)

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

def get_content(self, _str):
    p = PyQuery(_str)
    if p('div.review-words.Hide'):

        html = p('div.review-words.Hide').html().strip()
        try:
         str =  (get_target_text(html,
                              open('/home/lab421-ckq/文档/github /TouristSpider/style.css', 'r').read(),
                              codecs.open('/home/lab421-ckq/文档/github /TouristSpider/zf.svg', 'r',
                                          encoding='utf-8').read()));


        except Exception:
            str = "";
    else:

        html = p('div.review-words').html().strip()
        # 表明没有字符
        try:
         str = (get_target_text(html,
                               open('/home/lab421-ckq/文档/github /TouristSpider/style.css', 'r').read(),
                               codecs.open('/home/lab421-ckq/文档/github /TouristSpider/zf.svg', 'r',
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

    return self.shop_name_search_key(_str);

fl_comment1 = Fieldlist(

    Field(fieldname=FieldName.SHOP_NAME, css_selector='#review-list > div.review-list-container > div.review-shop-wrap > div.shop-info.clearfix > h1', is_isolated=True,is_info=True),
Field(fieldname=FieldName.SHOP_NAME_SEARCH_KEY, css_selector='#review-list > div.review-list-container > div.review-shop-wrap > div.shop-info.clearfix > h1',filter_func=get_shop_name_search_key, is_isolated=True,is_info=True),

    Field(fieldname=FieldName.COMMENT_USER_NAME, css_selector='div > div.dper-info > a',is_info=True),
    Field(fieldname=FieldName.COMMENT_TIME, css_selector='div > div.misc-info.clearfix > span.time',filter_func=get_comment_time,is_info=True),
    Field(fieldname=FieldName.COMMENT_CONTENT, css_selector='div.main-review',attr='innerHTML',filter_func=get_content, is_info=True),

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
          is_info=True),
    # Field(fieldname=FieldName.COMMENT_PIC_LIST, list_css_selector='div.main-review > div.review-pictures > ul', item_css_selector='li > a > img', attr='src', timeout=0),
)

page_comment_1 = Page(name='大众点评景点评论列表', fieldlist=fl_comment1, listcssselector=ListCssSelector(list_css_selector='#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.reviews-items > ul > li'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)

class DianpingSpotSpider(TravelDriver):

    def more_comment(self):
        while(True):
            self.is_ready_by_proxy_ip()
            self.switch_window_by_index(index=-1)
            self.deal_with_failure_page()
            self.until_scroll_to_center_click_by_css_selector(css_selector='#comment > div > div.comment > div.more-comment > a.dp-link')
            time.sleep(2)
            self.switch_window_by_index(index=-1)  # 页面选择
            if '验证中心' in self.driver.title:
                self.info_log(data='关闭验证页面!!!')
                self.close_curr_page()
            else:
                break
        # time.sleep(1)
        # while(True):
        #     self.until_scroll_to_center_click_by_css_selector(css_selector='#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.reviews-filter.clearfix > div.sort > a')
        #     time.sleep(1)
        #     self.is_ready_by_proxy_ip()
        #     self.until_scroll_to_center_click_by_css_selector(css_selector='#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.reviews-filter.clearfix > div.sort-selection-list > a')
        #     time.sleep(1)
        #     self.switch_window_by_index(index=-1)
        #     if '验证' in self.driver.title:#如果是验证页面
        #         self.driver.back()
        #     else:
        #         break

    def get_shop_comment(self):
        self.fast_new_page(url='http://www.baidu.com');
        shop_collcetion = Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection,
                                 ).get_collection()
        shop_name_url_list = list()
        for i in shop_collcetion.find(self.get_data_key()):
            if i.get('shop_comment_url'):
                shop_name_url_list.append((i.get('shop_name'),i.get('shop_comment_url')))
        for i in range(len(shop_name_url_list)):

            self.info_log(data='第%s个,%s'%(i+1, shop_name_url_list[i][0]))
            self.fast_new_page(url='http://www.baidu.com');
            self.shop_name =  shop_name_url_list[i][0]
            self.fast_new_page(url=shop_name_url_list[i][1],is_scroll_to_bottom=False)
            time.sleep(3)
            self.driver.find_element_by_link_text(link_text='默认排序').click();
            time.sleep(2)
            self.driver.find_element_by_link_text(link_text='最新点评').click();
            time.sleep(5)
            # while (True):
            #         self.is_ready_by_proxy_ip()
            #         self.switch_window_by_index(index=-1)
            #         self.deal_with_failure_page()
            #         self.fast_new_page(url=shop_name_url_list[i][1])
            #         time.sleep(1)
            #         self.switch_window_by_index(index=-1)  # 页面选择
            #         if '验证中心' in self.driver.title:
            #               self.info_log(data='关闭验证页面!!!')
            #               self.close_curr_page()
            #         else:
            #           break

            self.until_click_no_next_page_by_css_selector(nextpagesetup=NextPageCssSelectorSetup(
                css_selector='#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.bottom-area.clearfix > div > a.NextPage',
                stop_css_selector='#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.bottom-area.clearfix > div > a.NextPage.hidden',
                main_pagefunc=PageFunc(
                    func=self.from_page_get_data_list,
                    page=page_comment_1), pause_time=3))
            self.close_curr_page()

            # time_list = [i.get(FieldName.COMMENT_TIME) for i in nextpagesetup.page.mongodb.get_collection().find(
            #     self.merge_dict(self.data_key, {FieldName.SHOP_NAME: shop_name_url_list[i][0]}),
            #     {FieldName.COMMENT_TIME: 1, FieldName.ID_: 0})]
            # time_list.sort(reverse=True)
            # newest_time = (lambda tl: tl[0] if len(tl) >= 1 else '')(time_list)  # 最新的时间
            # self.debug_log(data='数据库评论最新时间:%s' % newest_time)
            # # self.from_page_get_comment_data_list(page=page_comment_1,is_effective=True,newest_time=newest_time)
            # # self.until_click_no_next_page_by_partial_link_text(nextpagesetup=NextPageLinkTextSetup(link_text='下一页',pause_time=5,  main_pagefunc=PageFunc(func=self.get_newest_comment_data_by_css_selector(), page=page_comment_1)))
            # self.until_click_no_next_page_by_partial_link_text(nextpagesetup=NextPageLinkTextSetup(link_text='下一页',pause_time=5,  main_pagefunc=PageFunc(func=self.from_page_get_comment_data_list,page=page_comment_1,is_effective=True,newest_time=newest_time)))
            #self.close_curr_page()

    def get_shop_detail(self):
        shop_collcetion = Mongodb(db=TravelDriver.db,collection=TravelDriver.shop_collection, host='10.1.17.25').get_collection()
        shop_url_set = set()
        for i in shop_collcetion.find(self.get_data_key()):
            shop_url_set.add(i.get(FieldName.SHOP_URL))
        count = 0
        for url in shop_url_set:
            print(count)
            count += 1
            while (True):
                self.is_ready_by_proxy_ip()
                time.sleep(5)
                self.switch_window_by_index(index=-1)
                self.deal_with_failure_page()
                self.fast_new_page(url=url)
                time.sleep(10)
                self.switch_window_by_index(index=-1)  # 页面选择
                if '验证中心' in self.driver.title:
                    self.info_log(data='关闭验证页面!!!')
                    self.close_curr_page()
                else:
                    break
            data = self.from_fieldlist_get_data(page=page_shop_2)
            self.update_data_to_mongodb(shop_collcetion,self.merge_dict(self.get_data_key(),{FieldName.SHOP_URL:url}), data)
            self.close_curr_page()

    def get_shop_info_list(self):
        # self.fast_click_first_item_page_by_partial_link_text(link_text='周边游')
        # time.sleep(30)
        # self.until_click_no_next_page_by_partial_link_text(NextPageLinkTextSetup(link_text='下一页',is_proxy=False,pause_time=20, main_pagefunc=PageFunc(self.from_page_get_data_list, page=page_shop_1)))
        #每次手动修改
        self.fast_new_page(url = 'http://www.dianping.com/search/keyword/2/35_%E6%95%85%E5%AE%AB/g33831')
        self.from_page_get_data_list(page=page_shop_1)

    def login(self):
        self.fast_new_page(url='http://www.baidu.com')
        self.fast_new_page(url='http://www.dianping.com')
        time.sleep(2)
        # self.until_scroll_to_center_send_text_by_css_selector(css_selector='#kw', text=self.data_region + self.data_website)
        # self.until_scroll_to_center_send_enter_by_css_selector(css_selector='#kw')
        # self.fast_click_first_item_page_by_partial_link_text(link_text=self.data_website)
        with open('./cookies/dianping_cookies.json', 'r', encoding='utf-8') as f:
            listCookies = json.loads(f.read())

        for cookie in listCookies:
            self.driver.add_cookie(cookie)
        self.close_curr_page()
        self.fast_new_page(url='http://www.dianping.com')
        # self.fast_click_first_item_page_by_partial_link_text(link_text=self.data_website)
        time.sleep(2)

    def run_spider(self):
        try:
            self.data_region_search_key = self.get_data_region_search_key()
            self.login()
            #self.get_shop_info_list()
            #self.get_shop_detail()
            self.get_shop_comment()
        except Exception:
            self.error_log(e='cookies失效!!!')