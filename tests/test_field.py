# -*- coding:utf-8 -*-

from spider.driver.base.field import Field,Fieldlist,FIELD_NAME_TYPE,FieldType

a = (lambda x:FIELD_NAME_TYPE.get(x) if FIELD_NAME_TYPE.get(x) else FieldType.STR)('shop_name')
print(a)


