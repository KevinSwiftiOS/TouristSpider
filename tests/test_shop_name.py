# -*- coding:utf-8 -*-
from spider.driver.base.field import *
from spider.driver.travel.core.traveldriver import WebsiteName,DataSourceName,TravelDriver
from spider.driver.base.mongodb import Mongodb

shops = Mongodb(db=TravelDriver.db,collection=TravelDriver.shop_collection,host='10.1.17.15').get_collection()
comments = Mongodb(db=TravelDriver.db,collection=TravelDriver.comments_collection).get_collection()
key = {
    FieldName.DATA_SOURCE:DataSourceName.HOTEL,
    FieldName.DATA_WEBSITE:WebsiteName.QUNAR,
    FieldName.DATA_REGION : '千岛湖',
}
shop_name_list = []
for i in shops.find(key):
    shop_name_list.append(i.get(FieldName.SHOP_NAME))
print(len(shop_name_list))
print(len(set(shop_name_list)))