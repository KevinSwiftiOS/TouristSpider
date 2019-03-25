# -*- coding:utf-8 -*-
import  platform
PROJECT_HEALTH = ['health','warning','error']

PROJECT_STATUS = ['stop','start']

PROJECT_SUCCESS = 'ok'

SPIDERPY_PROCESS_CMD = 'ps -ax | grep \'python run_spider.py %s .*\' | sed \'/grep/d\' | awk \'{print $1}\''
#ubuntu环境下为该命令
if(platform.system() == 'Windows'):
    SPIDERPY_START_CMD = '\"python run_spider.py %s %s %s %s\"'
else:
    SPIDERPY_START_CMD = 'gnome-terminal -e \"python run_spider.py %s %s %s %s\"'
#windows命令下为该命令

SPIDER_LOGS_DIR = './logs/log_%s.txt'