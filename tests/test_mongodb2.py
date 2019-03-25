from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

shop_collection = Collection(Database(MongoClient(host='10.1.17.15'), 'dspider2'), 'shops')
for i in shop_collection.find({'data_source':'餐饮', 'data_region':'千岛湖', 'data_website':'大众点评', 'shop_url':'http://www.dianping.com/shop/66205575'}):
    print(i.get('shop_time'))