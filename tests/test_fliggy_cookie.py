# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
import time
import json

driver = webdriver.Chrome()
driver.get('https://www.taobao.com')
time.sleep(3)
# driver.switch_to.frame(driver.find_element_by_css_selector('#J_login_container > div > iframe'))
# driver.find_element_by_css_selector('body > div > div.qrcode-page > div.icon-pc').click()
time.sleep(80)
dictCookies = driver.get_cookies()
jsonCookies = json.dumps(dictCookies)
# 登录完成后，将cookie保存到本地文件
with open('/home/lab421-ckq/fliggy_cookies.json', 'w+') as f:
    f.write(jsonCookies)