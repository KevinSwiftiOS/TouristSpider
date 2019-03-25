from selenium import webdriver
import time
#
# def get_profile():
#     profile = webdriver.FirefoxProfile()
#     profile.set_preference("browser.privatebrowsing.autostart", True)
#     return profile
#
# def main():
#     browser = webdriver.Firefox(firefox_profile = get_profile())
#
#     #browser shall call the URL
#     browser.get("http://www.google.com")
#     time.sleep(5)
#     browser.quit()


# mobile_emulation = {"deviceName": "Nexus 5"}
# options = webdriver.ChromeOptions()
# options.add_experimental_option('mobileEmulation', mobile_emulation)
# driver = webdriver.Chrome(chrome_options=options)
#
# url = "https://m.tuniu.com/menpiao/t_138"
# driver.get(url)
# time.sleep(5)
# ele = driver.find_element_by_css_selector('#detail-placeholder > div.main > div.tabs-box > div:nth-child(1) > ul > li:nth-child(3)')
# ele.click()
import re
list = []
from pyquery import PyQuery as pq
#html元素标签
html =  '''<i class="icon-star star-active"></i><i class="icon-star star-active"></i><i class="icon-star star-active"></i>'''

style = 'background-position-y:-90px'
width = re.findall(r'[\d]{1,3}',style)[0]
print(float(width) / 150 * 5)
# doc = pq(html)
# print(doc('.star-active').length)