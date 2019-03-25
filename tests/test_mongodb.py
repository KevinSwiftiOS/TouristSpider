from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

shop_collection = Collection(Database(MongoClient(host='10.1.17.15'), 'dspider2'), 'shops')
for i in shop_collection.find({'data_source':'餐饮', 'data_region':'千岛湖', 'data_website':'大众点评'}):
    for j in ['http://www.dianping.com/shop/18238638', 'http://www.dianping.com/shop/66847478', 'http://www.dianping.com/shop/65330164', 'http://www.dianping.com/shop/91599719']:
        if j in i.get('shop_url'):
            print(i.get('shop_url'), i.get('shop_name'), i.get('subtype_name'), i.get('shop_menu'))