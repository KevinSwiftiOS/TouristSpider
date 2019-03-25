import os
import platform
import time
from apscheduler.schedulers.blocking import BlockingScheduler
region_to_websites_ubuntu = [
    {
        '携程':'千岛湖',
        '马蜂窝': '千岛湖',
        '驴妈妈': '千岛湖',
        '大众点评': '千岛湖',
        '飞猪': '千岛湖',
        '去哪儿': '千岛湖',
        '途牛': '千岛湖',


    },
    {
        '携程': '西湖',
        '马蜂窝': '杭州西湖',
        '驴妈妈': '西湖',
        '大众点评': '西湖',
        '飞猪': '西湖',
        '去哪儿': '杭州西湖',
        '途牛': '西湖',

    },
    {
        '携程': '西溪',
        '马蜂窝': '杭州西溪',
        '驴妈妈': '西溪',
        '大众点评': '西溪',
        '飞猪': '西溪',
'去哪儿': '西溪',
        '途牛': '西溪',


    },
    {
        '携程': '溪口',
        '马蜂窝': '宁波溪口',
        '驴妈妈': '溪口',
        '大众点评': '溪口',
        '飞猪': '溪口',
        '去哪儿': '溪口',
        '途牛': '溪口',

    },
{
        '携程': '神仙居',
        '马蜂窝': '神仙居',
        '驴妈妈': '神仙居',
        '大众点评': '神仙居',
        '飞猪': '神仙居',
    '去哪儿': '神仙居',
    '途牛': '神仙居',
    },
    {
        '携程': '西塘',
        '马蜂窝': '西塘',
        '驴妈妈': '西塘',
        '大众点评': '西塘',
        '飞猪': '西塘',
        '去哪儿': '西塘',
        '途牛': '西塘',

    },
    {
        '携程': '横店',
        '马蜂窝': '横店',
        '驴妈妈': '横店',
        '大众点评': '横店',
        '飞猪': '横店',
        '去哪儿': '横店',
        '途牛': '横店',

    },
{
        '携程': '江郎山',
        '马蜂窝': '江郎山',
        '驴妈妈': '江郎山',
        '大众点评': '江郎山',
        '飞猪': '江郎山',
    '去哪儿': '江郎山',
    '途牛': '江郎山',
    },
  {
        '携程': '雁荡山',
        '马蜂窝': '雁荡山',
        '驴妈妈': '雁荡山',
        '大众点评': '雁荡山',
        '飞猪': '雁荡山',

      '去哪儿': '雁荡山',
      '途牛': '雁荡山',

    },
    {
        '携程': '普陀山',
        '马蜂窝': '普陀山',
        '驴妈妈': '普陀山',
        '大众点评': '普陀山',
        '飞猪': '普陀山',
        '去哪儿': '普陀山',
        '途牛': '普陀山',

    },
   {
        '携程': '南浔古镇',
        '马蜂窝': '南浔',
        '驴妈妈': '南浔古镇',
        '大众点评': '南浔',
        '飞猪': '南浔',
'去哪儿': '南浔',
        '途牛': '南浔',

    },

     {
        '携程': '天台山',
        '马蜂窝': '台州天台山',
        '驴妈妈': '台州天台山',
        '大众点评': '天台山',
        '飞猪': '天台山',
         '去哪儿': '台州天台山',
         '途牛': '天台山',

    },
     {
        '携程': '根宫佛国文化旅游区',
        '马蜂窝': '根宫佛国文化旅游区',
        '驴妈妈': '根宫佛国文化旅游区',
        '大众点评': '根宫佛国文化旅游区',
        '飞猪': '根宫佛国文化旅游区',
         '去哪儿': '根宫佛国文化旅游区',
         '途牛': '根宫佛国文化旅游区',

    },
    {
        '携程': '乌镇',
        '马蜂窝': '乌镇',
        '驴妈妈': '乌镇',
        '大众点评': '乌镇',
        '飞猪': '乌镇',
'去哪儿': '乌镇',
        '途牛': '乌镇',

    },
   {
        '携程': '鲁迅',
        '马蜂窝': '鲁迅',
        '驴妈妈': '鲁迅',
        '大众点评': '鲁迅',
        '飞猪': '鲁迅',
       '去哪儿': '鲁迅',
       '途牛': '鲁迅',
    },
    {
        '携程': '嘉兴南湖',
        '马蜂窝': '嘉兴南湖',
        '驴妈妈': '嘉兴南湖',
        '大众点评': '南湖',
        '飞猪': '南湖',

        '去哪儿': '嘉兴南湖',
        '途牛': '嘉兴南湖',

    },
   {
        '携程': '黄山',
        '马蜂窝': '黄山',
        '驴妈妈': '黄山',
        '大众点评': '黄山',
        '飞猪': '黄山',

       '去哪儿': '黄山',
       '途牛': '黄山',

    },
    {
        '携程': '三清山',
        '马蜂窝': '三清山',
        '驴妈妈': '三清山',
        '大众点评': '三清山',
        '飞猪': '三清山',
        '去哪儿': '三清山',
        '途牛': '三清山',

    }
];
region_to_websites_windows = [
    {


        '去哪儿': '千岛湖',
        '途牛': '千岛湖',
    },
     {


        '去哪儿': '杭州西湖',
        '途牛': '西湖',
    },
    {


        '去哪儿': '西溪',
        '途牛': '西溪',
    },
     {
        '去哪儿': '溪口',
        '途牛': '溪口',
    },
    {
        '去哪儿': '神仙居',
        '途牛': '神仙居',
    },
     {
       '去哪儿': '西塘',
        '途牛': '西塘',
    },
     {
        '去哪儿': '横店',
        '途牛': '横店',
    },
    {
        '去哪儿': '江郎山',
        '途牛': '江郎山',
    },
     {
        '去哪儿': '雁荡山',
        '途牛': '雁荡山',
    },
    {
        '去哪儿': '普陀山',
        '途牛': '普陀山',
    },
    {
        '去哪儿': '南浔',
        '途牛': '南浔',
    },

     {
       '去哪儿': '台州天台山',
        '途牛': '天台山',
    },
     {
       '去哪儿': '根宫佛国文化旅游区',
        '途牛': '根宫佛国文化旅游区',
    },
    {
        '去哪儿': '乌镇',
        '途牛': '乌镇',
    },
     {
       '去哪儿': '鲁迅',
        '途牛': '鲁迅',
    },
     {
        '去哪儿': '嘉兴南湖',
        '途牛': '嘉兴南湖',
    },
     {
       '去哪儿': '黄山',
        '途牛': '黄山',
    },
    {
        '去哪儿': '三清山',
        '途牛': '三清山',
    },
];

# if(platform.system() == 'Windows'):
#  website_to_search_keys = region_to_websites_windows['三清山'];
# else:
#  website_to_search_keys = region_to_websites_ubuntu['三清山'];
# #开始结束日期
#
# sched.start();
# sched = BlockingScheduler()
# os.system("gnome-terminal -e 'bash -c \"python run_spider.py "  + str(index) +  " " + "携程"
#             + " " + "千岛湖" + " " + "景点" +
#   "; exec bash\"'")
#os.system("gnome-terminal -e 'bash -c \"python3 run_spider.py 00 携程 千岛湖 景点\"'")


#定义开始与结束的景区
ends = 30;
sched = BlockingScheduler();

#全局的index和景区平台对应数组和计数器表明爬哪个范围内的景区 现在默认每天爬6个
cnt = 0;
website_region_arrays = [];
index = 0;
#每隔多少执行一次
def start_spider():
  global index;
  try:
         select_dic = website_region_arrays[index];

         if (platform.system() == 'Windows'):
           os.system("python run_spider.py " + str(index) + " " + select_dic['website'] + " " + select_dic['region_search_key'] + " " + "景点");
         else:
          #大众点评和飞猪不希望关闭命令行
          #  if(select_dic["website"] == '飞猪' or select_dic["website"] == '大众点评'):
          #   os.system("gnome-terminal -e 'bash -c \"python3 run_spider.py "  + str(index) +  " " + select_dic["website"]
          #           + " " + select_dic['region_search_key'] + " " + "景点" +
          # "; exec bash\"'")
          #  else:
               #关闭命令行
          os.system("gnome-terminal -e 'bash -c \"python3 run_spider.py " + str(index) + " " + select_dic["website"]
                         + " " + select_dic['region_search_key'] + " " + "景点\"'")

         index += 1;

  except Exception as e:
      sched.remove_job('intervalspider')
      print("本次爬虫结束")


def calculate():
     print(333);
     global index;
     global website_region_arrays;
     global cnt;
     #结束的index
     global ends;
     index = 0;
     website_region_arrays = [];
     cnt += 1;
     #数组的开始与结束
     start_index = 0;
     end_index = 0;
     if(cnt % 3 == 1):
        start_index = 0;
        end_index = 6;
     elif(cnt % 3 ==  2):
         start_index = 6;
         end_index = 12;
     elif(cnt % 3 == 0):
         start_index = 12;
         end_index = 18;
     #从数组里面进行统计
     if (platform.system() == 'Windows'):
         #表明结束和字典对数组
         ends = 12;
         website_to_serch_keys = region_to_websites_windows;
     else:
         ends = 42;
         website_to_serch_keys = region_to_websites_ubuntu;

     for i in range(start_index,end_index):
         select_website_to_region = website_to_serch_keys[i];
         # 进行字典遍历
         #进行叠加
         for website in select_website_to_region:

             dic = {
                 "website":website,
                 "region_search_key":select_website_to_region[website]
             }
             website_region_arrays.append(dic);


     sched.add_job(start_spider,'interval',minutes = 15,id = 'intervalspider')

#每天爬取6个景区
sched.add_job(calculate,'cron',day_of_week = '0-6',hour = 8,minute = 52);
sched.start();
