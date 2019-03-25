import requests

import os,re
print(re.findall(r'[\d]{1,3}.[\d]{1,3}.[\d]{1,3}.[\d]{1,3}',os.popen("tsocks wget -q -O - http://pv.sohu.com/cityjson | awk '{print $5}'").read())[0])
# print(os.popen("tsocks wget -q -O - http://pv.sohu.com/cityjson | awk '{print $5}'").read())