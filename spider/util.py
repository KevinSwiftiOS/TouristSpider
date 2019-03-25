# -*- coding:utf-8 -*-
import os,signal
from .params import *
from .models import Project
from spider.driver.base.field import FieldName
from spider.driver.travel.core.traveldriver import WEBSITE_NAME_LIST,DataSourceName,TravelDriver
from spider.driver.base.mongodb import Mongodb
import time

shops_collection = Mongodb(host=TravelDriver.host, port=TravelDriver.port, db=TravelDriver.db,
                           collection=TravelDriver.shop_collection).get_collection()
comments_collection = Mongodb(host=TravelDriver.host, port=TravelDriver.port, db=TravelDriver.db,
                              collection=TravelDriver.comments_collection).get_collection()

def ProjectStatistics():
    """

    :return:
    """
    project_statistics_data = '\"<ul>'
    predict_comment_count_sum = 0
    for shop in shops_collection.find():
        predict_comment_count_sum += shop.get(FieldName.SHOP_COMMENT_NUM)
    project_statistics_data += '<li>店铺:%s家</li>' % (shops_collection.count())
    project_statistics_data += '<li>实际评论:%s条</li>'%(comments_collection.count())
    project_statistics_data += '<li>预计评论:%s条</li>' % (predict_comment_count_sum)
    project_statistics_data += '</ul>\"'
    return project_statistics_data

def GetProjectdictList(project_list):
    """

    :param project_list:
    :return:
    """
    project_dict_list = []
    for project in project_list:
        project_dict = {
            'id':project.id,
            'name':'%s-%s-%s'%(project.data_website,project.data_region,project.data_source),
            'status':project.status,
            'editor':project.editor,
            'statistics':'店铺: ?家 评论: ?条 剩余: ?条 爬取率: ?% 今日: ?条 本周: ?条 本月: ?条'
        }
        project_dict_list.append(project_dict)
    return project_dict_list

def ProjectHealth():
    """

    :return:
    """
    project_health = PROJECT_HEALTH[0]
    project_health_data_list = []
    for project in Project.objects.all():
        cmd = SPIDERPY_PROCESS_CMD % project.id
        if 'start' in str(project.status):
            try:
                int(os.popen(cmd).read()[:-1])
            except Exception as e:
                project_health_data_list.append('第{}个爬虫项目有错误'.format(project.id))
                project_health = PROJECT_HEALTH[2]
        elif 'stop' in str(project.status):
            try:
                int(os.popen(cmd).read()[:-1])
                project_health_data_list.append('第{}个爬虫项目有错误'.format(project.id))
                project_health = PROJECT_HEALTH[2]
            except Exception as e:
                pass
    project_health_data = '\"<ul>'
    for phd in project_health_data_list:
        project_health_data += '<li>{}</li>'.format(phd)
    project_health_data += '</ul>\"'
    return (project_health,project_health_data)

def StartProject(project):
    """

    :param project:
    :return:
    """
    result = PROJECT_SUCCESS
    try:
        cmd = SPIDERPY_PROCESS_CMD % project.id
        int(os.popen(cmd).read()[:-1])
        print('项目已经在运行,不用重复开启!!!')
        result = 'error:项目已经在运行,不用重复开启!!!'
    except Exception as e:
        cmd = SPIDERPY_START_CMD % (project.id,project.data_website,project.data_region,project.data_source)
        print(cmd)
        try:
            os.system(cmd)
        except Exception as e:
            print('%e,没有这个选项!!!'%(e))
            result = 'error:没有这个选项!!!'
    return result

def StopProject(project):
    """

    :param project:
    :return:
    """
    result = PROJECT_SUCCESS
    try:
        cmd = SPIDERPY_PROCESS_CMD % project.id
        print(cmd)
        process = int(os.popen(cmd).read()[:-1])  # 获取floodlight的进程号
        os.kill(process, signal.SIGTERM)
    except Exception:
        print('没有这个项目,无法停止!!!')
        result = 'error:没有这个项目,无法停止!!!'
    return result

def get_last_line(inputfile):
    """

    :param inputfile:
    :return:
    """
    filesize = os.path.getsize(inputfile)
    blocksize = 1024
    dat_file = open(inputfile, 'r')
    last_line = ""

    lines = dat_file.readlines()
    count = len(lines)
    if count > 100:
        num = 100
    else:
        num = count
    i = 1
    lastre = []
    for i in range(1, (num + 1)):
        if lines:
            n = -i
            last_line = lines[n].strip()
            # print "last line : ", last_line
            dat_file.close()
            # print i
            lastre.append(last_line)
    return lastre