# -*- coding:utf-8 -*-

from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.maximize_window()
# driver.set_page_load_timeout(10)
driver.get('https://www.kaola.com/login.html')
time.sleep(5)
loginbox = driver.find_element_by_css_selector('#loginbox')
iframe = loginbox.find_element_by_css_selector('iframe')
driver.switch_to.frame(iframe)
driver.find_element_by_css_selector('#phoneipt').send_keys('123')
# time.sleep(1)
# driver.find_element_by_css_selector('#phoneipt').send_keys('123')
# time.sleep(10000)