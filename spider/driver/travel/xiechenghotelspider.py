# -*- coding:utf-8 -*-

from spider.driver.travel.core.traveldriver import TravelDriver
from spider.driver.base.page import Page,NextPageCssSelectorSetup,PageFunc
from spider.driver.base.field import Fieldlist,Field,FieldName
from spider.driver.base.tabsetup import TabSetup
from spider.driver.base.listcssselector import ListCssSelector
from spider.driver.base.mongodb import Mongodb
import re
import time
import json
from pyquery import PyQuery

fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME,css_selector='li.hotel_item_name > h2 > a',regex=r'^[\d]*(.*)$',repl=r'\1'),
    Field(fieldname=FieldName.SHOP_URL,css_selector='li.hotel_item_name > h2 > a',attr='href',regex=r'^([^\?]*)?.*$',repl=r'\1'),
    # Field(fieldname=FieldName.SHOP_ID, css_selector='li.hotel_item_name > h2 > a', attr='href',regex=r'^[^\?\d]*([\d]*).html?.*$', repl=r'\1'),
    Field(fieldname=FieldName.SHOP_IMG, css_selector='li.pic_medal > div > a > img', attr='src'),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='li.hotel_item_name > p.hotel_item_htladdress'),
    Field(fieldname=FieldName.SHOP_GRADE,css_selector='li.hotel_item_judge.no_comment > div.hotelitem_judge_box > a > span.hotel_value'),
    # Field(fieldname=FieldName.SHOP_STATISFACTION_PERCENT,css_selector='li.hotel_item_judge.no_comment > div.hotelitem_judge_box > a > span.total_judgement_score > span'),
    Field(fieldname=FieldName.SHOP_RATE, css_selector='li.hotel_item_name > span', attr='innerHTML',regex=r'[^\d]*'),
    # Field(fieldname=FieldName.SHOP_ACTIVE_STATUS, css_selector='li.hotel_item_name > p.hotel_item_last_book'),
    Field(fieldname=FieldName.SHOP_PRICE,css_selector='span.J_price_lowList'),
    # Field(fieldname=FieldName.SHOP_CATEGORY_NAME, css_selector='li.hotel_item_name > p.medal_list > span'),
    Field(fieldname=FieldName.SHOP_COMMENT_NUM,css_selector='li.hotel_item_judge.no_comment > div.hotelitem_judge_box > a > span.hotel_judgement > span'),
    Field(fieldname=FieldName.SHOP_FEATURE,
          css_selector=''),
    # Field(fieldname=FieldName.SHOP_GRADE_TEXT,css_selector='li.hotel_item_judge.no_comment > div.hotelitem_judge_box > a > span.recommend'),
)

def get_recommend_all_room_dict(self, _str):
    p = PyQuery(_str)
    item_list = []
    for each in p('tr').items():
        if each.attr('class'):
            item_list.append(each)
    recommend_all_room_dict = {}
    all_room_list = []
    recommend_room = {}
    room_detail = {}
    room_info_list = []
    for item in item_list[::-1]:
        if item.attr('class') == 'clicked hidden':
            if room_detail and room_info_list:
                all_room_list.append({'room_detail': room_detail, 'room_info_list': room_info_list})
            room_detail = {}  # 重置
            room_info_list = []  # 重置
            room_detail.setdefault('房型', (lambda x: x.replace('\n', '').strip() if x else x)(item('div.hrd-title').text()))
            for i in item('ul.hrd-info-base-list>li').items():
                kv = i.text().split(':')
                if len(kv) == 1:
                    kv = i.text().split('：')
                if len(kv) == 1:
                    kv.append(kv[0])
                room_detail.setdefault(kv[0].strip(), kv[1].strip())
            for i in item('ul.hrd-allfac-list>li').items():
                kv = i.text().split(':')
                if len(kv) == 1:
                    kv = i.text().split('：')
                if len(kv) == 1:
                    kv.append(kv[0])
                room_detail.setdefault(kv[0].strip(), kv[1].strip())
        elif item.attr('class') == 'hidden':
            pass
        else:
            room_info = {}
            room_info.setdefault('满意度', (lambda x:x.replace('\n', '').strip() if x else x)(item('td.child_name').text()))
            room_info.setdefault('床型', (lambda x: x.replace('\n', '').strip() if x else x)(item('td.col3').text()))
            room_info.setdefault('早餐', (lambda x: x.replace('\n', '').strip() if x else x)(item('td.text_green.col4').text()))
            room_info.setdefault('宽带', (lambda x: x.replace('\n', '').strip() if x else x)(item('td.col5').text()))
            room_info.setdefault('入住人数', (lambda x: x.replace('\n', '').strip() if x else x)(item('td.col_person>span').attr('title')))
            room_info.setdefault('政策', (lambda x: x.replace('\n', '').strip() if x else x)(item('td.col_policy').text()))
            room_info.setdefault('房价', (lambda x: x.replace('\n', '').strip() if x else x)(item('td>div>span.base_price').text()))
            room_info_list.append(room_info)
    if room_detail and room_info_list:
        recommend_room = {'room_detail': room_detail, 'room_info_list': room_info_list}
    recommend_all_room_dict.setdefault('recommend_room', recommend_room)
    recommend_all_room_dict.setdefault('all_room', all_room_list)
    return json.dumps(recommend_all_room_dict, ensure_ascii=False)

def get_favourable_room(self, _str):
    favourable = {}
    room = {}
    p = PyQuery(_str)
    tr1 = p('tr.group_hotel.J_GroupRoom')
    room.setdefault('房型', (lambda x: x.strip() if x else x)(tr1('td.room_type').text()))
    room.setdefault('活动', (lambda x: x.strip() if x else x)(tr1('td.child_name').text()))
    room.setdefault('床型', tr1('td:nth-child(3)').text())
    room.setdefault('早餐', tr1('td:nth-child(4)').text())
    room.setdefault('宽带', tr1('td:nth-child(5)').text())
    room.setdefault('政策', tr1('td:nth-child(6)').text())
    room.setdefault('房价', tr1('td:nth-child(7)').text())
    favourable.setdefault('优惠房', room)
    tr2 = p('tr.rooms_sales.J_MeetingRooms')
    favourable.setdefault((lambda x: x.replace('\n', ',').strip() if x else '优惠')(tr2('td.room_type').text()),
                          (lambda x: x.replace('\n', '').strip() if x else x)(tr2('td:nth-child(2)').text()))
    tr3 = p('tr.hotel_spot.J_ShxDpSpot')
    package_list = []
    for i in tr3('td.room_type').items('div'):
        package_list.append({(lambda x: x if x else '房型')(tr3('p').text()): (
            lambda x: x.replace('\n', ',').strip() if x else x)(tr3('span').text())})
    package_list.append({(lambda x: x.replace('\n', ',').strip() if x else '套餐价')(
        tr3('td:nth-child(3)>p:nth-child(1)').text()): (lambda x: x.replace('\n', ',').strip() if x else x)(
        tr3('td:nth-child(3)>p:nth-child(2)').text())})
    favourable.setdefault((lambda x: x.replace('\n', ',').strip() if x else '优惠套餐')(tr3('td:nth-child(1)').text()),
                          package_list)
    return json.dumps(favourable, ensure_ascii=False)

def get_hotel_intro(self, _str):
    p = PyQuery(_str)
    hotel_intro_dict = {}
    # 酒店介绍
    intro = {}
    label = []
    for i in p('div.special_label').items('i'):
        label.append(i.text())
    intro.setdefault('label', label)
    info = []
    info_count = 0
    for i in p('div.special_info>ul').items('li'):
        info_count += 1
        info.append({(lambda x: re.sub(r'[^\u4e00-\u9fa5]', '', x) if x else '%s' % info_count)(i('span').text()): (
            lambda x: x if x else x)(i.text())})
    intro.setdefault('info', info)
    intro.setdefault('other',
                     (lambda x: x.replace('\n', ',').strip() if x else x)(p('div.htl_room_txt.text_3l').text()))
    hotel_intro_dict.setdefault('酒店介绍', intro)
    # 酒店设施
    facilities = {}
    for i in p('#J_htl_facilities > table > tbody').items('tr'):
        item = (lambda x: x if x else '')(i.text()).split('\n')
        facilities.setdefault(item[0], (lambda x: x[1:] if len(x) >= 2 else [''])(item))
    hotel_intro_dict.setdefault('酒店设施', facilities)
    # policy
    policy = {}
    for i in p('div.htl_info_table > table.detail_extracontent > tbody').items('tr'):
        item = (lambda x: x if x else '')(i.text()).split('\n')
        if '支付方式' in item[0]:
            item = item[:1]#初始化
            for j in i('div.card_cont_img').items('span'):
                p_pay = PyQuery(j.attr('data-params'))
                item.append(p_pay('div.jmp_bd').text().split('\'')[0])
            for j in i('span.detail_cardname').items():
                item.append(j.text().strip())
        policy.setdefault(item[0], (lambda x: x[1:] if len(x) >= 2 else [''])(item))
    hotel_intro_dict.setdefault('酒店政策', policy)
    return json.dumps(hotel_intro_dict, ensure_ascii=False)

def get_shop_statistics(self, _str):
    p = PyQuery(_str)
    statistics = {}
    # 点评
    dianping = []
    for i in p('div.comment_sumary_box>div.comment_total_score').items('span'):
        (lambda x: dianping.append(x.strip()) if x else '')(i.text())
    for i in p('div.comment_sumary_box>div.bar_score').items('p'):
        text = i.text()
        dianping.append({re.sub(r'[^\u4e00-\u9fa5]', '', text): re.sub(r'[^\d.]', '', text)})
    statistics.setdefault('点评', dianping)
    # 印象
    impression = []
    count = 0
    for i in p('div.user_impress').items('a'):
        count += 1
        text = i.text()
        impression.append({(lambda x: x if x else '第一个%s' % count)(re.sub(r'[^\u4e00-\u9fa5]', '', text)): re.sub(
            r'[^\d]', '', text)})
    statistics.setdefault('印象', impression)
    left = []
    for i in p('div.comment_box_bar_new.clearfix > div.bar_left').items('a'):
        left.append({re.sub(r'[^\u4e00-\u9fa5]*', '', i.text()): re.sub(r'[^\d]*', '', i.text())})
    statistics.setdefault('评论好评统计', left)
    right = []
    for i in p('div.comment_box_bar_new.clearfix > div.bar_right > select.select_room').text().split('\n')[1:]:
        right.append({re.sub(r'[^\u4e00-\u9fa5]*', '', i): re.sub(r'[^\d]*', '', i)})
    statistics.setdefault('评论房型统计', right)
    return json.dumps(statistics, ensure_ascii=False)

def get_around_facilities(self, _str):
    _str = re.sub(r'^.*<h2 class=\"detail_title\">周边设施</h2>(.*)$', r'\1', _str)
    p = PyQuery(_str)
    around = {}
    for i in p('div.htl_info_table > table > tbody').items('tr'):
        item = (lambda x: x if x else '')(i.text()).split('\n')
        if len(item) >= 2:
            around.setdefault(item[0], (lambda x: x[1:] if len(x) >= 2 else [''])(item))
    return json.dumps(around, ensure_ascii=False)

fl_shop2 = Fieldlist(
    # Field(fieldname=FieldName.SHOP_ROOM_RECOMMEND_ALL,css_selector='#hotelRoomBox', attr='innerHTML', filter_func=get_recommend_all_room_dict, pause_time=1, is_focus=True),
    # Field(fieldname=FieldName.SHOP_ROOM_FAVOURABLE,css_selector='#divDetailMain > div.htl_room_table',attr='innerHTML', filter_func=get_favourable_room, is_focus=True),
    # Field(fieldname=FieldName.SHOP_INTRO, css_selector='#hotel_info_comment > div',attr='innerHTML', filter_func=get_hotel_intro, is_focus=True),
    # Field(fieldname=FieldName.SHOP_PHONE, css_selector='#J_realContact', attr='data-real', regex='^([^<]*).*$', repl=r'\1', is_focus=True, is_info=True),
    # Field(fieldname=FieldName.SHOP_STATISTICS, css_selector='#commentList > div.detail_cmt_box',attr='innerHTML',filter_func=get_shop_statistics, is_focus=True),
    # Field(fieldname=FieldName.SHOP_AROUND_FACILITIES, css_selector='#hotel_info_comment > div', attr='innerHTML',filter_func=get_around_facilities, is_focus=True),
)

page_shop_1 = Page(name='携程酒店店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#hotel_list > div.hotel_new_list', item_css_selector='ul.hotel_item'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection),is_save=True)

page_shop_2 = Page(name='携程酒店店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector='li.hotel_price_icon > div.action_info > p > a'), mongodb=Mongodb(db=TravelDriver.db,collection=TravelDriver.shop_collection), is_save=False)

fl_comment1 = Fieldlist(
    Field(fieldname=FieldName.COMMENT_USER_NAME, css_selector='div.user_info.J_ctrip_pop > p.name'),
    Field(fieldname=FieldName.COMMENT_TIME, css_selector='div.comment_main > div.comment_txt > div.comment_bar > p > span', regex=r'[^\d-]*'),
    Field(fieldname=FieldName.SHOP_NAME, css_selector='#J_htl_info > div.name > h2.cn_n', is_isolated=True),
    Field(fieldname=FieldName.COMMENT_CONTENT, css_selector='div.comment_main > div.comment_txt > div.J_commentDetail'),
    # Field(fieldname=FieldName.COMMENT_USER_IMG, css_selector='div.user_info.J_ctrip_pop > p.head > span > img', attr='src'),
    # Field(fieldname=FieldName.COMMENT_USER_CHECK_IN, css_selector='div.comment_main > p > span.date'),
    # Field(fieldname=FieldName.COMMENT_USER_ROOM, css_selector='div.comment_main > p > a'),
    # Field(fieldname=FieldName.COMMENT_TYPE, css_selector='div.comment_main > p > span.type'),
    Field(fieldname=FieldName.COMMENT_SCORE, css_selector='div.comment_main > p > span.score', regex=r'[^\d.]*'),
    # Field(fieldname=FieldName.COMMENT_SCORE_TEXT, css_selector='div.comment_main > p > span.small_c', attr='data-value'),
    # Field(fieldname=FieldName.COMMENT_USER_NUM, css_selector='div.user_info.J_ctrip_pop > p.num'),
    # Field(fieldname=FieldName.COMMENT_PIC_LIST, list_css_selector='div.comment_txt > div.comment_pic', item_css_selector='div.pic > img', attr='src', timeout=0),
    # Field(fieldname=FieldName.COMMENT_REPLAY, css_selector='div.comment_main > div.htl_reply > p.text.text_other'),
)

page_comment_1 = Page(name='携程酒店评论列表', fieldlist=fl_comment1, listcssselector=ListCssSelector(list_css_selector='#divCtripComment > div.comment_detail_list > div.comment_block'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)

class XiechengHotelSpider(TravelDriver):

    def change_index_sort(self):
        try:
            self.info_log(data='评论按照入住时间排序')
            for i in range(3):
                self.until_scroll_to_center_select_by_visible_text_by_css_selector(
                    css_selector='#divCtripComment > div.comment_box_bar_new.clearfix > div.bar_right > select.select_sort',
                    text='入住时间排序')
                time.sleep(3)
        except Exception:
            self.error_log(e='点击入住时间排序出错!!!')

    def get_shop_info(self):
        try:
            shop_data_list = self.from_page_get_data_list(page=page_shop_1)
            nextpagesetup = NextPageCssSelectorSetup(css_selector='#divCtripComment > div.c_page_box > div > a.c_down', page=page_comment_1, pause_time=2, pre_pagefunc=PageFunc(func=self.change_index_sort))
            extra_pagefunc = PageFunc(func=self.get_newest_comment_data_by_css_selector, nextpagesetup=nextpagesetup)
            self.from_page_add_data_to_data_list(page=page_shop_2, pre_page=page_shop_1, data_list=shop_data_list, extra_pagefunc=extra_pagefunc)
        except Exception as e:
            self.error_log(e=str(e))

    def get_shop_info_list(self):
        self.driver.get('https://www.baidu.com')
        self.fast_new_page('http://hotels.ctrip.com/', is_scroll_to_bottom=False)
        self.until_scroll_to_center_send_text_by_css_selector(css_selector="#txtCity", text=self.data_region)
        time.sleep(3)
        self.until_scroll_to_center_send_enter_by_css_selector(css_selector="#txtCity")
        time.sleep(2)
        self.fast_click_same_page_by_css_selector(click_css_selector='#btnSearch')
        self.until_click_no_next_page_by_css_selector(nextpagesetup=NextPageCssSelectorSetup(css_selector='#downHerf.c_down',main_pagefunc=PageFunc(func=self.get_shop_info)))

    def run_spider(self):
        try:
            self.get_shop_info_list()
        except Exception as e:
            self.error_log(e=str(e))