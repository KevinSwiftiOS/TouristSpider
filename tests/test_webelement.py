from selenium.webdriver.remote.webelement import WebElement

from spider.driver.base.tabsetup import TabSetup
from spider.driver.base.field import Field,Fieldlist
from spider.driver.base.page import Page,PageGroup
from spider.driver.base.listcssselector import ListCssSelector
from spider.driver.base.mongodb import Mongodb

fl = Fieldlist(Field(fieldname=12),Field(fieldname=13))
mongo = Mongodb(db='122',collection='12')
lcs = ListCssSelector(list_css_selector=12)
tab = TabSetup(url_name=12)
p = Page(name=122,fieldlist=fl,mongodb=mongo,listcssselector=lcs,tabsetup=tab)
p1 = Page(name=123,fieldlist=fl,mongodb=mongo,listcssselector=lcs,tabsetup=tab)
pg = PageGroup(p,p1)
print(next(pg))

