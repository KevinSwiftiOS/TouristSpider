from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
import json
from .util import *
from .params import *
from spider.driver.base.field import *
from spider.driver.travel.core.traveldriver import TravelDriver
from spider.driver.base.mongodb import Mongodb

def Index(request):
    """
    项目主页
    :param request:
    :return:
    """
    project_health,project_health_data = ProjectHealth()
    project_statistics_data = ProjectStatistics()
    project_list = Project.objects.all().order_by('-created_time')
    project_dict_list = GetProjectdictList(project_list)
    return render(request, 'spider/index.html', context={
        'project_list': project_dict_list,
        'project_health':project_health,
        'project_health_data':project_health_data,
        'project_statistics_data':project_statistics_data,
    })

def Status(request):
    """
    项目状态
    :param request:
    :return:
    """
    id = request.GET['id']
    status = request.GET['status']
    project = Project.objects.get(id=id)
    project.status = status
    project.save()
    if PROJECT_STATUS[1] in str(status):
        result = StartProject(project)
        return HttpResponse(result)
    elif PROJECT_STATUS[0] in str(status):
        StopProject(project)
    return HttpResponse(PROJECT_SUCCESS)

def GlobalStatistics(request):
    """
    全局统计信息
    :param request:
    :return:
    """
    return HttpResponse(ProjectStatistics())

def Statistics(request):
    """
    项目状态
    :param request:
    :return:
    """
    id = request.GET['id']
    project = Project.objects.get(id=id)
    shop_count = shops_collection.find({FieldName.DATA_WEBSITE:str(project.data_website), FieldName.DATA_REGION: str(project.data_region), FieldName.DATA_SOURCE:str(project.data_source)}).count()
    comment_count = comments_collection.find({FieldName.DATA_WEBSITE: str(project.data_website), FieldName.DATA_REGION: str(project.data_region), FieldName.DATA_SOURCE: str(project.data_source)}).count()
    try:
        predict_comment_count = shops_collection.aggregate([{'$match':{FieldName.DATA_WEBSITE: str(project.data_website), FieldName.DATA_REGION: str(project.data_region), FieldName.DATA_SOURCE: str(project.data_source)}}, {'$group':{FieldName.ID_:None,FieldName.SHOP_COMMENT_NUM_SUM:{'$sum':'$%s'%FieldName.SHOP_COMMENT_NUM}}}]).next().get(FieldName.SHOP_COMMENT_NUM_SUM)
    except Exception:
        predict_comment_count = 0
    curr_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    comment_count_today = comments_collection.find({FieldName.DATA_WEBSITE:str(project.data_website), FieldName.DATA_REGION: str(project.data_region), FieldName.DATA_SOURCE:str(project.data_source), FieldName.CRAWL_TIME:{'$regex':curr_date}}).count()
    week_start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - 7 * 24 * 3600))
    comment_count_week = comments_collection.find({FieldName.DATA_WEBSITE:str(project.data_website), FieldName.DATA_REGION: str(project.data_region), FieldName.DATA_SOURCE:str(project.data_source), FieldName.CRAWL_TIME:{'$gt':week_start}}).count()
    month_start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()-30*24*3600))
    comment_count_month = comments_collection.find({FieldName.DATA_WEBSITE:str(project.data_website), FieldName.DATA_REGION: str(project.data_region), FieldName.DATA_SOURCE:str(project.data_source), FieldName.CRAWL_TIME:{'$gt':month_start}}).count()
    result = '店铺:%6s家 评论:%6s条 剩余:%6s条 爬取率:%.2f%% 今日:%6s条 本周:%6s条 本月:%s条'%(shop_count,comment_count,predict_comment_count-comment_count,(lambda x:0 if x==0 else comment_count/x)(float(predict_comment_count))*100, comment_count_today, comment_count_week, comment_count_month)
    return HttpResponse(result)

def RunningResults(request):
    """
    运行结果
    :param request:
    :return:
    """
    try:
        id = request.GET['id']
        project = Project.objects.get(id=id)
        running_results = get_last_line(SPIDER_LOGS_DIR % (project.id))
        return render(request, 'spider/runningresults.html', context={'running_results': running_results})
    except Exception:
        return render(request, 'spider/runningresults.html', context={'running_results': ['当前没有运行结果生成']})

def ShopResults(request):
    """
    从数据库获取店铺结果
    :param request:
    :return:
    """
    id = request.GET['id']
    project = Project.objects.get(id=id)
    shops = Mongodb(host=TravelDriver.host,port=TravelDriver.port,db=TravelDriver.db,collection=TravelDriver.shop_collection).get_collection()
    thead_list = list()
    tbody_list = list()
    shops_data_list = list(shops.find({
        FieldName.DATA_WEBSITE:str(project.data_website),
        FieldName.DATA_REGION:str(project.data_region),
        FieldName.DATA_SOURCE:str(project.data_source),
    }))
    for shop_data in shops_data_list:
        shop_data.pop(FieldName.ID_)
        shop_data.pop(FieldName.DATA_WEBSITE)
        shop_data.pop(FieldName.DATA_REGION)
        shop_data.pop(FieldName.DATA_SOURCE)
        thead_list.extend(shop_data.keys())
    thead_list = list(set(thead_list))
    if FieldName.SHOP_NAME in thead_list:
        thead_list.remove(FieldName.SHOP_NAME)
        thead_list.insert(0,FieldName.SHOP_NAME)
    if FieldName.SHOP_COMMENT_NUM in thead_list:
        thead_list.remove(FieldName.SHOP_COMMENT_NUM)
        thead_list.insert(1,FieldName.SHOP_COMMENT_NUM)
    thead_tuple_list = list()#第一个中文,第二个是英文的元组列表
    for thead in thead_list:
        thead_tuple_list.append((FIELD_NAME_ZH.get(thead),thead))
    for shop_data in shops_data_list:
        td_list = [{FieldName.SHOP_NAME:shop_data.get(FieldName.SHOP_NAME),'id':id}]
        for key in thead_list[1:]:
            if key not in shop_data:
                td_list.append(['nonexistent','nonexistent'])
            else:
                if not shop_data.get(key):
                    if FIELD_NAME_TYPE.get(key) == FieldType.FLOAT or FIELD_NAME_TYPE.get(key) == FieldType.INT:
                        td_list.append(['0','0'])
                    else:
                        td_list.append(['null','null'])
                else:
                    value_complete = shop_data.get(key)#未做修改的value
                    value = value_complete
                    if isinstance(shop_data.get(key),list):#如果是照片列表,就把照片列表转换成unicode字符串
                        value = json.dumps(value)[:10]
                    try:
                        int(value)#如果是一个数字字符串则不进行字符串的切割检测
                    except:
                        if len(value) > 10:
                            value = value[0:10]+u'...'
                    td_list.append([value,value_complete])
        tbody_list.append(td_list)
    return render(request, 'spider/shopresults.html', context={
        'thead_tuple_list':thead_tuple_list,
        'tbody_list':tbody_list,
    })

def CommentsResults(request):
    """
    从数据库获取评论结果
    :param request:
    :return:
    """
    id = request.GET['id']
    shop_name = request.GET[FieldName.SHOP_NAME]
    project = Project.objects.get(id=id)
    comments = Mongodb(host=TravelDriver.host,port=TravelDriver.port,db=TravelDriver.db,collection=TravelDriver.comments_collection).get_collection()
    thead_list = list()
    tbody_list = list()
    comments_data_list = list(comments.find({
        FieldName.DATA_WEBSITE:str(project.data_website),
        FieldName.DATA_REGION:str(project.data_region),
        FieldName.DATA_SOURCE:str(project.data_source),
        FieldName.SHOP_NAME:shop_name,
    }))
    for comment_data in comments_data_list:
        comment_data.pop(FieldName.ID_)
        comment_data.pop(FieldName.DATA_WEBSITE)
        comment_data.pop(FieldName.DATA_REGION)
        comment_data.pop(FieldName.DATA_SOURCE)
        # comment_data.pop(FieldName.SHOP_NAME)
        thead_list.extend(comment_data.keys())
    thead_list = list(set(thead_list))
    # for thead in thead_list:
    #     if 'shop' in thead:
    #         thead_list.remove(thead)
    for comment_data in comments_data_list:
        td_list = list()
        for key in thead_list:
            if key not in comment_data:
                td_list.append(['nonexistent','nonexistent'])
            else:
                if not comment_data.get(key):
                    if FIELD_NAME_TYPE.get(key) == FieldType.FLOAT or FIELD_NAME_TYPE.get(key) == FieldType.INT:
                        td_list.append(['0','0'])
                    else:
                        td_list.append(['null','null'])
                else:
                    value1 = comment_data.get(key)
                    value = value1
                    if isinstance(comment_data.get(key),list):#如果是照片列表
                        value = json.dumps(value)[:10]
                    try:
                        int(value)
                    except:
                        if len(value) > 10:
                            value = value[0:10]+u'...'
                    td_list.append([value,value1])
        tbody_list.append(td_list)
    thead_chinese_list = list()
    for thead in thead_list:
        thead_chinese_list.append(FIELD_NAME_ZH.get(thead))
    return render(request, 'spider/commentresults.html', context={
        'thead_list':thead_chinese_list,
        'tbody_list':tbody_list
    })