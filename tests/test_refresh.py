#coding=utf-8
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time

driver = webdriver.Chrome()
driver.set_page_load_timeout(2)
driver.get('https://www.sogou.com/')
time.sleep(1)
driver.find_elements_by_partial_link_text('微信')[0].click()