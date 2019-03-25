# -*- coding:utf-8 -*-

class ListCssSelector(object):
    def __init__(self, list_css_selector='', item_css_selector='', item_start=0, item_end=0):
        """
        在网页端： item_start和item_end的这两个参数的作用可以限制页面item列表的范围
        在移动端： item_start的作用就是元素向下移动最开始的序号，item_end在移动端没有任何含义，
        :param list_css_selector:
        :param item_css_selector:
        :param item_start:默认为0表示未设置,从1开始计数，这个参数有一个限制条件：必须在网页端长度已知的情况下使用，移动端不可以使用这个参数，即使设置了也不会生效
        :param item_end:默认为0表示未设置,位置可以和item_start重叠，item_end的使用的限制条件和移动端一样
        eg. 选取第五个和第六个可以是:item_start=5,item_end=6
        """
        self.list_css_selector = list_css_selector
        self.item_css_selector = item_css_selector
        self.item_start = item_start
        self.item_end = item_end

    def __str__(self):
        if not self.list_css_selector:
            return str(None)
        else:
            result = vars(self).copy()
            if not self.item_end:
                result.pop('item_end')
            if not self.item_css_selector:
                result.pop('item_css_selector')
            return str(result)

    def __eq__(self, other):
        if other is None:
            return not self.list_css_selector
        else:
            if vars(other) == vars(self):
                return True
            else:
                super.__eq__(self, other)