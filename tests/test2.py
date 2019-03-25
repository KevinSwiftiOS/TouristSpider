#使用pickle模块将数据对象保存到文件

from spider.driver.base.mongodb import Mongodb
from pymongo.command_cursor import CommandCursor

shop_collection = Mongodb(db='dspider2',collection='shops', host='10.1.17.15').get_collection()
print(shop_collection.aggregate([{'$match':{'data_website':'大众点评','data_region':'千岛湖','data_source':'餐饮'}}, {'$group':{'_id':None,'sum':{'$sum':'$shop_comment_num'}}}]).next().get('sum'))
# c = CommandCursor()
# c.