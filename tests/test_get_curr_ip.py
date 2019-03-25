# import socket
# try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.connect(('8.8.8.8', 80))
#         ip = s.getsockname()[0]
#         print(ip)
# finally:
#         s.close()
# localIP = socket.gethostbyname(socket.gethostname())#这个得到本地ip
# print ("local ip:%s "%localIP)
# ipList = socket.gethostbyname_ex(socket.gethostname())
# for i in ipList:
#     if i != localIP:
#         print ("external IP:%s"%i)
from lxml import etree
from urllib import request
from pyquery import PyQuery
import re
res = request.urlopen("https://who.is/");
html = etree.HTML(res.read());
a = (html.xpath('/html/body/div[3]/div[1]/div/center/p[3]/a'));
for i in a:
    print(i.text)
# #解析html
# pq = PyQuery(html);
# print(pq[''])
# print(re.findall(r'[\d]{1,3}.[\d]{1,3}.[\d]{1,3}.[\d]{1,3}',html)[0]);
