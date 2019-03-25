# -*- coding:utf-8 -*-

from spider.driver.base.field import *
from spider.driver.travel.core.traveldriver import WebsiteName,DataSourceName,TravelDriver
from spider.driver.base.mongodb import Mongodb

shops = Mongodb(db=TravelDriver.db,collection=TravelDriver.shop_collection,host='127.0.0.1').get_collection()
comments = Mongodb(db=TravelDriver.db,collection=TravelDriver.comments_collection).get_collection()
key = {
    FieldName.DATA_SOURCE:DataSourceName.ENTERTAINMENT,
    FieldName.DATA_WEBSITE:WebsiteName.DINGPING,
}
print(shops.remove(key))



