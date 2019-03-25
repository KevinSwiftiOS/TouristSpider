# -*- coding:utf-8 -*-

from spider.driver.base.driver import *
from spider.driver.base.field import FieldName
from spider.driver.base.mongodb import Mongodb
import sys
class DataRegionName(object):
    """
    数据区域名称
    """
    QIANDAOHU = '千岛湖'
    XIHU = '西湖'




DATAREGION_NAME_LIST = (lambda d:list({key:d[key] for key in d if '_' not in key}.values()))(vars(DataRegionName))

class WebsiteName(object):
    """
    旅游网站名称
    """
    XIECHENG = '携程'
    DINGPING = '大众点评'
    FLIGGY = '飞猪'
    QUNAR = '去哪儿'
    LVMAMA = '驴妈妈'
    TUNIU = '途牛'
    MAFENGWO = '马蜂窝'
    ELONG = '艺龙'
    BAIDU = '百度'
    GUANWANG = '官网'

WEBSITE_NAME_LIST = (lambda d:list({key:d[key] for key in d if '_' not in key}.values()))(vars(WebsiteName))

class DataSourceName(object):
    """
    数据来源名称
    """
    SPOT = '景点'
    HOTEL = '酒店'
    FOOD = '餐饮'
    SHOPPING = '购物'
    HEALTH = '健康'
    CAR = '爱车'
    ENTERTAINMENT = '娱乐'
    TRANSPORT = '交通'


DATASOURCE_NAME_LIST = (lambda d:list({key:d[key] for key in d if '_' not in key}.values()))(vars(DataSourceName))

class TravelSpiderName(object):
    """
    旅游网站爬虫的名称
    """
    XIECHENG_SPOT = WebsiteName.XIECHENG + DataSourceName.SPOT
    XIECHENG_HOTEL = WebsiteName.XIECHENG + DataSourceName.HOTEL
    DIANPING_SPOT = WebsiteName.DINGPING + DataSourceName.SPOT
    DIANPING_HOTEL = WebsiteName.DINGPING + DataSourceName.HOTEL
    DIANPING_FOOD = WebsiteName.DINGPING + DataSourceName.FOOD
    DIANPING_SHOPPING = WebsiteName.DINGPING + DataSourceName.SHOPPING
    DIANPING_HEALTH = WebsiteName.DINGPING + DataSourceName.HEALTH
    DIANPING_CAR = WebsiteName.DINGPING + DataSourceName.CAR
    DIANPING_ENTERTAINMENT = WebsiteName.DINGPING + DataSourceName.ENTERTAINMENT
    FLIGGY_SPOT = WebsiteName.FLIGGY + DataSourceName.SPOT
    FLIGGY_HOTEL = WebsiteName.FLIGGY + DataSourceName.HOTEL
    QUNAR_SPOT = WebsiteName.QUNAR + DataSourceName.SPOT
    QUNAR_HOTEL = WebsiteName.QUNAR + DataSourceName.HOTEL
    LVMAMA_SPOT = WebsiteName.LVMAMA + DataSourceName.SPOT
    LVMAMA_HOTEL = WebsiteName.LVMAMA + DataSourceName.HOTEL
    TUNIU_SPOT = WebsiteName.TUNIU + DataSourceName.SPOT
    TUNIU_HOTEL = WebsiteName.TUNIU + DataSourceName.HOTEL
    MAFENGWO_SPOT = WebsiteName.MAFENGWO + DataSourceName.SPOT
    MAFENGWO_HOTEL = WebsiteName.MAFENGWO + DataSourceName.HOTEL
    ELONG_HOTEL = WebsiteName.ELONG + DataSourceName.HOTEL
    BAIDU_FOOG = WebsiteName.BAIDU + DataSourceName.FOOD
    GUANWANG_SPOT = WebsiteName.GUANWANG + DataSourceName.SPOT #官网景点的爬去

class TravelDriver(Driver):
    host = '127.0.0.1'
    port = 27017
    db = 'dspider2'
    if sys.argv[2] == '官网':
        shop_collection = 'guanwang_shop'
        comments_collection = 'guanwang_comment'
    #数据库名字根据需求进行修改
    elif sys.argv[4] == '餐饮':

        shop_collection = 'restaurant_shop'
        comments_collection = 'local_comment'
    elif  sys.argv[4] == '景点':

        shop_collection = 'spot_shop'
        comments_collection = 'spot_comment'
    else:
        shop_collection = 'hotel_shop'
        comments_collection = 'hotel_comment'

    print(shop_collection)
    print(comments_collection)
    website_name = WebsiteName()
    website_name_list = WEBSITE_NAME_LIST
    datasource_name = DataSourceName()
    datasource_name_list = DATASOURCE_NAME_LIST
    travel_spider_name = TravelSpiderName()

    def __init__(self,isheadless=False,ismobile=False,isvirtualdisplay=False,isloadimages=False,isproxy=False,initial_proxy_ip='127.0.0.1',spider_id='',
                 data_website='',
                 data_region='',
                 data_source=''):
        """
        isvirtualdisplay的优先级高于isheadless
        :param isheadless:
        :param ismobile:
        :param isvirtualdisplay:
        :param isloadimages:
        :param isproxy:
        :param initial_proxy_ip:
        :param spider_id:
        :param data_website:
        :param data_region:
        :param data_source:
        """
        Driver.__init__(self,log_file_name=spider_id,ismobile=ismobile,isvirtualdisplay=isvirtualdisplay,isheadless=isheadless,isloadimages=isloadimages,isproxy=isproxy,initial_proxy_ip=initial_proxy_ip)
        if not data_website or not data_source or not data_region:
            self.error_log('data_website or data_source or data_region can not none!!!')
            raise ValueError
        self.data_website = data_website
        self.data_region = data_region
        self.data_source = data_source
        self.data_region_search_key = self.get_data_region_search_key()
        self.logger.debug('%s-%s-%s'%(self.data_website,self.data_region,self.data_source))
        self.data_key = {
            FieldName.DATA_WEBSITE: self.data_website,
            FieldName.DATA_REGION: self.data_region,
            FieldName.DATA_SOURCE: self.data_source,
        }

    def from_page_get_comment_data_list(self, page:Page, newest_time:str, is_effective=True):
        if not newest_time:#如果当前没有评论
            self.debug_log(data='数据库目前没有评论数据,直接保存到数据库!!!')
            self.from_page_get_data_list(page=page)
        else:
            comment_data_list = self.from_page_get_data_list(page=page)
            time_list = [i.get(FieldName.COMMENT_TIME) for i in comment_data_list]
            time_list.sort()#取出最旧的数据
            curr_time = (lambda tl:tl[0] if len(tl) >=1 else '')(time_list)#当前最新时间
            self.debug_log(data='当前最新评论的最旧时间是：%s'%curr_time)
            if curr_time < newest_time and is_effective:
                self.info_log(data='当前的评论数据不是最近更新的,不用继续往下爬虫!!!')
                raise ValueError
    #获取对应文字
    def get_data_region_search_key(self):

        search_keys = [
            '千岛湖', '西湖', '西溪', '溪口', '乌镇', '西塘', '横店', '江郎山', '雁荡山', '普陀山',
            '南浔', '神仙居', '天台山', '根宫', '鲁迅', '南湖', '黄山', '三清山'
        ];
        for i,search_key in enumerate(search_keys):
            if(search_key in sys.argv[3]):
                return search_key
        return '千岛湖';
    def shop_name_search_key(self,shop_name):


        shop_name_search_keys = [
            '中心湖', '梅峰', '龙山岛', '月光岛', '渔乐岛', '东南湖', '黄山尖', '天池岛', '桂花岛', '蜜山岛',
            '文渊狮城', '石林', '九咆界', '下姜', '森林氧吧', '龙川', '芹川', '秘境', "仙人谷",
            "钓鱼岛", "白云溪"
        ];
        if(self.get_data_region_search_key() == '千岛湖'):

            for i, search_key in enumerate(shop_name_search_keys):
                if (search_key in shop_name):

                    return search_key
            return '中心湖';
        return '';


    def get_city_from_region_CHN(self,_str):
        dic = {'西湖': '杭州', '千岛湖': '杭州', '溪口': '宁波'}

        for key in dic:
            if key == _str:

                return dic[key]

    def get_city_from_region_ENG(self, _str):
        dic = {'西湖': '/hangzhou/', '千岛湖': '/hangzhou/', '溪口': '/ningbo/'}

        for key in dic:
            if key == _str:

                return dic[key]
    def get_newest_comment_data_by_css_selector(self, nextpagesetup:NextPageCssSelectorSetup, shop_name_css_selector='', is_effective=True):

        data_website = sys.argv[2],

        data_source = sys.argv[4]

        if(data_website[0] == '马蜂窝'
) and data_source == '景点':

            #body > div.wrapper > div.col-main > div.m-box.m-details.clearfix > div.title.clearfix > div > h1
            shop_name_css_selector ='body > div.wrapper > div.col-main > div.m-box.m-details.clearfix > div.title.clearfix > div > h1'

        elif data_website[0] == '去哪儿' and data_source == '酒店':
            shop_name_css_selector = '#detail_pageHeader > h2 > span'
        field_shop_name = None
        for field in nextpagesetup.page.fieldlist:
            if field.fieldname == FieldName.SHOP_NAME:
                field_shop_name = field
                break
        if field_shop_name:
            try:
                shop_name = self.until_presence_of_element_located_by_css_selector(css_selector=field_shop_name.css_selector, timeout=field_shop_name.timeout).text
            except Exception:
                self.warning_log(e='SHOP_NAME应该是is_isolated=True')
                if shop_name_css_selector:
                    try:
                        shop_name = self.until_presence_of_element_located_by_css_selector(css_selector=shop_name_css_selector, timeout=field_shop_name.timeout).text

                    except Exception:
                        self.error_log(e='shop_name_css_selector有错!!!')
                        self.driver.quit()
                        sys.exit()
                else:
                    self.error_log(e='shop_name_css_selector没有填写!!!')
                    self.driver.quit()
                    sys.exit()
            time_list = [i.get(FieldName.COMMENT_TIME) for i in nextpagesetup.page.mongodb.get_collection().find(self.merge_dict(self.data_key, {FieldName.SHOP_NAME:shop_name}), {FieldName.COMMENT_TIME:1,FieldName.ID_:0})]
            time_list.sort(reverse=True)
            newest_time = (lambda tl:tl[0] if len(tl) >=1 else '')(time_list)#最新的时间
            self.debug_log(data='数据库评论最新时间:%s'%newest_time)
            nextpagesetup.set_main_pagefunc(pagefunc=PageFunc(func=self.from_page_get_comment_data_list, page=nextpagesetup.page, newest_time=newest_time, is_effective=is_effective))
            try:
                self.until_click_no_next_page_by_css_selector(nextpagesetup=nextpagesetup)
            except Exception:
                pass
        else:
            self.error_log(e='%s字段不存在!!!'%FieldName.SHOP_NAME)
            raise ValueError

