# -*- coding:utf-8 -*-
from .field import Fieldlist
from .tabsetup import TabSetup
from .listcssselector import ListCssSelector
from .mongodb import Mongodb

class Page(object):
    def __init__(self, name='', fieldlist=Fieldlist(), is_save=False, mongodb=Mongodb(), listcssselector=ListCssSelector(), tabsetup=TabSetup()):
        """

        :param name:
        :param fieldlist:
        :param is_save:
        :param mongodb:
        :param listcssselector:
        :param tabsetup:
        """
        self.name = name
        self.fieldlist = fieldlist
        self.is_save = is_save
        self.mongodb = mongodb
        self.listcssselector = listcssselector
        self.tabsetup = tabsetup

    def __str__(self):
        if not self.name or self.fieldlist == None:
            return str(None)
        else:
            result = {'name':self.name,'is_save':self.is_save}
            if self.fieldlist != None:
                result.setdefault('fieldlist',str(self.fieldlist))
            if self.is_save:
                result.setdefault('mongodb',str(self.mongodb))
            if self.listcssselector != None:
                result.setdefault('listcssselector',str(self.listcssselector))
            if self.tabsetup != None:
                result.setdefault('tabsetup',str(self.tabsetup))
            return str(result).replace('\\','')

    def __eq__(self, other):
        if other is None:
            return not self.name or self.fieldlist == None
        else:
            if vars(other) == vars(self):
                return True
            else:
                super.__eq__(self, other)

    def __iter__(self):
        return self

    def set_fieldlist(self, fieldlist):
        self.fieldlist = fieldlist

class PageGroup(object):
    def __init__(self, *args:Page):
        self.iter = iter(args)
        self.tuple = args

    def __iter__(self):
        return self

    def __next__(self):
        for i in self.iter:
            return i

    def __str__(self):
        return '(%s)'%','.join([str(i) for i in self.tuple])

    def __eq__(self, other):
        if other is None or other == []:
            return not self
        else:
            super.__eq__(self, other)

class PageFunc(object):
    #*args是非关键字参数，用于元组，**kw是关键字参数
    def __init__(self, func=None, **kwargs):
        self.func = func
        self.kwargs = kwargs

    def set_kwargs(self, **kwargs):
        self.kwargs = kwargs

    def run(self):
        if self.func:
            self.func(**self.kwargs)
        else:
            print('func为空!!!')

class NextPageCssSelectorSetup(object):
    def __init__(self, css_selector:str, stop_css_selector='', ele_timeout=1, pause_time=1, is_next=True, is_proxy=True, page=Page(), pre_pagefunc=PageFunc(), main_pagefunc=PageFunc(), after_pagefunc = PageFunc()):
        """

        :param css_selector:
        :param stop_css_selector:
        :param ele_timeout:
        :param pause_time:
        :param is_next:
        :param is_proxy:
        :param page:
        :param pre_pagefunc:
        :param main_pagefunc:
        :param after_pagefunc:
        """
        self.css_selector = css_selector
        self.stop_css_selector = stop_css_selector
        self.ele_timeout = ele_timeout
        self.pause_time = pause_time
        self.is_next = is_next
        self.is_proxy = is_proxy
        self.page = page
        self.pre_pagefunc = pre_pagefunc
        self.main_pagefunc = main_pagefunc
        self.after_pagefunc = after_pagefunc

    def set_main_pagefunc(self, pagefunc:PageFunc):
        self.main_pagefunc = pagefunc

    # def __str__(self):
    #     if not self.css_selector:
    #         return str(None)
    #     else:
    #         return str(vars(self))
    #
    # def __eq__(self, other):
    #     if other is None:
    #         return not self.css_selector
    #     else:
    #         if vars(other) == vars(self):
    #             return True
    #         else:
    #             super.__eq__(self, other)

class NextPageLinkTextSetup(object):
    def __init__(self, link_text:str, ele_timeout=1, pause_time=1, is_next=True, is_proxy=True, page=Page(), pre_pagefunc=PageFunc(), main_pagefunc=PageFunc(), after_pagefunc = PageFunc()):
        """

        :param link_text:
        :param ele_timeout:
        :param pause_time:
        :param is_next:
        :param is_proxy:
        :param page:
        :param pre_pagefunc:
        :param main_pagefunc:
        :param after_pagefunc:
        """
        self.link_text = link_text
        self.ele_timeout = ele_timeout
        self.pause_time = pause_time
        self.is_next = is_next
        self.is_proxy = is_proxy
        self.page = page
        self.pre_pagefunc = pre_pagefunc
        self.main_pagefunc = main_pagefunc
        self.after_pagefunc = after_pagefunc

    def set_main_pagefunc(self, pagefunc:PageFunc):
        self.main_pagefunc = pagefunc
