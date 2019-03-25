# -*- coding:utf-8 -*-

class TabSetup(object):
    def __init__(self, url_name='', click_css_selector='', pause_time=1, x_offset=8, y_offset=8, try_times=20):
        """
        爬虫标签页设置
        :param url_name:
        :param click_css_selector:
        :param pause_time:暂停时间
        :param x_offset:x轴方向页面偏移
        :param y_offset:y轴方向页面偏移
        :param try_times:尝试的次数
        """
        self.url_name = url_name
        self.click_css_selector = click_css_selector
        self.pause_time = pause_time
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.try_times = try_times

    def __str__(self):#url_name与click_css_selector两者只能存在一个
        if (not self.url_name and not self.click_css_selector) or (self.url_name and self.click_css_selector):
            return str(None)
        else:
            result = vars(self).copy()
            if self.url_name:
                result.pop('click_css_selector')
            elif self.click_css_selector:
                result.pop('url_name')
            return str(result)

    def __eq__(self, other):
        if other is None:
            return (self.url_name and self.click_css_selector) or (not self.url_name and not self.click_css_selector)
        else:
            if vars(other) == vars(self):
                return True
            else:
                super.__eq__(self, other)
