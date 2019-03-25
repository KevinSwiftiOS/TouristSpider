# -*- coding:utf-8 -*-

class FieldType(object):
    NONE = None
    KEY_STR = 'key_str'
    STR = 'str'
    LIST_STR = 'list_str'
    INT = 'int'
    FLOAT = 'float'

class FieldName(object):
    NONE = None
    SHOP_ELE = 'shop_ele'  # 店铺页面元素
    ID_ = '_id'#mongodb的默认id
    SUM = 'sum'#求和

    DATA_WEBSITE = 'data_website'#数据的来自的网站
    DATA_REGION = 'data_region'#数据来自的景点
    DATA_SOURCE = 'data_source'#数据来自的分类
    CRAWL_TIME = 'crawl_time'#爬虫的时间
    SUBTYPE_NAME = 'subtype_name'#子类名
    SUBTYPE_URL = 'subtype_url'#子类的链接

    SHOP_COMMENT_NUM_SUM = 'shop_comment_num_sum'#店铺评论数目求和
    SHOP_NAME = 'shop_name'#店铺名
    SHOP_URL = 'shop_url'#店铺链接
    SHOP_CURR_URL = 'shop_curr_url'#实时链接
    SHOP_ID = 'shop_id'#店铺编号
    SHOP_IMG = 'shop_img'#店铺的图片
    SHOP_COMMENT_NUM = 'shop_comment_num'#店铺的评论数量
    SHOP_TIME = 'shop_time'#店铺的营业时间
    SHOP_PHONE = 'shop_phone'#店铺的电话
    SHOP_RATE = 'shop_rate'#店铺的等级
    SHOP_GRADE = 'shop_grade'#店铺的评分
    SHOP_GRADE_TEXT = 'shop_grade_text'#店铺文字评分
    SHOP_VOLUME = 'shop_volume'#店铺的销量
    SHOP_PRICE = 'shop_price'#店铺的平均价格
    SHOP_ADDRESS = 'shop_address'#店铺的地址
    SHOP_INTRO = 'shop_intro'#店铺的简介
    SHOP_CATEGORY_NAME = 'shop_category_name'#店铺类别
    SHOP_TITLE = 'shop_title'#店铺标语
    SHOP_STATISTICS = 'shop_statistics'#店铺评论统计
    SHOP_DETAIL_URL = 'shop_detail_url'#店铺详情页面链接
    SHOP_ACTIVE_STATUS = 'shop_active_status'#店铺的活动状态
    SHOP_DISTANCE = 'shop_distance'#店铺距离景点的距离
    SHOP_STATISFACTION_PERCENT = 'shop_satisfaction_percent'#店铺的满意度
    SHOP_YEAR = 'shop_year'#店铺的年份
    SHOP_ROOM_RECOMMEND_ALL = 'shop_room_recommend_all'#推荐和所有房型
    SHOP_ROOM_FAVOURABLE = 'shop_room_favourable'#优惠房型
    SHOP_AROUND_FACILITIES = 'shop_around_facilities'#周边设施
    SHOP_FACILITIES = 'shop_facilities'  # 店铺设施
    SHOP_RANK = 'shop_rank'#店铺排名
    SHOP_TRAFFIC = 'shop_traffic'#位置交通
    SHOP_TAG = 'shop_tag'#店铺标签
    SHOP_PACKAGE = 'shop_package'#店铺套餐
    SHOP_FEATURE = 'shop_feature'#店铺特色
    SHOP_FLAG = 'shop_flag' #是否成功爬取
    SHOP_TICKET = 'shop_ticket'#店铺门票
    SHOP_RESERVE = 'shop_reserve'#店铺预定
    SHOP_INFO = 'shop_info'#店铺信息
    SHOP_RECOMMEND_DISH = 'shop_recommend_dish'#推荐菜品
    SHOP_PROMOTION = 'shop_promotion'#优惠促销
    SHOP_MENU = 'shop_menu'#店铺菜单
    SHOP_COMMENT_URL = 'shop_comment_url'#评论链接
    SHOP_SCORE = 'shop_score' #评论成绩
    SHOP_COOK_STYLE = 'shop_cook_style' #菜系
    SHOP_LNG = 'shop_lng' #店铺经度
    SHOP_LAT = 'shop_lat' #店铺纬度
    SHOP_SITE = 'shop_site' #店铺商区
    SHOP_TASTE = 'shop_taste' #店铺口味
    SHOP_ENV = 'shop_env' #店铺环境
    SHOP_SERVICE = 'shop_service'  # 店铺服务
    SHOP_AREA = 'shop_area' #店铺分布的地理位置
    SHOP_DES = 'shop_des' #店铺描述
    BAIDU_SPIDER_STEP = 'baidu_spider_step' #百度地图爬的步骤

    COMMENT_USER_NAME = 'comment_user_name'#评论者的名字
    COMMENT_USER_ID = 'comment_user_id'#评论者的编号
    COMMENT_USER_IMG = 'comment_user_img'#评论者的头像
    COMMENT_USER_RATE = 'comment_user_rate'#评论者的等级
    COMMENT_USER_CHECK_IN = 'comment_user_check_in'#评论者的入住时间
    COMMENT_USER_ROOM = 'comment_user_room'#评论者的入住房间
    COMMENT_SCORE = 'comment_score'#评论者的评分
    COMMENT_USER_NUM = 'comment_user_num'#用户评论
    COMMENT_TIME = 'comment_time'#评论发表的时间
    COMMENT_DATE = 'comment_date'#店铺入住日期
    COMMENT_CONTENT = 'comment_content'#评论的内容

    COMMENT_URL = 'comment_url'#评论链接
    COMMENT_RATE_TAG = 'comment_rate_tag'#评论的评分标签
    COMMENT_PIC_LIST = 'comment_pic_list'#评论的照片列表
    COMMENT_GRADE = 'comment_grade'#评论的评分
    COMMENT_USER_URL = 'comment_user_url'  # 评论者的主页链接
    COMMENT_SCORE_TEXT = 'comment_score_text'#评论的文字打分
    COMMENT_ROOM = 'comment_room'#评论的酒店房间
    COMMENT_TYPE = 'comment_type'#评论的类型
    COMMENT_REPLAY = 'comment_replay'#评论回复
    COMMENT_RATE = 'comment_rate'#评论等级
    COMMENT_CATEGORY = 'comment_category' #评论类别

    COMMENT_YEAR = 'comment_year' #评论年份
    COMMENT_SEASON = 'comment_season' #评论季度
    COMMENT_MONTH = 'comment_month' #评论月份
    COMMENT_WEEK = 'comment_week' #评论周
    COMMENT_DAY = 'comment_day' #评论天

    COMMENT_TASTE_SCORE = 'comment_taste_score' #评论的口味
    COMMENT_ENV_SCORE = 'comment_env_score' #评论的环境
    COMMENT_SERVICE_SCORE = 'comment_service_score' #评论的服务
    COMMENT_LIKE_NUM = 'comment_like_num'  # 评论的点赞数
    COMMENT_REPLY_NUM = 'comment_reply_num'  # 评论的回复数量
    COMMENT_COLLECT_NUM = 'comment_collect_num' #评论的收藏数
    COMMENT_COMPLAIN_NUM = 'comment_complain_num' #评论的投诉数
    COMMENT_AVERAGE_PRICE = 'comment_average_price' #人均价格

    DATA_REGION_SEARCH_KEY = 'data_region_search_key' #景区关键字搜索
    SHOP_NAME_SEARCH_KEY = 'shop_name_search_key' #景点店铺关键字搜索

FIELD_NAME_TYPE = {
    FieldName.NONE : FieldType.NONE,
    FieldName.SHOP_NAME : FieldType.KEY_STR,
    FieldName.SHOP_ID : FieldType.STR,
    FieldName.SHOP_IMG : FieldType.STR,
    FieldName.SHOP_URL : FieldType.KEY_STR,
    FieldName.SHOP_CURR_URL : FieldType.STR,
    FieldName.SHOP_COMMENT_NUM : FieldType.INT,
    FieldName.SHOP_RATE : FieldType.STR,
    FieldName.SHOP_GRADE : FieldType.FLOAT,
    FieldName.SHOP_GRADE_TEXT : FieldType.STR,
    FieldName.SHOP_VOLUME : FieldType.INT,
    FieldName.SHOP_TIME : FieldType.STR,
    FieldName.SHOP_PHONE : FieldType.STR,
    FieldName.SHOP_PRICE : FieldType.FLOAT,
    FieldName.SHOP_ADDRESS : FieldType.STR,
    FieldName.SHOP_INTRO : FieldType.STR,
    FieldName.SHOP_CATEGORY_NAME : FieldType.STR,
    FieldName.SHOP_TITLE : FieldType.STR,
    FieldName.SHOP_STATISTICS : FieldType.STR,
    FieldName.SHOP_DETAIL_URL : FieldType.STR,
    FieldName.SHOP_ACTIVE_STATUS : FieldType.STR,
    FieldName.SHOP_DISTANCE : FieldType.STR,
    FieldName.SHOP_STATISFACTION_PERCENT : FieldType.FLOAT,
    FieldName.SHOP_YEAR : FieldType.STR,
    FieldName.SHOP_ROOM_RECOMMEND_ALL : FieldType.STR,
    FieldName.SHOP_ROOM_FAVOURABLE : FieldType.STR,
    FieldName.SHOP_AROUND_FACILITIES : FieldType.STR,
    FieldName.SHOP_FACILITIES : FieldType.STR,
    FieldName.SHOP_RANK : FieldType.STR,
    FieldName.SHOP_TRAFFIC : FieldType.STR,
    FieldName.SHOP_TAG : FieldType.STR,
    FieldName.SHOP_PACKAGE : FieldType.STR,
    FieldName.SHOP_FEATURE : FieldType.STR,
    FieldName.SHOP_SERVICE : FieldType.STR,
    FieldName.SHOP_TICKET : FieldType.STR,
    FieldName.SHOP_RESERVE : FieldType.STR,
    FieldName.SHOP_INFO : FieldType.STR,
    FieldName.SHOP_RECOMMEND_DISH : FieldType.STR,
    FieldName.SHOP_PROMOTION : FieldType.STR,
    FieldName.SHOP_MENU : FieldType.STR,
    FieldName.SHOP_COMMENT_URL : FieldType.STR,
    FieldName.SHOP_SCORE:FieldType.STR,
    FieldName.SHOP_COOK_STYLE:FieldType.STR,
    FieldName.SHOP_LNG:FieldType.STR,
    FieldName.SHOP_LAT:FieldType.STR,
    FieldName.SHOP_SITE:FieldType.STR,
    FieldName.SHOP_TASTE:FieldType.STR,
    FieldName.SHOP_ENV:FieldType.STR,
    FieldName.SHOP_FLAG:FieldType.STR,  #是否成功爬取
    FieldName.SHOP_AREA:FieldType.STR, #爬取地区
    FieldName.SHOP_DES:FieldType.STR, #店铺描述
    FieldName.BAIDU_SPIDER_STEP:FieldType.STR,#爬取的是第几步


    FieldName.COMMENT_USER_NAME : FieldType.KEY_STR,
    FieldName.COMMENT_TIME : FieldType.KEY_STR,
    FieldName.COMMENT_USER_ID : FieldType.STR,
    FieldName.COMMENT_USER_IMG : FieldType.STR,
    FieldName.COMMENT_DATE : FieldType.STR,
    FieldName.COMMENT_USER_CHECK_IN : FieldType.STR,
    FieldName.COMMENT_USER_ROOM : FieldType.STR,
    FieldName.COMMENT_SCORE: FieldType.FLOAT,
    FieldName.COMMENT_USER_NUM: FieldType.STR,
    FieldName.COMMENT_CONTENT : FieldType.STR,
    FieldName.COMMENT_USER_RATE : FieldType.STR,

    FieldName.COMMENT_URL : FieldType.STR,
    FieldName.COMMENT_RATE_TAG : FieldType.STR,
    FieldName.COMMENT_PIC_LIST : FieldType.LIST_STR,
    FieldName.COMMENT_GRADE : FieldType.FLOAT,
    FieldName.COMMENT_USER_URL : FieldType.STR,
    FieldName.COMMENT_SCORE_TEXT : FieldType.STR,
    FieldName.COMMENT_ROOM : FieldType.STR,
    FieldName.COMMENT_TYPE : FieldType.STR,
    FieldName.COMMENT_REPLAY : FieldType.STR,
    FieldName.COMMENT_RATE : FieldType.STR,
    FieldName.COMMENT_CATEGORY:FieldType.STR,
    FieldName.COMMENT_YEAR:FieldType.STR, # 评论年份
    FieldName.COMMENT_SEASON:FieldType.STR,  # 评论季度
    FieldName.COMMENT_MONTH:FieldType.STR,  # 评论月份
    FieldName.COMMENT_WEEK:FieldType.STR,  # 评论周
    FieldName.COMMENT_DAY :FieldType.STR,  # 评论天
    FieldName.DATA_REGION_SEARCH_KEY :FieldType.STR, # 景区关键字搜索
    FieldName.SHOP_NAME_SEARCH_KEY:FieldType.STR, #景点关键字搜索

    FieldName.COMMENT_TASTE_SCORE:FieldType.STR,#评论的口味分数
    FieldName.COMMENT_ENV_SCORE:FieldType.STR, #评论的环境分数
    FieldName.COMMENT_SERVICE_SCORE:FieldType.STR,#评论的服务分数
    FieldName.COMMENT_REPLY_NUM: FieldType.INT, #回应数
    FieldName.COMMENT_LIKE_NUM: FieldType.INT,#点赞数
    FieldName.COMMENT_COLLECT_NUM:FieldType.INT,#收藏数
    FieldName.COMMENT_COMPLAIN_NUM:FieldType.INT,#投诉数
    FieldName.COMMENT_AVERAGE_PRICE:FieldType.INT #评论人均价格
}

FIELD_NAME_ZH = {
    FieldName.CRAWL_TIME:'爬虫时间',
    FieldName.SUBTYPE_NAME:'子类名称',
    FieldName.SUBTYPE_URL:'子类链接',

    FieldName.SHOP_NAME : '店铺名称',
    FieldName.SHOP_URL : '店铺链接',
    FieldName.SHOP_CURR_URL : '实时链接',
    FieldName.SHOP_ID : '店铺编号',
    FieldName.SHOP_IMG : '店铺图片',
    FieldName.SHOP_COMMENT_NUM : '评论数量',
    FieldName.SHOP_TIME : '营业时间',
    FieldName.SHOP_PHONE : '联系方式',
    FieldName.SHOP_RATE : '店铺等级',
    FieldName.SHOP_GRADE : '店铺评分',
    FieldName.SHOP_GRADE_TEXT : '文字评分',
    FieldName.SHOP_VOLUME : '店铺销量',
    FieldName.SHOP_PRICE : '平均价格',
    FieldName.SHOP_ADDRESS : '店铺地址',
    FieldName.SHOP_INTRO : '店铺简介',
    FieldName.SHOP_CATEGORY_NAME : '店铺类别',
    FieldName.SHOP_TITLE : '店铺标语',
    FieldName.SHOP_STATISTICS : '评论统计',
    FieldName.SHOP_DETAIL_URL : '详情链接',
    FieldName.SHOP_ACTIVE_STATUS : '店铺状态',
    FieldName.SHOP_DISTANCE : '店铺距离',
    FieldName.SHOP_STATISFACTION_PERCENT : '满意指数',
    FieldName.SHOP_YEAR : '店铺年份',
    FieldName.SHOP_ROOM_RECOMMEND_ALL : '房型列表',
    FieldName.SHOP_ROOM_FAVOURABLE : '优惠房型',
    FieldName.SHOP_AROUND_FACILITIES : '周边设施',
    FieldName.SHOP_FACILITIES : '店铺设施',
    FieldName.SHOP_RANK : '店铺排名',
    FieldName.SHOP_TRAFFIC : '位置交通',
    FieldName.SHOP_TAG : '店铺标签',
    FieldName.SHOP_PACKAGE : '店铺套餐',
    FieldName.SHOP_FEATURE : '店铺特色',
    FieldName.SHOP_SERVICE : '店铺服务',
    FieldName.SHOP_TICKET : '店铺门票',
    FieldName.SHOP_RESERVE : '店铺预定',
    FieldName.SHOP_INFO : '店铺信息',
    FieldName.SHOP_RECOMMEND_DISH : '推荐餐饮',
    FieldName.SHOP_PROMOTION : '优惠促销',
    FieldName.SHOP_MENU : '店铺菜单',
    FieldName.SHOP_COMMENT_URL : '评论链接',
    FieldName.SHOP_SCORE:'评论分数',
    FieldName.SHOP_COOK_STYLE:'店铺菜系',
    FieldName.SHOP_LNG:'店铺经度',
    FieldName.SHOP_LAT:'店铺纬度',
    FieldName.SHOP_SITE:'店铺地区',
    FieldName.SHOP_TASTE : '店铺口味',
    FieldName.SHOP_SERVICE : '店铺环境',
    FieldName.SHOP_FLAG:'是否爬取',
    FieldName.BAIDU_SPIDER_STEP:'百度爬取的是第几步',
    FieldName.SHOP_AREA:'百度爬取的地区',
    FieldName.SHOP_DES:'店铺描述',

    FieldName.COMMENT_USER_NAME : '用户名称',
    FieldName.COMMENT_USER_ID : '用户编号',
    FieldName.COMMENT_USER_IMG : '用户头像',
    FieldName.COMMENT_USER_RATE : '用户等级',
    FieldName.COMMENT_USER_CHECK_IN : '入住时间',
    FieldName.COMMENT_USER_ROOM : '入住房间',
    FieldName.COMMENT_SCORE : '用户评分',
    FieldName.COMMENT_USER_NUM: '用户评论',
    FieldName.COMMENT_TIME : '发表时间',
    FieldName.COMMENT_DATE : '入住日期',
    FieldName.COMMENT_CONTENT : '评论内容',
    FieldName.COMMENT_URL : '评论链接',
    FieldName.COMMENT_RATE_TAG : '评分标签',
    FieldName.COMMENT_PIC_LIST : '照片列表',
    FieldName.COMMENT_GRADE : '评论评分',
    FieldName.COMMENT_USER_URL : '用户链接',
    FieldName.COMMENT_SCORE_TEXT : '文字打分',
    FieldName.COMMENT_ROOM : '评论房间',
    FieldName.COMMENT_TYPE : '评论类型',
    FieldName.COMMENT_REPLAY : '评论回复',
    FieldName.COMMENT_RATE : '评论等级',
    FieldName.COMMENT_YEAR:'评论年份', # 评论年份
    FieldName.COMMENT_SEASON:'评论季度',  # 评论季度
    FieldName.COMMENT_MONTH:'评论月份',  # 评论月份
    FieldName.COMMENT_WEEK:'评论周',  # 评论周
    FieldName.COMMENT_DAY :'评论天',  # 评论天
    FieldName.DATA_REGION_SEARCH_KEY :'关键字搜索', # 景区关键字搜索
    FieldName.SHOP_NAME_SEARCH_KEY:'景点关键字搜索',
    FieldName.COMMENT_CATEGORY:'评论类别', #评论类别
    FieldName.COMMENT_TASTE_SCORE: "评论口味评分",  # 评论的口味分数
    FieldName.COMMENT_ENV_SCORE: "评论环境评分",  # 评论的环境分数
    FieldName.COMMENT_SERVICE_SCORE: "评论服务评分",  # 评论的服务分数
    FieldName.COMMENT_REPLY_NUM: "评论回复个数",  # 回应数
    FieldName.COMMENT_LIKE_NUM: "评论点赞个数",  # 点赞数
    FieldName.COMMENT_COLLECT_NUM: "评论收藏个数",  # 收藏数
    FieldName.COMMENT_COMPLAIN_NUM: "评论投诉个数" , # 投诉数
    FieldName.COMMENT_AVERAGE_PRICE:"评论中人均价格",#人均价
}

#offset是每次为了寻找元素偏移的距离
#try_times是为了寻找元素偏移的次数
class Field(object):
    def __init__(self, fieldname='', css_selector='', attr='', regex='', repl='', timeout=1, list_css_selector='', item_css_selector='', pause_time=0, is_focus=False, is_debug=False, is_info=False, is_error=False, is_isolated=False, filter_func=None,second_css_selector = ''):
        """

        :param fieldname:字段的名称
        :param css_selector:字段的css选择器
        :param attr:字段的html属性
        :param regex:字段的正则匹配表达式
        :param repl:字段的正则替换表达式
        :param timeout:获取字段的超时时间
        :param list_css_selector:列表字段的css选择器
        :param item_css_selector:列表字段里面字段的css选择器
        :param pause_time:暂停的时间
        :param is_focus:是否将元素移到页面中间
        :param is_debug:表示是否输出调试信息
        :param is_info:表示是否显示字段的提取结果
        :param is_error:表示是否输出错误日志
        :param is_isolated:表示爬虫字段的css_selector是否孤立
        :param filter_func:过滤函数
        """
        self.fieldname = fieldname
        self.fieldtype = (lambda x:FIELD_NAME_TYPE.get(x) if FIELD_NAME_TYPE.get(x) else FieldType.STR)(fieldname)
        self.css_selector = css_selector
        self.attr = attr
        self.regex = regex
        self.repl = repl
        self.timeout = timeout
        self.list_css_selector = list_css_selector
        self.item_css_selector = item_css_selector
        self.pause_time = pause_time
        self.is_focus = is_focus
        self.is_debug = is_debug
        self.is_info = is_info
        self.is_error = is_error
        self.is_isolated = is_isolated
        #过滤函数默认有两个参数self,_str
        self.filter_func = filter_func
        self.second_css_selector = second_css_selector

    def __str__(self):
        if not self.fieldname:
            return str(None)
        else:
            result = vars(self).copy()
            if not self.fieldtype:
                result.pop('fieldtype')
            if not self.css_selector:
                result.pop('css_selector')
            if not self.attr:
                result.pop('attr')
            if not self.regex:
                result.pop('regex')
            if not self.repl:
                result.pop('repl')
            if not self.list_css_selector:
                result.pop('list_css_selector')
            if not self.item_css_selector:
                result.pop('item_css_selector')
            if not self.filter_func:
                result.pop('filter_func')
            return str(result)

    def __eq__(self, other):
        if other is None:
            return not self.fieldname
        else:
            if vars(other) == vars(self):
                return True
            else:
                super.__eq__(self, other)

class Fieldlist(list):
    def __init__(self, *args:Field):
        list.__init__(self,list(args))
    def append(self,field=Field()):
        list.append(self,field)
    def extend(self,*args:Field):
        list.extend(self,list(args))
    def __str__(self):
        return '[%s]'%','.join([str(l) for l in self])
    def __eq__(self, other):
        if other is None or other == []:
            return not self
        else:
            super.__eq__(self, other)

